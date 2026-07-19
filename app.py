import os
import hashlib
import unicodedata
import json
import datetime
import requests
from flask import Flask, jsonify, request, send_from_directory, session

app = Flask(__name__, static_folder='.', static_url_path='')
# 임시 비밀키 (실제 운영 시 랜덤 문자열 사용 필요)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32).hex())

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# SEC-03 FIX: Supabase 환경변수 미설정 시 경고 출력
if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ [WARNING] SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다. 하드코딩 명단으로만 인증합니다.")

ALLOWED_USERS_HASH = {
    "156f2206251171b17054c694e8750f862bbfa2aefbc2d3524261337a15f24770": "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0",
    "a0f19d0a0a734a3d10498dbe76d5b851fc0a6ce399e1e956012f3361f1757256": "0a0abd5382ade9afd7067605d9508ef17526b6cb7c7ee48b04549756d81b8aab",
    "9c363eef2c9b2d3fcb2c952820a021596dfa8484eb7fdbe719ffcf44f5aecf07": "611f02bd80facdf0ecf24d2bc73aec046ab719092cd18c0ba7c7368524d38db0",
    "5b91ec1281c3d823dc92928198bee2b35822c2ef6111113198e7d9158df59537": "611f02bd80facdf0ecf24d2bc73aec046ab719092cd18c0ba7c7368524d38db0",
    "481ddb216a499985c8de6781e305767dee6451d46b14640d90d2695a3fbea40e": "af956f342c1c6459ed991798fd3342ed848f24f0e17386831b1ef7b4ef91af34",
    "3e3eb7bd1b3630f9f57153f8bf9aa0e8c054e45a37011a89b3280224285ded1a": "5324c7411a7c61557a17354517b35ae5e31fd5515e44dd475ba12258d1c5f265",
    "d64246030c81dfc5a1a375f8de057b27e6220ee0c2d7a771e232c60b8a662d24": "024f281da9fe62e5914e47d82cd1ab07791d0fc565426e5f6f2405762307a561",
    "39fe8d87fca5d4fd441ddb087b9f798ee08968149fc74d79296814564699cfd1": "89d6aac5e0b914e3b82820f9691e02803786833387db7f0ad09000b83ee212ee",
    "13c7484d9bbcb8f0bf5c13638960465785fb49b0363aa40215fdc7b3205ab824": "b280279a0ef279d0b9f0bdc4162591dbbc6312abac67120527b20d65c7de5dbf",
    "cae279cf253b7d6afb71cef284908a43e0910e72f858e2cceff54308c6766df3": "7ee3819bf62f7e4563a2a9476df6e18a6cd17cceb30b92f00a24a6c8175e3740",
    "18199079baddf7331dfce23af9c90173aefeb51541a60e94ec49f9b7119bb3cb": "15945fafd4ec4cd8e690a6d24cfb05ec2ac904e5091bf65adc3e1df3c43ed290",
    "2f64b26042d87ed7df390e843fe862795a941e1f1adfc2d6a30a08c04a966f6f": "eaf493e8af54e4fb893988a51b83b390a725e24bbe1575a50625c811c08ecb6f",
    "5b6b0247ef514ab935d1a5dd293db9fa95123f7e90684b8e59c445eaf95fe401": "fb1a382ee284b5583dd34f44245ab1444e083b4daec944fa533c19806ff3e90a",
    "69f235dd3d93598686d7b6b079f5a09e35ad288bdf5205d3ef37d5267737ba2e": "f7cc0e8b019506df9430a4245962eb4e1c18cee9f7e58ab1e17a846c3e3d0c84",
    "e36c0aa506f1a6ed21f588431929899ccd4aca7f3b22ca9998e9880fddcd35c5": "a3d951e968e6ca5ee3af64eab235842c06af694b9943eea7fc81eacd738e7224",
    "9435629d95fbaaec4bb35a0bbb4c9bdc86d244e81825cd2f18df2a449e50a603": "3b731d7620bf723f5df5cb3dc1ab0c3f452db716712cc14379a4dfd92d19182f",
    "9bc92a3d4f8fc5f63a737b88d46f03bd3b50f5910fa24f7ab5ea24534f5cb170": "d3a780f832d288bd44a79551a67966f66ffc0145658e162dfe3c8cc010923f58",
    "ab507176d5074c8835453512e1fd3a6a3bd67e79d2d89ddd4c167d2d0965877e": "95935676a6f8cf1183b545413ebe3f7773b11fd806614a208f7149f3e712385e",
    "e4a3fad84871316094a70b72e080e44a93da17307b7c1726c66d39056a17d443": "bf30ed96384de5c4c3e9ca7626bd81ec350074281b86c8c839041b783ff945c0",
    "599abf0bf9c381e30cdab6ce54b2980cc5d3cd594a89e19020f7a7429a628ef8": "e734ce8f057a2863077c0e6e2d2baab2d05a98d063f7d916077db89488bf9dd5",
    "402d8d4920b6c4ad455c759d1ec688ed5f6939af4a9beb62156471e78f97b812": "23f08458907bbe924afada3c2a9b4d82e46b4190ffa0a45d8a35099109f24d4a",
    "c5cd4e7f600b45aac97117b9374a149243183cf6c5f4ee1875b8b14949805bd2": "6bf76be895daa81eecd02713d3fb73d1f5215d48720a139479234c293e88d26a",
    "fa84ec52147f43662b1396085c17a7395076e5c92561376efc4457414d98fbba": "0325d6c1080c79e16fb6027538978fb227d912b89b16e40f23a831f9b80c0423",
    "22ac33e911541eb0bf66787059a10c7f3614656d219139a49aea79ff983354f5": "105068fe92543bdd1ff1938e3abfec9c30a7200d8da65e9c764cd643581f9be2",
    "ab5a5ca66a85745defcd6782ceccd80ccf2ee1ee5b1af49f7b2bd5ff3d39eb4a": "2ec950ea98c80e146cbd6454e2c24d3aeaa3a0d66b0154c73ad106d9e25e811a",
    "19c4a3691f2fb5a1e0738598d4db03af5b7b87a65e3913014c5dfa9ca70332e1": "6b0f184f14930ed2aab00d963792fac1cf7c8439503cb58ac06dde647c456940",
    "62be0185bee2f51b5ea0a40f7f41ec71fa930b46503549c9b821334781131c2a": "5973ede00eaa6fc11f4a294b815dcaeec2f9cb20d203b30257d2976cf4b19cc6",
    "5d5095aafa6fdff3d0fbe7b0c4b2a8bfa7d87240654053b72fc978d6e58a3e2a": "462b01670e50875a9df97c18e87cd367dbe7fbd6f32783be20883747e37d5af6",
    "b6591b7172d78a438a8f0a6897908ed9184d1b18d1e472766090a7d81753052b": "88552e1c2d4d53c988676a44e3eb7ac41e3ee7cbadf45fb505b0443473d445f3",
    "e87851e18e96aa2c0e41f6095d82f70e7b74ddd597998e88dbd7c84771a1a084": "5008a184a9ed025b6380c79a07a851600d0f6245c98c404795b53de8e31e3f44",
    "a30cbf29dac5f5f703efd7b6ec889697b6cddb08dd3e6ba0c80a18c4f437036f": "e3ff67a034be1f249caab8a72f61e8ad2a64e417b5ce6e0941416e56e591994d",
    "27a60914e08f9cb55ae0b20a23fa1a397e9bbaf48eaddf1b4af1039b36b560c4": "5b10564b32ea564df50f0c56353b0b4ed3821fb86fc4555a4aa2461e76d07473",
    "4305bc1a3a6852e96b64c55b228af06891c7727e2ad5e9fe86f442c2e3a3b68d": "71181f5d23343d7db98f90aed3499d8c2a23131b3151cc66c4591918dfc09acc",
    "106faa490f84eb792981e0599b0c345f6e88bf5e672b577268c9124caf68064e": "a24e43b7765e445a86b1904b1c24b094dbd50eaf218ddc9cd6c2b3cbcd72cea3",
    "7ce2ed0026483fdbaa7c6ef3f86c7fcd380a22600e447313ec82363a74338644": "7e245b947ebe781ac1bfeda5f29923699652dc48971898132821a302ddbb3d3c",
    "d7ebd69d2596ca7ad35ce8faa01ec5f7d35030ad2e9c78ee3ed131922b86718d": "0d685d0e6c2a2d4513de2125b3acec7650aef3fa246f77d9ed2ca120e3db297d",
    "5fb4f2c520e29ad0ef7709cf40f2e29bddded8f6980b5125156d306748d5020c": "7ac9206afbb213cb8b284d5031b86dbd721606d5753907a42ba92648ead52a22",
    "dd9df9575c187d647fe0b07c628e7a7d2cf9e104e719efd2515e287d21396255": "e1fc72b4d465a7d03830afe06cb7f2a49f5be2cf26158a44dd9849882830f0bb",
    "1100cef66135ff3853b2cd9a4cbee8d3b166bccfd76fc07eb56e70b972917ddb": "08b25a1fb4a58b22867bb84357d0368b782ebcf3dcf263261a3b7087807ea016",
    "b61b608c352b760cda7ce773ae01d04a2464960d90204c90dbaba603502ae086": "8ecb5bcd8cd84cc3ffc6f5dc3076d81c0a457a6bd4b305a33f318b623d701c2e",
    "d1bd6159ee9945a2f163e496b349673786d17c41dc3fcc9029db4591421fa2e0": "cfe35c9e498096d4463cfade00cdef305d2311d90db9949bf321f87447fc2f1a",
    "96fc9f50acd6a453f4cc71358c9f198cbe4b20acd3b2ede74e2d42d668ff2f86": "9d73bfb92adaebaa346e5c12db11ce0bf0dc5ae059677dcec5198d7302d32493",
    "b2b5c2cb178f40047207d550923b902412147b74d5e1778cba5f86e5b6e1954e": "e0963ee5228d3ea114cc8af37585893a3be748efd68e67b5301d38329c7f65fc",
    "ca64700327eeaa8bc732510af86c1cbd9ede4e43f07e7f49ea8756e4a05f74fe": "da19ec9481cbcf30da9993db3570aa8442c6684464f26030eb2c045152b376bd",
    "06c991252e3b17866c169816c6497744569c957f674a4221d6880c2aad1326c8": "5d9e09b09389f1e4c8268e5464bfce4c9ea6a516f9c84b2f49e313427421ef3d",
    "32c8f64578b87770e4781fd19d6cb9ff79df1d75bf31a570f0c40fdd3a9d1c1d": "2d6c50388f532bd1bbe52e5a25fad2a7fd3955bb2855b0b72cd28765e78b62e9",
    "ad5894be8cfbcd60c9b8cdb216067783d70ea6cedefbc768a2abc0507fb5444e": "dafb86559ecc15b8996f52a2b848861d59136f6df27ebba67472ee74a36456c7",
    "ea7c6db315d9d27ddc41cd75c1676668d60d16c8f45916119ae1d34682a33a0d": "e5a406855f76b37cf13c1da6b49bd00b0e2341c96eba17278303a2b7bb33346c",
    "d85c531b590cf26d5e8ed2907cf3e06f675524a8c8b73946622f77caf854b440": "44ab142b5171cd63db89e3186367c9a7a2a28e5daee21305214ff6626d9fb842",
    "b6b5b62f6beb41c7b5ef5a51a0c8b2555508d043f6987885166e2ebdd401e822": "544101748cc0e2e64e48892f8d27a7fc83245f1a18c6b25f437eb626dbc1345a",
    "a412a39ed23b9824087fc127e41aa4f9862282aacfccaec42646546a93abca5c": "d9f3e0597d973d5f0173fc1d5dba50595188c8650a263c926d6fb3b619667b78",
    "4e7d0b03623999d923775928a1d60be9cc6753ac8c31e65e60a704fcaa853305": "d8b4c70897b50e123d819f719db2cb5931da41e609abd572b815ddeafd6d2847",
    "0d2e51357b1ef45b99736b3c250f4bd13056a4733eb7637bdc6def80e9227b10": "fdbcf987fae167738b6002cf6ffe0581b553cc430e284ccdf82f733860b09772",
    "5ca26c62e1332365f7cc59823e833a02f1303fd3da58c50181dce097724f9295": "41214f55c1e8d6170239eb93d7cc105abbee1dc0fbe8f7a258962da285dfe9cd",
    "d3a76db0c36dbca64482b71bdc9f025d4329a72626c887093f431f2ff7b026b1": "7987e36c43f067b54276ccb5f72d4d495d4ec9d21dab110714eeb9148df9e3ec",
    "79f7b70e00be156e764dae932eba4cf47840fbc1a03b927d89c1ad6df6bb9857": "d845f041e1ad38ef69cba0abbabeb3558a976f50fb4d217e4099fe36fbf8f623",
    "7f5c84579e535dc473255cfb9a369b67e95abc9d8ad9bf95813305294d6c393a": "93de0089bfe55e8e2af2cdc3cfad5280486b63c0bbc8bcf7e069bed9e084ac7a",
    "56f91d75c4faac9f90a434731aec2af0e5dfcfe193745bbe796e7a4a4bd20c59": "a306c73ff0f8e27bfdee1cd291159a49a8f21c31c4c832236d04b1cca8e48cfb",
    "4ee8093dd2ed62b8489d8f03ea04933781ad3db5d860de7a4853410b12425e0e": "13324c96f0cb855057d3eaceeeb8ddc7ac38e8502c8ca130652414fc156c9bed",
    "ee267b4fd78057460b943c98d9be17a21b48fb98002cfa4146b9d6a7f12e3e29": "03340dc42c4919ce6019ae44c24f3997ccd529f7af6f7f516c015338f14631cd",
    "735372c77d6d0777846e38c0a224b6ab620244dd6c344a55c586b1cd85c4af42": "9c62fc31f992e53eb9d965e9dcbd08bc215030db233af0a638d2c2be796ab1b0",
    "e81f1f7cce54a3a3b13c3d265995e65f693ab346712c9aad539b6d59f330ff68": "cb03a2c5a7b9b56fb286424939260fb6fda92ba9ed26f01619d3cee8bdac771b",
    "ecdbd18df46fe93b7105b01f810c749eef059be4bf00113e4a2a0957a9c479ad": "514cfacbe557df83c85cb1f068e280efc5a0a24c9ba49ed0de547a2efcd85c56",
    "dc241d460a13021ed66233ea215408579fa68fd113637e6b13b156655450629b": "86748254b6bfcc91d1a9b18d2b99dc9fdebec608dd68b83c3186a94f36e5f4c3",
    "7752e2c91b4573d336f683b7ce4185c1397845f19d5b298bad0fb696e466b6d4": "c7c1b4da9b9f745dff12aca04605cb7fb33baf4ba84c5b473b16ef1ed16f9c25",
    "1f30b778bdf54621cce9482bdf4fcccc8eed6468ddca3a5582b60b441ff43b4f": "a62aef6bb252cddd3bba35aa52968f35ba596d0e5cda16b5989b195a5c4df4a5",
    "5486230318bfaa9cb56ea6023dc6226112f4017c4e5e9e0cf4cd963bc269a463": "44021a167f13d094844b227e9d97d834de20cf0473c99a9eddc5c702a1f66697",
    "bd30e33135466ebce9ca5032985edae98544ce68946b1885df4dd23046ae2b63": "8ff9538e65e6781d654b811f88161d12455935ffb8f470815063b6ab6cb7fdff",
    "6628b2e7a6a0197d76eb745087abb5bc45206f11ac72a5c67e4dd85d3508969c": "d7bf08e6602a741a0d3ca2e65907bb5f32def1b31a11e0c87b0a7d44545fcb10",
    "ee118959fde49647dc70271ebb0da17abd5401a708fc81a1df1c966ee4cfc981": "56cc29cee9e859a5314952b8184da882e2482d7bc17234b4ca333bfffe5f74f3",
    "9d4560f6f65aa5f6ef044e55338a2f2d3506598910092c4dbb366e391418e643": "997b0081a9cb967261b9554336e8edda0019827a98334da2cd3841bfb09c1bca",
    "1efd16e74ec7d800658b8d1b3d1b48b022c7c182eb62c6e9a9e3eb52c462c6b3": "23f08458907bbe924afada3c2a9b4d82e46b4190ffa0a45d8a35099109f24d4a",
    "d291c8b32c41057fe82a163ece7afdc0f4f5942fddd267d2335a81eec15a66da": "6ed701cfedb16ebd91b2d185383115c6f9ce12f2f9c744d7d605be0002109362",
    "f6b93ba667569fb8eb972a72ba167cfe8e5b95aced82275230b2ec0bb4b14df8": "8efb3a60255de6db1c77dcdaec905d1045a88e70dddd53d524fc4cb7d1a609d7",
    "6234cd04c10e63ac273fe605827c6e79846a53bfc2baeca991b18f3761db024f": "909033570f5545191e17d1c5ec80f6e822c0ed7f5af9838ee96c0b1781273317",
    "c5c33aad70b000e20ee5f8e908488ec373c30c587f4257d7fc7ad2754d85a72d": "1f498bac4b23bacc32684c7a2f3abeca22d55509ecfa6853e1d428c0443218c2",
    "04daa54c8b239dd2faec115346ab3e406f9052c0a42a1238ab58a336bb5fbbab": "f72b71f2cf7221d17e8e7dcb23ba1aebadee8813fb843860fa6894b9c658269c",
    "76724cdcc40834408c982e0556194dba735745f7b0eded79b07a536ea29bb91b": "d5aa5e4ae9fc046931742f900b38d9c7be0c904a30b68f542479aff13237e6a0",
    "8c5138c6377ff04416270f499fe78e16ec966e66900b4f028f6941079343829a": "03c3ee4bc24a67660cf377bb85ef4ee4c4723f1d2d99b4caf7886b005d4d9954",
    "c80bf41727f41fd80e0c30eaceec835d38758f4e41e8ac3656e4bf3c35447498": "572878043beff72a7ae455785619593dac4a462771c18335de2a49a010efbc47",
    "531260d1367969a7913524ac46f75cba63cb840780dc656e9a3c580f15dab1ba": "2181cc570872136d026dfc526621b9ec092bfb2effe888fba88a6c52f8965430",
    "5cba0888bbcf631426b639b21ca1eb726ebc598eb2feb13474eceb2f97c8bd62": "f6e2d4fb073bdf38cd18c5437c5cc814130a9d9529a949f14c492d3231b6ec6a",
    "249d1785c6866cd9b73ef1ea5ee4195c11a3c3ba92494343760e763fff122d40": "f6e2d4fb073bdf38cd18c5437c5cc814130a9d9529a949f14c492d3231b6ec6a",
    "3a49b513ddebeb5f1b7208ef037d9df2abaee48b9574d91204f38cd2fb8704e2": "756a6524cdb2d4eaad13228bd69d6266ffbb77c78e7f3cfde29e2667f38d3a2d",
    "b076c46b5d9b4e2bf0b59bb92f39a319ba61e5b3475aa77ce508e64aa9541575": "8d2efba45f136abdd6d9548ca3be7df0542bb39e5c0aadba883e191d1c54712b",
    "0ff30f5d3e9bec2f1e598ef550aa756653e881064a14934bbb2deb7c09b83441": "48e6d088c751a0bd26be61e1279c16d39b810de6b18c91ac178b4bab87f0ffd4",
    "7dddae73a80907bb2f4560eaf72ceedd065f2f615256ab537eeacbd790f7a05f": "a740a8741ca6c59b0e0f1d2e5037677b8fbd7b0c34ee4f7791be025d904170cc",
    "a18c624c73f837f01ce189f40090ff0c064dc68dfa726ecc4aca6665d46331a4": "c2c358e9dd15de84331652b848b7ad410ef3f0f8a06a312065349f6c58991966",
    "fd601c231a25cf899477f88d7585406119fd138ed64e9da1913e0cda70f9dd3a": "7ca26aafbfe189a20d2fed657ddcca8aa31581ee6838b90289c4faa4dd23fef8",
    "083ce048149966cfe211dfc88ad50cf83bd6309a22e7817f1aac0a972634a8a7": "78a69c6fdc7b95f502f14d3c826b21528318ef248796d5a41478096973dd1ad6",
    "abd36d9edb9f3e787308a3f263d1e301360b80ae2b2e0eaf341f4e3685fa70f7": "374c0fd6e94e0cec99de6089e5a6409dc4816b0f9427363c44b8985f60481f35",
    "7ac407e04698b5541411ac9ce3dbdf1e7de112e3a090894ae1469d31a058ccd1": "434f4d14c1eb231306b51aaa160c021b63670ac6ca67fb8e403f4500983dd1e4",
    "4ada0ba5227f8c1e9737d025dfeb36c81c8dfbea4898c6e784434f048f5d513c": "f7d7736a8f77a494064203eda8d618bb0cfbe19668065fa083825ecdc1eda540",
    "2941cc17f83c2dafdaac06447a40dc4842f6f6c84637eb45345562bb686fdbc3": "cf3b763a62724306dca2a00ed53a7c0a19074286e40b8f0b96544ccbab4aaae2",
    "bf40392d2dc7da13d7a14c2408cf0738585e574968630ada8d2a53bb892148c0": "b954bc4acaad1bfa43689f654027227c6cd416e797fbf7ddbd2a38864d857a5e",
    "196ba51dc6297cea4a791253a6accfb23ff333db0320fb4fde1fb7e2f628fe75": "ea4bdbc1419b6c7aa4919f1276fcb3eb6fd9a316e52e177fa519b1cbe9fbb3de",
    "07947665e58f2c5f608cb2d61041957c9900a2bca66b76ea2b3e535102b531cb": "a1fb4e703a9ef1fa4936801721ff285a97ac85330856674412e054892afe6972",
    "0447a608b0327060df1e4547cb35ddfb657c25cddd0e30e45b16b01861b79bc4": "d1913a47aec9a99a549e8d075b5118abcabd8e8599d6fbbdb67785a5c31d9b03",
    "f02361a6f605b192d7de8c1eeef059434c77f135b5381f301530f8b0580b3a3e": "5119e090c80757fec3c9f1dca46e3481688fed2fea905db0af7994857abb92a6",
    "06c86870ce966a9f790dea92f6867803625c990e30a5cf3cc5389382e5b29824": "03b0bd366e8184f8d871c3a7c7cc26c73c25b54ff54c64b28b10b898242cdc8a",
    "c1a8c38de902dd1df2981ad2283da6c5c30f688b08cd3a6ee469c5bd9dedcb01": "2ec1d83738358cd8610d8d7a699891f1e5d7dd9bdf6f82ae70d048bc13f7f11f",
    "db9f88c413c428ffc06bbbfd0fad941bb22e61cbc91df66c1ba5dbd042e93ae3": "2c2ae095d55ddbc0487f97a5e8db5ecd4b2f1538cd67e774b461d85c4b96a216",
    "bb4f332ffa027fa030c3cdf98e7470a288140afdaa0e83d83b062db008c86812": "cf1881df6f1696c2e59b47fde80838e66a1dfad4f0e993fd686186333456b55d",
    "886f574366984d340a2215ab5ae1983fe4c6bf0f0e2af656a4725414c114edec": "f1294f35f19846cd012506eadcc13ecda95eb7ddc6c661bc1b9402c4b00eb703",
    "c029836f84a430f0379582ebc21c608a7e88ffff08bfcf2c314fb7c9934a3be8": "f0e6a61a0b0037aa12879a3ba580a7b84ef77cd5a8a39f1832589d6390b7fa66",
    "ea6e683cd089bc5c027c159b5d338ec6f946e67b7cfba82a15080e066291712b": "461b2e3622293c303571880413edf2e26b35f5d191b30a32e7eea20da00613d2",
    "dc761a887aa6cb6a65e45abb1e6e8c44c10be54cfa7a2786b7e6d4fa1ff50a31": "29d9c129c3e755f6bd3f321ea47f6dd67bc9023b6bca2a8018a80be2adb6c957",
    "3b8dec7dbb7b718dd727903ef521e6b519cddb12868b3212aba7f5c940c0bbf5": "4baabeaad579e9201bfd7bc4dd8ba8392ce01ef09e8067c740adc882fdcba548",
    "8f2ccb383557c7d98945e0f0824f78940b22f1bdb21af0a055303d5be31c8474": "d0c9e369bee256f4b0182a503babb685ee7b00419c985fb423a47bfb0eb89f56",
    "e23397ee20dbe830cdf81b83a23633551b5cdc433c225e7e8ea7163a052c67f1": "de8736cc048486e16dcd174d8f5f0bc3e19aa4f0b0c26a19572b4cfafa5b31ca",
    "b05193a2568cce567074c3c8e78fa4e822c627ac42f85d6ccda430bf3a30dc00": "16d5164c6ff6bf7201a90e9ec406fe9d122c9894cda28854a05e68ff1f2e804c",
    "305bf59e098d3d08c90af0436ee6e21705662419e9d5152a4b11e80275cf051d": "6bfc25cc7df52b4fabc33e36962aed9620b8f61ad7bbab543996d0575e12c832",
    "b2a391ae19bb65ef90bfb6a78fcaece1c2a8099e7814373bc19ce95ec54bc62f": "ac2151d8aa26b5784551edad3b8ffdaf126a08a8f4ae57db2fc94e01b5443860",
    "64a5b67b01286e3052bae5698468ee5d95a5025952ad3fd424fd6d6c46f71e40": "714bc174ac5066ca0a4a710f503d76ce0254e2c8d1e313abf90171be0ff5975e",
    "13318b0c637272965f6b891dbefca6a5c3b913711818c112ce9c3768cd34f9a5": "88367dd16bfd18ba5595a82d9076f8405807ea4df66c0d282de850391349986a",
    "165cc6f8db72aeee16f9336b0f3abd6c6cbb3f29d22bc03906f45e87f6e8fd19": "2612d391c1eb9a05beb967f1f2adaf215a544bd5e2d88d2a13c531e56af493a6",
    "412f9b3f64294c6337d7be6680037813efaa066e02ba1704a0be0ccd5194fc36": "7d4a25031f5a15141275e08712537464836bbe2cc81512cadfa828d619cbba4a",
    "5f3cccee7b06941609fb55be6396dbd9a3d9c94e5346e91a6ad8ba1c04834b80": "a498b30af4f790314c211c4e6a9a4d8c37015ec9102a6496406cd49b85d37502",
    "be4b08c15fb586cae8972bb1f28da0c08054abbafbb91c67ffaa04027dce7d44": "de7d5e6247fb643608b4f5ef96726ec0c478e1499bcf1f650fa4cf118063dad0",
    "5b1d1063bf62836cedfed54c6af4c3ecb6af92d99b6012c8bf280d93e129b4fc": "179cf283f9f50c9bbf5b86380349d36adf78f5f47d09f939e7a1bf190e8641f4",
    "0cec8e0c1dbec4a4cad36144b3ba9a9a8bb8892f64c4ffe3c3357cbf83db2e59": "9c27727c109abd005defbcac1ab6f1a69a3f858144024969816b65c00f89ed18",
    "2822ac4015f1156b5be7e2b34e223c4c8e336504cc610fea04a9c52f369fd5b2": "c15195e527aab50976ac9ac7596cc6521f141e8499f65be42f0a7df3445d12ab"
}

