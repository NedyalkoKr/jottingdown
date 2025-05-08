import re
from django.utils.encoding import punycode
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator


def validate_not_all_numbers(value):
    if value.replace('@', '').replace('.', '').isdigit():
        raise ValidationError("Email address can't be all numbers.")


class PasswordMaximumLengthValidator:

    def __init__(self, max_length=64):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                message=(f"Your password must not exceed \
                    {self.max_length} characters. Your current password is \
                    {len(password)} characters long."
                ),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return (f"Your password must not exceed {self.max_length} characters.")


class PasswordSpecialCharacterValidator:
    ALLOWED_SPECIAL_CHARACTERS = "$ # ? ! ~ . _ { } [ ] < > : %"

    def __init__(self, special_chars=ALLOWED_SPECIAL_CHARACTERS):
        self.special_chars = special_chars

    def validate(self, password, user=None):
        for char in self.special_chars:
            if char in password:
                break
        else:
            raise ValidationError(
                message = ("Use at least one special character."),
                code = "password_has_no_special_chars",
                params = {"allowed_special_chars": self.special_chars}
            )

    def get_help_text(self):
        return (f"Use at least one special character {self.special_chars}")


@deconstructible
class UsernameValidator(ASCIIUsernameValidator):
    regex  = r"^[a-z]+$"
    message = ("Username can't contain digits, uppercase letters, whitespace or any other symbols. Only English letters are allowed.")
    code = "invalid username"
    flags = re.ASCII


@deconstructible
class NameValidator(RegexValidator):
    regex = r"^[a-zA-Z]+$"
    message = ("First or last name can't contain digits, or any other symbols, only lowercase and uppercase letters.")
    code = "invalid name"


@deconstructible
class DisposableEmailDomainValidator(EmailValidator):

    tld_blacklist = ['kr', 'ws', 'cc', 'xyz', 'cf', 'cx', 'ga', 'gq', 'tk', 'us', 'ru', 'pl', 'ml', 'info', 'email', 'biz', 'pro', 'mx', 'mobi', 'asia', 'buzz', 'tech', 'top', 'site', 'tc', 'mu', 'be', 'la', 'at', 'dj', 'vn', 'pw', 'dating', 'to', 'ch', 'uk', 'club', 'fr', 'ma', 'ht', 'za', 'nz', 'hu', 'team', 'studio', 'media', 'space', 'store', 'wtf', 'io', 'computer', 'me', "one", "net",]

    email_blacklist_domains = [
        "sharklasers", "grr", "pokemail", "guerrillamail", "guerrillamailblock", "spam4", "maildrop", "yopmail", "vmani", "mailinator", "trash-mail", "trashmail", "10minutemail", "yepmail", "anonbox", "mailgano", "jetable", "moncourrier", "monemail", "mymail", "speedmail", "example", "zwoho", "cuoly", "eoopy", "1usemail", "funnymail", "spoofmail", "doublemail", "puppetmail", "emailgap", "opentrash", "fake-box", "rhyta", "monmail", "emltmp", "emlpro", "emlhub", "10minut", "lachezvos", "spamgourmet", "acrossgracealley", "onekisspresave", "vusra", "yomail", "bedroomsod", "cutradition", "maildax", "knowledgemd", "hide.biz", "courriel", "jetable", "cool", "thespambox", "eyepaste", "gufum", "niback", "trazeco"
    ]

    message = ("Enter a valid email address.")
    email_username_duplicate = ("Email is the same as the username.")
    code = "invalid email address"

    def __init__(self, message=None, code=None, user=None, whitelist=None):
        super().__init__(message, code, whitelist)

    def __call__(self, value):
        if not value or '@' not in value:
            raise ValidationError(self.message, code=self.code)

        user_part, domain_part = value.rsplit('@', 1)

        if '.' not in value:
            return
            # raise ValidationError(self.message, code=self.code)
        else:
            tld_part = domain_part.rsplit('.', 1)[1]

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code)

        if user_part.isdigit():
            raise ValidationError(self.message, code=self.code)

        if user_part[0].isdigit():
            raise ValidationError(self.message, code=self.code)

        if (domain_part not in self.domain_allowlist and not self.validate_domain_part(domain_part)):
            try:
                domain_part = punycode(domain_part)
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise ValidationError(self.message, code=self.code)
        
        if domain_part.find(domain_part) in self.email_blacklist_domains:
            raise ValidationError(self.message, code=self.code)

        if tld_part in self.tld_blacklist:
            raise ValidationError(self.message, code=self.code)

        for email in self.email_blacklist_domains:
            if email in domain_part:
                raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        super().__init__(other)
        return (
            isinstance(other, EmailValidator) and
            (self.domain_allowlist == other.domain_allowlist) and (self.message == other.message) and (self.code == other.code)
        )