def get_hash(text):
    normalized_text = unicodedata.normalize('NFC', text.strip())
    return hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid request"}), 400
    
    name = data['name'].strip()
    password = data['password'].strip()
    
    name_hash = get_hash(name)
    password_hash = get_hash(password)
    
    # 1. Supabase 데이터베이스 검증
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/user_credentials?username_hash=eq.{name_hash}", headers=headers)
        if response.status_code == 200:
            db_data = response.json()
            if db_data and len(db_data) > 0:
                # DB에 등록된 유저라면 DB 비밀번호로 검증
                if db_data[0]['password_hash'] == password_hash:
                    session['logged_in'] = True
                    session['user_name'] = name
                    is_master = (name == '김중일')
                    session['is_master'] = is_master
                    return jsonify({"success": True, "name": name, "isMaster": is_master})
                else:
                    return jsonify({"success": False, "message": "비밀번호가 일치하지 않습니다."}), 401
    except Exception as e:
        print(f"Supabase error: {e}")

    # 2. Supabase에 없다면 기존 하드코딩 명단(ALLOWED_USERS_HASH)으로 검증 (초기 로그인용)
    if name_hash in ALLOWED_USERS_HASH and ALLOWED_USERS_HASH[name_hash] == password_hash:
        session['logged_in'] = True
        session['user_name'] = name
        is_master = (name == '김중일')
        session['is_master'] = is_master
        return jsonify({"success": True, "name": name, "isMaster": is_master})
        
    return jsonify({"success": False, "message": "이름 또는 비밀번호가 일치하지 않습니다."}), 401