@deconstructible
class BlacklistDomainsValidator(RegexValidator):
    regex = r"pornhub|manyvids|ninjastream|tokyomotion|osakamotion|gofile|supremacist|fleshed|donkparty|redskin|raghead|xrateduniversity|xbabe|keezmovies|bravotube|bunnylust|whorish|here.xxx|drtuber|bobs-tube|videosz|digitalplaygroundnetwork|tiava|tube-bunny|clips4sale|tinder|nostringsattached|lobstertube|wankoz|bongacams|streamate|shag|redhotpie|xozilla|xtapes|freeomovie|plusone8|watchxxxfree\b|czechvideo|hitprn|perfectgirls|xfreehd|paradisehill|xxxfiles|taxi69|justswallows|fux|perverzija|fapmeifyoucan|euroxxx|hotgirlclub|flirt4free|flirtymania|sakuralive|luckycrush|imlive|skyprivate|dirtyship|influencersgonewild|nudostar|prothots|thothub|ibradome|teenager365|nudes7|fapfappy|bitchesgirls|famousinternetgirlsgalleries|fapopedia|cyberleaks|premiumbooty|celebjared|viraltags|vfansleaks|vthotpacks|javtrust|hpjav|vjav|incestflix|milfnut|realsrv|eacdn|betus|commissionkings|pnxbet|oshi|rubyfortune|spincasino|casinopurple|stripchat|sakuralive|fapcandy|slutroulette|coomeet|dirtyroulette|thecuckoldconsultant|shagle|eroleaks|bollock|thepiratebay|1377x|demonoid|nyaa|iptorrents|zooqle|torlock|limetorrents|sickjunk|deepgoretube|rapelust|winbet|cutscenes|xrares|home-made-videos|kaotic|inhumanity|fuqer|chatpic|luxuretv|crazyshit|pimpandhost|bet9ja|roobet|mrplay|royalvegascasino|pnxbet|imagevenue|damimage|betfury|superslots|wildz|sportsbetting|mybookie|slotocash|betonline|meetinchat|3movs|watchmygf|mansurfer|hypnohub|smutr|thefappeningblog\b|realitykings\b|tacamateurs|bffs|czechcasting|celebsroulette|topnudecelebs|celebuzz|tmz|justjared|imperiodefamosas|lushflirt|hornywife|zmero|masutabe|thelittleslush|metart|camsoda|boobieblog|eroticbeauties|uncams|amodoll|uescort|morazzia|readysetcam|thebestfetishsites|clipfoo|melonstube|gfsvideos|hentaihaven|thenipslip|girlscanner|flashingjungle|russiasexygirls|fleshbot|spizoo|godude|penthousegold|hustler|clubseventeen|devilsfilm|21naturals|segavideo|pureleaks|fikfap|fansteek|findhername|f95zone|camonster|trafficjunky|gamcore|fap-nation|lewdzone|androidadult|iloopit|literotica|eroprofile|myxclip|zoig|submityourflicks|adultism|thecamdude|babesdiscounts|vipergirls|jerkdolls|peefans|tgtube|eurogirlsescort|adultsearch|medleyads|privatedelights|mintboys|adultfriendfinder|camrabbit|tsescorts|skokka|harlothub|eroticmonkey|ghettogaggers|darknaija|babepedia|lemmecheck|100bucksbabes|elephantlist|swallowbay|thumbzilla|alohatube|femjoyhunter|jperotica|metarthunter|xerotica|chatzozo|erome|catsnbootsncats|xmissy|cremz|orgasmatrix|girlsofdesire|sweetlicious|smutr|kikdolls|homemoviestube|hentaied|heymanhustle|yesbitch|okokoras|popwrecked|silkengirl|babesandgirls|babeimpact|sensualgirls|bustybloom|urlgalleries|imagefart|alrincon|tryquinn|ixxx|realgirls\b|naughtyblog|onlythots|pixhost|siterips|exposedcasting|brattysis|freshoutofhighschool|nscash|amateurallure|familylust|lustery|myfriendshotmom|dadcrush|pascalssubsluts|hookuphotshot|burningangel|analized|toughlovex|fit18|hegre|tonightsgirlfriend|piratecams|lasfolladoras|bellesafilms|40ozbounce|wetandpuffy|scrolller|find-bride|fling|blackcrush|tsdates|redhotpie|ashleymadison|yoni|dogfartnetwork|xlgirls|javfree|bigtitsdiscounts|scoreland|firecams|immorallive|xlovecam|preggophilia|redclouds|femefun|dothewife|fetster|sinclips|efukt|humoron|heavy-r|nonktube|cutscenes|bestgore|bestrapeporn|sickjunk|pandesiaworld|iphun|freeones|dickflash|cameraprive|qrlsx|swallowed|videobox|8muses|letsjerk|primecurve|tantaly|siliconwives|curvyerotic|curvywebcam|brdteengal|freexcafe|cat3movie|vidsgator|loveherfeet|videbd|xnalgas|trkbc|radicaljizzlam|antoniosuleiman|hitprn|pictoa|fapcat|thatsitcomshow|shoplyfter|vivthomas|ersties|hazeher|oldje|bluepillmen|grandmams|ccbill|dreamtranny|transfixed|transangelsnetwork|tsplayground|dropmms|livedosti|apeshit|letsdoeit|mamacitaz|cherrypimps|boodigo|hotmovies|fyptt|findtubes|hotmovs|rubmaps|bedpage|vixen|loan4k|butthole|teencoreclub|karups|nothingbutcurves|helixstudios|nextdoorraw|humpchies|xxxstreams|imgcloud|escort-ireland|sinns|cdgogogo|ohentai|pinkworld|fancentro|bentbox|bannedstories|loyalfans|fansly|xfantazy|booloo|porzo|lovense|bellesaplus|flingster|streamen|dudesraw|boy18tube|webcamjackers|mansurfer|latinleche|butchdixon|gydoo|queermenow|zybrdr|uberhorny|xcams|adultseek|megapersonals|escortbabylon|locan|scarletblue|angelsoflondon|phncdn|perfectly-girl|mydirtytinders|bitcoinadvertisers|cryptocoinsad|bitcoset|bittraffic|doubleclick|gaynetwork|gaybeeg|nnmclub|hotcelebshome|thehun|guyswithiphones|freebunker|imagesnake|imgcarry|bootyoftheday|maturetubehere|4tube|peekvids|7mmtv|celebjihad|badjojo|instawank|smutty|pinflix|9vids|sxyprn|sexvid|tuberel|boundhub|boysfood|tubegalore|megatube|babestube|trannylime|moviesand|submityourflicks|pinupfiles|pervnana|notmygrandpa|granddadz|grandmams|laceystarr|ageandbeauty|latinaabuse|oyeloca|virtwish|grindr|redgifs|swag.live|jlist|virtualmate|teenpies|feetfinder|girlsway|lesbea|ersties|addicted2girls|sheseducedme|webyoung|mommysgirl|ftvgirls|met-art.com|kindgirls|primecurves|babestation|cambb|xcamsclub|harlothub|kanadoll|hanime|mencelebrities|fuqqt|xxxbios|exotic4k|interracialpass|nsfwalbum|vidmo|hdzog|nudography|rat.xxx|rusdosug|sleazyneasy|youx.xxx|yourlust|xxxrip|stileproject|pervclips|fantasti|zoofiliatube|watchjavonline|txxx|kantotero|xbree|pinayot|javjack|inserted.com|dorcelclub|deviante|eritonetwork|sislovesme|familystrokes|blacksonblondes|swallowed.com|adulttime|rtbabeskiss|redtube|xkeezmovies|xnxx|spankbank|beeg|chaturbate|livejasmin|xvideo|xhamster|cliphunter|youjizz|mofosnetwork|javtrust|fapster|fling|xxbrits|4chan|4cdn|youporn|omegle|tsyndicate|fakehub|mylf|scout69|faphouse|brazzers|puretaboo|taboo6|asiafriendfinder|mature.nl|amigos.com|babesnetwork|melonjuggler|momswap|nurumassage|fakings|naughtyamerica|nudevista|noodlemagazine|mywape|voxxx|cat3movie|imagefap|vintagetube|film1k|painaltube|dump.xxx|nothingtoxic|nubileset|parodypass|nubiles|fapello|babesandbitches|sexykittenporn|littlepeachytoys|hqbabes|hegreartnudes|wannawatchme|bestlivecamsites|glam0ur|novoporn|rabbitsfun|find-datings|mylked|clubtug|seemomsuck|tugpass|tube8|theleakbay|wicked|mofos|hornyfanz|motherless|rechub|watchfreejavonline|eincest|cutscenes|theync|shooshtime|fuskator|pornpics|dirtyshack|kenyaadultblog|nairobihot|xlviirdr|cumclinic|familyporn|callofdating|fapvid|hellporno|1000facials|blowpass|immorallive|mommyblowsbest|throated|czechav|pervmom|caribbeancom|mddmp03|teamskeet|lovehomeporn|letsgodirty|niksindian|boobzig|roccosiffredi|mydirtyhobby|auntjudysxxx|korea1818|blackedraw|sexyhub|tushy|bannedsextapes|fundorado|bambiblacks|inflagranti|fetishnetwork|thaigirlswild|taworship|theartporn|shadyspa|eroticax|summersinners|alsscan|oldiesprivat|amkingdom|oldgoesyoung|omapass|milkyperu|lezpov|real-teens|scandalousgfs|beautyandthesenior|vip4k|elegantraw|stepsiblings|realsexpass|girlcum|hardx|amarotic|herlimit|tiny4k|bbvideo|brutalx|avidolz|sexmex|heavyonhotties|colorclimax|couplescinema|sperma-studio|asiansexdiary|virginmassage|loan4k|xillimite|exploitedcollegegirls|mywifesmom|clubnewcity|germangoogirls|cuckoldmilf|dirtyflix|anilos|msparisandfriends|mariskax|virtualtaboo|blackambush|ultrafilms|allcelebs|zerotolerance|houseofyre|beate-uhse-movie|familysexmassage|sarajay|teenpies|privateblack|horrorporn|pornovrai|tutor4k|grandparentsx|tabooheat|naughtymidwestgirlsxxx|affect3dnetwork|latinafucktour|tripforfuck|anyporn|katestube|celebpornarchive|mysexylily|czechwifeswap|casualteensex|teendreams|facefucktour|mycuteasian|realgangbangs|allinternal|wankz|vipissy|realcouples|mandyflores|czechvr|whoresinpublic|trickery|swingingbicouples|handdomination|teenmegaworld|shoplyftermylf|best-datingclub|deeptaboo|goldenslut|4porn|iceporn|tonicmovies|tubexxxx|jizzbunker|analdin|myretrotube|rulertube|afrosex|spicybigtits|titshits|largepornfilms|newmatures|handjobhub|gifgoo|pornaddik|dropyourload|jerkmatelive|hclips|bangher|toppornsites|cfnmteens|freeusemilf|nichepornsites|tsvirtuallovers|mybigtitsbabes|nudegirlsalert|boobsrealm|thelivesexcams|xlviiirdr|wehateporn|realitylovers|iporntoo|hentaizilla|uhairy|pervtherapy|blowjobit|nakedsword|superbe|upornia|amateur8|hsrvv|xnxxporn|lushely|xxxshake|petite18|pornpetite|viptube|yeptube|zbporn|pornicom|4kporn|womenforlove|hdsex|tubent|wildwildvids|pornmist|finalteens|daftsex|shemalez|thegay|see.xxx|tporn|voyeurhit|mediafire|vk.com|xvideos|nuvid|pornerbros|spankwire|sunporn|alphaporno|xtube|pornoxo|tnaflix|pornsharia|extremetube|slutload|empflix|alotporn|xxxbunker|madthumbs|dateadvisor|pornhost|fux|gettranny|bellesa|stasyq|thechive|stufferdb|nakednews|barelist|erotik|vrporn|hd-easyporn|palmtube|pornoflix|gimmeporn|bitporno|pornwiss|thepervs|tube.perverzija|videosection|ahmovs|bravoteens|gotporn|pornid|fapvidhd|keekass|bestandfree|21sextreme|fetishshrine|bestday2love|moviefap|hellmoms|porn-plus|zedporn|porcore|gamcore|superchat.live|pornnut|uncams|tokyoteenies|jsexnetwork|alljapanesepass|milf300|milfporn8|grannymommy|milffox|olderwanker|milfmovs|8teenxxx|nudeamateurgirls|thotsgirls|transangels|weliketosuck|puffynetwork|pornshare|xtapes|fuck55|fap18|tubebrother|goaserv|rule34hentai|pornbraze|xraws|twistedporn|ceskeporno|liztube|traporn|xpaja|xnalgas|xleche|xorgasmo|lechetube|genaporn|clicporn|ltnpornlist|petitepov|vagina.nl|localmeetut|singleflirt|moozporn|sanktor|hentaisea|sharkyporn|amateurporn|pornsamurai|livenude|darmowesexkamerki|fuckass|bdsm365|onstreams|pornhost|megacams|milffinder|linkr|kissuz|sexei|bumsfilme|hornybitches|homemade-clips|taschengeld|data-load|creepshots|wankmaterial|doseofporn|gallery-dump|duckgay|bromonetwork|fuckamilf|zoompussy|therapyporn|fappercams|superheroinejav|ozporno|sexpin|booru|trannylivecams|tophentaicomics|lushstories|solotouch|bongacash|xwebcams|gammastats|fantasymassage|24porn|teen-tube-19|18teen-tube|18-teen-sex|sexbombo|jerkorama|xxxtube2022|flirtymania|lustxtube|esexxxx|lonelywife|lonelywifehookup|milfaholic|smutcam|jizzroulette|eharmony|userscloud|fullxh|pornovore|bitporno|torrentfunk|yourbittorrent|yourbittorrent2|mp4upload|cutebabe|theporngod|coomer|skipthegames|topescortbabes|t-escorts|888companions|myescort|trans-escorts|xescorthub|smooci|adultlook|lovehub|newzealandgirls|heredatesites|comewithdaddy|smartsecuredt|banglachotigram|tubesafari|naturalistsbumpmystic|zippyshare|mediafire|hamsterix|perfektdamen|porndig|sexu|pussyspace|vivud|shorte|clips4sale|pornomico|tabooporn|newbienudes|recurbate|innocentvagina|yourdoll|jsdolls|acsexdolls|sexysexdoll|sexyrealsexdolls|sexmachine|joylovedolls|shemalehd|anyshemale|meetwives|findafuckbuddy|pornheed|pornrabbit|pornwhite|pornmaki|tabootube|onlytaboo|milfzr|thepornblender|mylf|glamourtits|momzr|voyeurpapa|erofus|darknessporn|crocotube|porndoe|xxxcomics|exoav|pornmemo|taiav|mysexgames|stripparadise|glamourtits|sexmummy|buondua|avgle|gay0day|lewdgamer|deviants|javgg|flyingjizz|instantfap|pornvalleymedia|hwcdn|momsteachsex|bdsmstreak|hcbdsm|escortguide|veporno|tubeteencam|pornedup|vipergirls|arabysex|realdoll|hqcollect|tastyblacks|cnnamado|xnalgas|xorgasmo|shockingmovies|eroticmonkey|slavestube|myfreecams|theleaksbay|xlivrdr|yourdailypornvideos|babestare|watchporn|exploitedteens|camfoxe|elitebabes|viewgals|yespornpics|babesource|wetgif|porngifs|porngifmag|filmnudes|glambabesblog|blovjobs|vanillababes|supremebabes|bdsmgifer|londonpussy|muchfap|boobshere|pornzog|manysex|onlyfans|thepornmap|rabbitscams|jerkmate|amatporn|cam69|anacams|channelerotica|nudelive|flirtyones|transflix|shemaleporntube|tpornstars|sheflix|transpornsites|trannytube|youtrannytube|spicytrannyhd|fulltrannytube|gaymaletube|camsfinder|sexstoriespost|nubilefilms|vipwank.com|g2fame|adultempire|homepornking|vrbangers|asiansex|hotebonytube|ebonygalore|ghettotube|sexlikereal|blackmilftube|pornsos|ozeex|meetmindful|refinery29|forhertube|realgirlsonly|vidmixxx|pornimigur|sendnudeselfie|gofucknow|porngipfy|xgifer|ovelycosplay|pierbabes|onlyhcore|hentaicentro|hentai.xxx|spizcash|realsensual|firstclasspov|rawattack|mrluckyvip|pinkocash|mrskincash|porntourist|maturevan|unlimitedmilfs|porndish|inporn|crackshash|sexvideos|adultcomixxx|livesexasian|camclips|swift4claim|1337x.to|javbangers|camwhoresbay|porntrex|netfapx|shortenbuddy|javhdporn|blowxtube|adultprime|titfap|pornrewind|yespornplease|tubxporn|yasying|javbobo|tik.porn|xfree|xxxtik|pornkai|babesandstars|dbnaked|cnnamador|smutr|arrechote|faapy|pornbaker|wankflix|xzorra|igporn|wetsins|pornmeka|fliporno|drporntube|zigtube|pornhat|ultrahorny|foxtube|tubehall|fapbraze|viralpornhub|severeporn|eroasmr|chatsex|rabbitsreviews|tiktok\b|tinychat|pornxp|javdaddy|getsex|porngo|porn13|suicidegirls|pichunter|nakedpornpics|juicysexstories|conlysexstories|punishworld|lesbify|leslez|milfslesbian|amateurcool|entensity|pornmate|swame|babesaround|bestbritishbabes|betmgm|pixbet|betano|bet365|leaktape|nothingtoxic|hornybutt|daftporn|escortnews|cartelmarket|maturetube|xcafe|ukrainebrides4you|reallifecam|xgroovy|kommons|escortsandbabes|xfeed|cambash|taboostepmom|over40handjobs|wtfpeople|mypornhere|yourporndump|theomegaproject|istripper|camiplay|secretfriends|sugarbounce|sexier|baddaddypov|fiqfuq|onlytik|xfree|tiktits|xxxbule|delightdate|loveme1|pictwits|juicygirls|feelfllirty|pornklout|onlyrizz|1024tera|hotcoin|xhamsterlive|cam4free|freelocalsex|amateurest|fakku|pornito|xxxfollow|xfollowcams|livehdcams|youjizzlive|bubbleclips|streamray|camvoice|instachatrooms|fruzo|chatville|joyclub|onlyfinder|loyalfans|meetzur|nurulive|camstreams|bimbim|olecams|tokenfox|camdolls|chatzy|superips|urporn|socialmediagirls|hotcoin|aznude|cooch|xxvidsx|ipuss|pornspan|xcum|pornlib|pdcams|porndex|fullpornvideos|dinotube|latingalore|modelgalore|metaporn|assoass|sambaporno|el-ladies|analgalore|asiangalore|vrxxx|muycerdas|hubit|shemalestube|shemaleleaks|trannyvideosxxx|ashemaletube|celebmasta|nudogram|javfinder|kissjav|javmost|onlyincestporn|incestporn|evilx|findhername|thottok|coomer|voyeurflash|simpcity|internetchicks|mangoporn|ruleporn|hotscope|thisvid|adultdeepfakes|deepfucks|sexystars|desifakes|famousboard|footstockings|tubepornclassic|amateurcool|realgfporn|warddogs|xcums|lecoinporno|reddxxx|javpub|americass|fuckmeets|saveporn|asstraffic|bdsmx.tube|getallmylink|bet365|williamhill|ladbrokes|paddypower|betfair|unibet|888sport|betvictor|coral|skybet|betway|10bet|gentingcasino|sportingbet|marathonbet|188bet|sbobet|dafabet|12bet|fun88|bwin|partypoker|interwetten|tipico|betclic|expekt|bet-at-home|mybet|comeon|leovegas|royalpanda|32red|guts|rizk|casumo|karamba|energybet|lvbet|fonbet|betfred|totesport|boylesports|betbright|sportpesa|betstars|betsson|nordicbet|betsafe|betser|bethard|cashpoint|digibet|favbet|forzza|goalbet|harrys|heyspin|hopa|jackpotcity|jetbull|lsbet|mansionbet|matchbook|megapari|melbet|meridianbet|mobilbet|mrplay|netbet|noxwin|optibet|pinnacle|planetwin365|redbet|redstar|reloadbet|royalbet|sbobet|scandibet|sportium|sportsbet|superlenny|svenskaspel|tipbet|tonybet|tornadobet|vbet|vernons|vitalbet|volcanobet|w88|wanabet|westcasino|winmasters|winnings|wunderino|xtip|youwin|zebet|zodiacbet|1xbet|22bet|888casino|energypoker|loyalfans|sinparty|21sextury|gptgirlfriend|shameless|dansmovies"

    message = f"Bad domain detected."
    code = "invalid domain"
    inverse_match = True
    flags = re.IGNORECASE