@app.route('/api/change_password', methods=['POST'])
def change_password():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401

    data = request.get_json()
    current_password = data.get('current_password', '').strip()
    new_password = data.get('new_password', '').strip()
    
    if not current_password or not new_password:
        return jsonify({"success": False, "message": "비밀번호를 입력해주세요."}), 400

    name = session.get('user_name')
    name_hash = get_hash(name)
    current_password_hash = get_hash(current_password)
    new_password_hash = get_hash(new_password)

    # 기존 비밀번호 일치 여부 확인 (Supabase -> 하드코딩 순)
    is_valid = False
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/user_credentials?username_hash=eq.{name_hash}", headers=headers)
        if response.status_code == 200 and response.json():
            if response.json()[0]['password_hash'] == current_password_hash:
                is_valid = True
        else:
            if name_hash in ALLOWED_USERS_HASH and ALLOWED_USERS_HASH[name_hash] == current_password_hash:
                is_valid = True
    except Exception as e:
        print(f"Supabase password check error: {e}")

    if not is_valid:
        return jsonify({"success": False, "message": "현재 비밀번호가 일치하지 않습니다."}), 401

    # 새 비밀번호를 Supabase에 Upsert (저장/업데이트)
    payload = {
        "username_hash": name_hash,
        "password_hash": new_password_hash
    }
    upsert_headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    
    try:
        upsert_res = requests.post(f"{SUPABASE_URL}/rest/v1/user_credentials", json=payload, headers=upsert_headers)
        if upsert_res.status_code in [200, 201]:
            return jsonify({"success": True, "message": "비밀번호가 성공적으로 변경되었습니다."})
        else:
            return jsonify({"success": False, "message": "DB 저장 실패"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"서버 오류: {e}"}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/check_session', methods=['GET'])
def check_session():
    if session.get('logged_in'):
        return jsonify({
            "success": True, 
            "user_name": session.get('user_name'),
            "is_master": session.get('is_master', False)
        })
    return jsonify({"success": False}), 401

@app.route('/api/analects/today', methods=['GET'])
def get_today_analects():
    try:
        with open('analects.json', 'r', encoding='utf-8') as f:
            analects_list = json.load(f)
        
        # 오늘 날짜를 기준으로 인덱스 계산 (매일 자정 변경)
        today = datetime.date.today()
        day_index = today.toordinal() % len(analects_list)
        
        return jsonify(analects_list[day_index])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.json
    project_name = data.get('project_name', '')
    content = data.get('content', '')
    is_anonymous = data.get('is_anonymous', False)
    
    if not content:
        return jsonify({"success": False, "message": "Content is required"}), 400
        
    author = "익명" if is_anonymous else session.get('user_name', 'Unknown')
    
    feedback_entry = {
        "id": hashlib.md5(f"{datetime.datetime.now().isoformat()}{author}".encode()).hexdigest()[:8],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "author": author,
        "project_name": project_name,
        "content": content
    }
    
    # ADD-07 FIX: 파일 잠금으로 동시 접속 시 Race Condition 방지
    import fcntl
    feedback_path = os.path.join(os.path.dirname(__file__), 'feedback_db.json')
    try:
        # 파일이 없으면 빈 배열로 생성
        if not os.path.exists(feedback_path):
            with open(feedback_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        with open(feedback_path, 'r+', encoding='utf-8') as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # 배타적 잠금
            try:
                feedback_list = json.load(f)
            except json.JSONDecodeError:
                feedback_list = []
            
            feedback_list.append(feedback_entry)
            f.seek(0)
            f.truncate()
            json.dump(feedback_list, f, ensure_ascii=False, indent=4)
            fcntl.flock(f, fcntl.LOCK_UN)  # 잠금 해제
            
        return jsonify({"success": True, "message": "Feedback safely delivered."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    if not session.get('logged_in') or not session.get('is_master'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    try:
        if os.path.exists('feedback_db.json'):
            with open('feedback_db.json', 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Protect sensitive static files (like the weekly report html/pdf if they exist in a protected folder)
# Currently, the frontend loads an iframe to a local file or absolute path, which isn't secure. 
# But this satisfies the basic requirement of server-side login.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 15000))
    app.run(host='0.0.0.0', port=port)