@deconstructible
class OffensiveWordsValidator(RegexValidator):
    ''' do not put | at the end of last word 

        this validator will match any word that 
        is the word itself or any other word that contains 
        the word itself

        words here has to be exact

        # anal\b will match anal
        # will not match analytics
        # ^gay\b        
    '''
    OFFENSIVE_WORDS = [
        "creampie", "cuckold", "vulva", "cunnilingus", "lovegoo", "lovebone", "lovegun",
        "pussy", "milf", "jizz", "pussies", "ebony", "prostitute", "bukkake", "vagina", "dildo",
        "sodomize", "dyke", "nipple", "masturbate", "skank", "morgue", "stripper", "lolita",
        "cameltoe", "queer", "incest", "feces", "rimjob", "shemale", "fisting", "footjob",
        "cocaine", "rectal", "rapist", "genitals", "scrotum", "jihad", "lapdance", "squirt",
        "gangbang", "ladyboy", "spunk", "bestiality", "playboy", "crossdressing", "femdom",
        "mistress", "missionary", "cumshot", "tranny", "yellowshower", "enema", "excrement",
        "fellatio", "heroin", "camshow", "choking", "porn", "masochist", "queef", "coprophilia",
        "hermaphrodite", "sleezebag", "sleezeball", "shagging", "clamdiver", "defecate",
        "holestuffer", "jizzjuice", "lactate", "lovemuscle", "lovepistol", "sissi", "femboy",
        "twat", "prolapse", "orgasm", "gagging", "pedophile", "dominatrix", "gloryhole", "smegma",
        "suicide", "futanari", "jugs", "nutsack", "titty", "tgirl", "brothel", "ejaculate", "slut",
        "shitter", "shitting", "shitstain", "skinflute", "swingers", "handjob", "nudity",
        "dragqueen", "twerk", "lesbian", "masturbating", "whore", "striptease", "farting", "asshole", "arsehole", "bastard", "horseshit", "dickhead", "wanker", "punani", "minge", "bisexual", "transgender", "transgendered", "bareback", "homosexual", "voyeurism", "pedophilia", "sex", r"pu\$\$y"
    ]
    regex = r"\b(" + "|".join(OFFENSIVE_WORDS) + r")\b"
    message = f"Do not use offensive word(s)."
    code = "invalid word"
    inverse_match = True
    flags = re.IGNORECASE