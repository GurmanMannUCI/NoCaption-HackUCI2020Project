import json

#Stopwords added in, so they dont appear in any of the indexed dictionairies
stopwords = {"a","about","above","after","again","against","all","am","an","and",
            "any","are","arent","as","at","be","because","been","before","being",
             "below","between","both","but","by","cant","cannot","could","couldnt",
             "did","didnt","do","does","doesnt","doing","dont","down","during",
            "each","few","for","from","further","had","hadnt","has","hasnt","have",
            "havent","having","he","hed","hes","her","here","heres","hers",
            "herself","him","himself","his","how","hows","i","id","ill","im","ive",
            "if","in","into","is","isnt","it","its","its","itself","know","lets","me","more",
            "most","mustnt","my","myself","no","nor","not","of","on","only",
            "or","other","ought","our","ours", "ourselves","out","over","own","same",
            "shant","she","shed","shell","shes","should","shouldnt","so","some","such",
            "than","that","thats","the","their","theirs","them","themselves","then","there",
            "theres","these","they","theyd","theyll","theyre","theyve","this","those","through",
            "to","too","under","until","very","was","wasnt","we","wed","well","were",
            "weve","were","werent","what","whats","when","whens","where","wheres","which",
            "while","who","whos","whom","why","whys","with","wont","would","wouldnt","you",
            "youd","youll","youre","youve","your","yours","yourself","yourselves"}

global maindict
global wordindex

def Loader():
    '''Loads in the main dictionairy holding in all the lyrics as well as the word index which showed where they are located'''
    try:
        global maindict
        maindict = json.load(open("masterfile.txt"))
    except:
        maindict = {}
        pass
    try:
        global wordindex
        wordindex = json.load(open("WordIndex.txt"))
    except:
        wordindex = {}
        pass

#Scores for each artist based on their popularity. highest score is .2 and lowest is .1
artistscores = {"Eminem" : 0.2,"Roddy Ricch" : 0.199742,"Marshmello & Roddy Ricch" : 0.199485,"Drake" : 0.199229,"Mac Miller" : 0.198974,"Post Malone" : 0.198719,"Post Malone & Swae Lee" : 0.198465,"G-Eazy & Halsey" : 0.198212,"Halsey" : 0.197959,"benny blanco, Halsey & Khalid" : 0.197707,"YoungBoy Never Broke Again" : 0.197455,
"Juice WRLD & YoungBoy Never Broke Again" : 0.197204,"DaBaby" : 0.196954,"Quality Control, Lil Baby & DaBaby" : 0.196704,"Juice WRLD" : 0.196455,"Lil Tecca & Juice WRLD" : 0.196207,"Future" : 0.195959,"Drake & Future" : 0.195712,"Odd Future" : 0.195465,"Jay Rock, Kendrick Lamar, Future & James Blake" : 0.195220,"Billie Eilish & Khalid" : 0.194974,
"Billie Eilish" : 0.194730,"Trippie Redd" : 0.194486,"Trippie Redd & 6ix9ine" : 0.194242,"Kris Wu, Rich Brian, Joji, Trippie Redd & Baauer" : 0.193999,"XXXTENTACION" : 0.193757,"Moneybagg Yo" : 0.193516,"Moneybagg Yo & Yo Gotti" : 0.193275,"Moneybagg Yo & Megan Thee Stallion" : 0.193034,"Lil Baby & Drake" : 0.192795,"Ski Mask the Slump God" : 0.192555,
"Lil Baby & Gunna" : 0.192317,"Lil Baby" : 0.192079,"Taylor Swift" : 0.191841,"ZAYN & Taylor Swift" : 0.191604,"The Weeknd" : 0.191368,"YNW Melly" : 0.191133,"Young Thug & Travis Scott" : 0.190897,"Young Thug" : 0.190663,"Young Thug & Rich Homie Quan" : 0.190429,"Rod Wave" : 0.190196,
"Lil Uzi Vert" : 0.189963,"Kygo & Selena Gomez" : 0.189731,"Selena Gomez" : 0.189499,"Selena Gomez & Marshmello" : 0.189268,"Luke Combs" : 0.189037,"Travis Scott" : 0.188807,"Kanye West" : 0.188578,"JAY-Z & Kanye West" : 0.188349,"Kanye West, JAY-Z & Big Sean" : 0.188121,"Lil Pump & Kanye West" : 0.187893,
"Khalid" : 0.187666,"Khalid & Normani" : 0.187439,"Harry Styles" : 0.187213,"Chris Brown" : 0.186987,"Chris Brown & Tyga" : 0.186762,"Joyner Lucas & Chris Brown" : 0.186538,"Ariana Grande" : 0.186314,"Ed Sheeran" : 0.186091,"Ed Sheeran & Beyonce" : 0.185868,"Ed Sheeran & Justin Bieber" : 0.185645,
"J. Cole" : 0.185424,"The Beatles" : 0.185202,"Kevin Gates" : 0.184982,"A Boogie Wit da Hoodie" : 0.184761,"Maroon 5" : 0.184542,"NLE Choppa" : 0.184323,"Kendrick Lamar" : 0.184104,"Jhené Aiko" : 0.183886,"Beyoncé" : 0.183668,"THE CARTERS" : 0.183451,
"Kodak Black" : 0.183234,"Gucci Mane, Bruno Mars & Kodak Black" : 0.183018,"Lil Wayne" : 0.182803,"Nicki Minaj, Drake & Lil Wayne" : 0.182588,"Drake, Kanye West, Lil Wayne & Eminem" : 0.182373,"Lil Wayne, Wiz Khalifa, Imagine Dragons, Logic & Ty Dolla $ign" : 0.182159,"Jonas Brothers" : 0.181946,"Summer Walker" : 0.181733,"Summer Walker & Drake" : 0.181520,"Summer Walker, London on da Track & Chris Brown" : 0.181308,
"Imagine Dragons" : 0.181096,"Justin Bieber" : 0.180885,"Justin Bieber & BloodPop®" : 0.180675,"Dan + Shay & Justin Bieber" : 0.180465,"Jason Aldean" : 0.180255,"Lewis Capaldi" : 0.180046,"Rihanna" : 0.179837,"Rihanna, Kanye West & Paul McCartney" : 0.179629,"N.E.R.D & Rihanna" : 0.179421,"Lizzo" : 0.179214,
"Arizona Zervas" : 0.179008,"Meek Mill" : 0.178801,"​blackbear" : 0.178596,"​blackbear & FRND" : 0.178390,"Doja Cat" : 0.178185,"Panic! at the Disco" : 0.177981,"​hamperedoutkast" : 0.177777,"JACKBOYS, Pop Smoke & Travis Scott" : 0.177574,"TrappaChiNo" : 0.177371,"​ibmac26" : 0.177168,
"JACKBOYS" : 0.176966,"Lil Tecca" : 0.176765,"Internet Money, Lil Tecca & A Boogie Wit da Hoodie" : 0.176564,"Camila Cabello" : 0.176363,"Machine Gun Kelly & Camila Cabello" : 0.176163,"Shawn Mendes & Camila Cabello" : 0.175963,"Camila Cabello & Daddy Yankee" : 0.175764,"Frank Ocean" : 0.175565,"Stunna 4 Vegas" : 0.175367,"Stunna 4 Vegas & Offset" : 0.175169,
"Queen" : 0.174971,"Fetty Wap" : 0.174774,"Queen Naija" : 0.174578,"Mustard" : 0.174382,"Mustard & Migos" : 0.174186,"Yellow Claw & Mustard" : 0.173991,"Tyler, The Creator" : 0.173796,"Kane Brown" : 0.173601,"Marshmello & Kane Brown" : 0.173407,"Kane Brown & Becky G" : 0.173214,
"Lil Dicky" : 0.173021,"Ol’ Dirty Bastard" : 0.172828,"Luke Bryan" : 0.172636,"BROCKHAMPTON" : 0.172444,"Quando Rondo" : 0.172253,"Cardi B, Bad Bunny & J Balvin" : 0.172062,"Nio García, Casper Mágico & Bad Bunny" : 0.171871,"Bad Bunny" : 0.171681,"Khea & Bad Bunny" : 0.171491,"Rvssian, Farruko & Bad Bunny" : 0.171302,
"Jhay Cortez, J Balvin & Bad Bunny" : 0.171113,"Bruno Mars" : 0.170925,"Cardi B & Bruno Mars" : 0.170737,"​twenty one pilots" : 0.170549,"Thomas Rhett" : 0.170362,"6ix9ine" : 0.170175,"Alessia Cara" : 0.169989,"Pink Floyd" : 0.169803,"Polo G" : 0.169617,"Dark Polo Gang" : 0.169432,
"Tones and I" : 0.169247,"Tory Lanez" : 0.169063,"Tory Lanez & Rich The Kid" : 0.168879,"Cashmere Cat, Major Lazer & Tory Lanez" : 0.168695,"Logic" : 0.168512,"Blake Shelton" : 0.168329,"Gucci Mane" : 0.168147,"Gucci Mane & Nicki Minaj" : 0.167965,"Don Toliver" : 0.167783,"$UICIDEBOY$" : 0.167602,
"$UICIDEBOY$ & Pouya" : 0.167421,"Florida Georgia Line" : 0.167241,"21 Savage & Metro Boomin" : 0.167061,"21 Savage" : 0.166881,"21 Savage, Offset & Metro Boomin" : 0.166702,"Migos" : 0.166523,"Migos, Nicki Minaj & Cardi B" : 0.166345,"Lil Skies" : 0.166167,"Calvin Harris & Sam Smith" : 0.165989,"Dreamville, Bas & JID" : 0.165811,
"Dreamville, J. Cole & Lute" : 0.165635,"Dreamville" : 0.165458,"Dreamville, EARTHGANG & J. Cole" : 0.165282,"Dreamville, JID & EARTHGANG" : 0.165106,"Dreamville, J. Cole, JID, Cozz & EARTHGANG" : 0.164930,"Dreamville & Cozz" : 0.164755,"Dreamville & J. Cole" : 0.164581,"Dreamville, JID & J. Cole" : 0.164406,"Morgan Wallen" : 0.164232,"Lil Peep" : 0.164059,
"Lil Peep & XXXTENTACION" : 0.163885,"Lil Peep & Lil Tracy" : 0.163713,"Marshmello & Lil Peep" : 0.163540,"Chance the Rapper" : 0.163368,"Dan + Shay" : 0.163196,"Dua Lipa" : 0.163025,"Martin Garrix & Dua Lipa" : 0.162854,"Calvin Harris & Dua Lipa" : 0.162683,"Dua Lipa & BLACKPINK" : 0.162513,"Silk City & Dua Lipa" : 0.162343,
"The Chainsmokers & Coldplay" : 0.162173,"Coldplay" : 0.162004,"Shawn Mendes" : 0.161835,"Playboi Carti" : 0.161666,"Lil Mosey" : 0.161498,"Lil Mosey & Chris Brown" : 0.161330,"Nipsey Hussle" : 0.161163,"Natanael Cano & Bad Bunny" : 0.160995,"Natanael Cano, Junior H & Dan Sanchez" : 0.160829,"Natanael Cano" : 0.160662,
"Bazzi" : 0.160496,"Trevor Daniel" : 0.160330,"Trevor Daniel & blackbear" : 0.160165,"Lil Nas X" : 0.16,"Lil Nas X & Cardi B" : 0.159835,"Ozuna" : 0.159670,"Chris Jeday, J Balvin & Ozuna" : 0.159506,"ROSALÍA & Ozuna" : 0.159342,"Ozuna, Mambo Kingz & DJ Luian" : 0.159179,"Sech, Ozuna & Anuel AA" : 0.159016,
"Lana Del Rey" : 0.158853,"Ariana Grande, Miley Cyrus & Lana Del Rey" : 0.158691,"2Pac" : 0.158529,"Sam Hunt" : 0.158367,"Gunna" : 0.158205,"Lil Baby, Gunna & Drake" : 0.158044,"Megan Thee Stallion" : 0.157884,"Megan Thee Stallion & VickeeLo" : 0.157723,"Zedd, Maren Morris & Grey" : 0.157563,"Maren Morris" : 0.157403,
"Niall Horan & Maren Morris" : 0.157244,"John Mayer" : 0.157085,"Nicki Minaj" : 0.156926,"Adele" : 0.156767,"Melanie Martinez" : 0.156609,"Old Dominion" : 0.156451,"Linkin Park" : 0.156294,"Jay-Z & Linkin Park" : 0.156136,"One Direction" : 0.155979,"Rich The Kid" : 0.155823,
"Migos & Rich the Kid" : 0.155667,"Dustin Lynch" : 0.155511,"George Strait" : 0.155355,"Fleetwood Mac" : 0.1552,"Elton John" : 0.155044,"Elton John & Kiki Dee" : 0.154890,"Michael Jackson" : 0.154735,"Drake & Michael Jackson" : 0.154581,"Red Hot Chili Peppers" : 0.154427,"A$AP Rocky" : 0.154274,
"Metallica" : 0.154121,"TACONAFIDE" : 0.153968,"Lil Durk" : 0.153815,"Chris Stapleton" : 0.153663,"Ed Sheeran, Chris Stapleton & Bruno Mars" : 0.153511,"Wiz Khalifa" : 0.153359,"2 Chainz & Wiz Khalifa" : 0.153208,"Snoop Dogg & Wiz Khalifa" : 0.153057,"Five Finger Death Punch" : 0.152906,"AC/DC" : 0.152755,
"The Chainsmokers" : 0.152605,"The Chainsmokers & 5 Seconds of Summer" : 0.152455,"Green Day" : 0.152306,"Kehlani" : 0.152156,"G-Eazy & Kehlani" : 0.152007,"PARTYNEXTDOOR" : 0.151859,"Jon Pardi" : 0.151710,"Lady Gaga & Bradley Cooper" : 0.151562,"Lady Gaga" : 0.151414,"Eric Church" : 0.151267,
"JayDaYoungan" : 0.151119,"JAY-Z" : 0.150972,"Usher" : 0.150826,"Frank Sinatra" : 0.150679,"Wale" : 0.150533,"Kenny Chesney" : 0.150387,"DJ Khaled" : 0.150242,"Kanye West & DJ Khaled" : 0.150096,"Cardi B" : 0.149951,"Blueface" : 0.149806,
"Eagles" : 0.149662,"G-Eazy & Bebe Rexha" : 0.149518,"G-Eazy" : 0.149374,"​The Lumineers" : 0.149230,"Katy Perry" : 0.149087,"Bryson Tiller" : 0.148944,"Lauren Daigle" : 0.148801,"Led Zeppelin" : 0.148659,"Tee Grizzley" : 0.148516,"5 Seconds of Summer" : 0.148374,
"Tame Impala" : 0.148233,"Pink Guy" : 0.148091,"P!nk" : 0.147950,"LANY" : 0.147809,"Machine Gun Kelly" : 0.147668,"Machine Gun Kelly, X Ambassadors & Bebe Rexha" : 0.147528,"Machine Gun Kelly, YUNGBLUD & Travis Barker" : 0.147388,"Rex Orange County" : 0.147248,"Fall Out Boy" : 0.147109,"Alec Benjamin" : 0.146969,
"Joji" : 0.146830,"Joji, Rich Brian, Higher Brothers & AUGUST 08" : 0.146691,"Childish Gambino" : 0.146553,"Lauv" : 0.146415,"Lauv & Troye Sivan" : 0.146277,"DJ Snake & Lauv" : 0.146139,"Lauv & LANY" : 0.146001,"The Rolling Stones" : 0.145864,"Zac Brown Band" : 0.145727,"Big Sean" : 0.145590,
"Kanye West, Chief Keef, Pusha T, Big Sean & Jadakiss" : 0.145454,"2 Chainz" : 0.145318,"ScHoolboy Q, 2 Chainz & Saudi" : 0.145182,"Kanye West, Pusha T, Common, 2 Chainz, CyHi The Prynce, Kid Cudi & D’Banj" : 0.145046,"Billy Joel" : 0.144911,"The Notorious B.I.G." : 0.144776,"Carrie Underwood" : 0.144641,"Kid Cudi" : 0.144506,"KIDS SEE GHOSTS" : 0.144372,"YG" : 0.144237,
"Cardi B & YG" : 0.144103,"Shoreline Mafia" : 0.143970,"Brett Young" : 0.143836,"Tyga" : 0.143703,"Tyga & Nicki Minaj" : 0.143570,"Trey Songz" : 0.143438,"Tim McGraw" : 0.143305,"Tim McGraw & Faith Hill" : 0.143173,"Ella Mai" : 0.143041,"Ella Mai, Nicki Minaj & Quavo" : 0.142909,
"Pop Smoke" : 0.142778,"NAV" : 0.142647,"NAV & Metro Boomin" : 0.142516,"Tom Petty and the Heartbreakers" : 0.142385,"Jack & Jack" : 0.142254,"Jack Johnson" : 0.142124,"Lady Antebellum" : 0.141994,"Nirvana" : 0.141864,"The 1975" : 0.141735,"Kacey Musgraves" : 0.141605,
"Rick Ross" : 0.141476,"Skrillex & Rick Ross" : 0.141347,"OneRepublic" : 0.141219,"OneRepublic & Seeb" : 0.141090,"Miley Cyrus" : 0.140962,"​​blink-182" : 0.140834,"​iann dior" : 0.140707,"PnB Rock" : 0.140579,"PnB Rock, Kodak Black & Boogie Wit Da Hoodie" : 0.140452,"Young Thug, 2 Chainz, Wiz Khalifa & PnB Rock" : 0.140325,
"PnB Rock & XXXTENTACION" : 0.140198,"Miranda Lambert" : 0.140072,"Demi Lovato" : 0.139945,"Luis Fonsi & Demi Lovato" : 0.139819,"Jacquees" : 0.139693,"Jacquees & DeJ Loaf" : 0.139568,"Alicia Keys" : 0.139442,"Shinedown" : 0.139317,"Slipknot" : 0.139192,"Hozier" : 0.139068,
"Hillsong Worship" : 0.138943,"50 Cent" : 0.138819,"Skrillex, Justin Bieber & Diplo" : 0.138695,"Diplo" : 0.138571,"Ellie Goulding & Diplo" : 0.138447,"The Diplomats" : 0.138324,"Jack Ü" : 0.138201,"Fabolous" : 0.138078,"Justin Timberlake" : 0.137955,"Calvin Harris" : 0.137833,
"YFN Lucci" : 0.137710,"Tyler Childers" : 0.137588,"Chris Young" : 0.137466,"Mariah Carey" : 0.137345,"Three Days Grace" : 0.137223,"Elvis Presley" : 0.137102,"My Chemical Romance" : 0.136981,"Keith Urban" : 0.136860,"Miguel" : 0.136740,"Miky Woodz" : 0.136619,
"Johnny Cash" : 0.136499,"Yelawolf" : 0.136379,"6LACK" : 0.136259,"Jessie Reyez & 6LACK" : 0.136140,"Hillsong UNITED" : 0.136021,"Little Big Town" : 0.135901,"Idina Menzel & Evan Rachel Wood" : 0.135783,"Idina Menzel" : 0.135664,"Idina Menzel & AURORA" : 0.135545,"Kristen Bell & Idina Menzel" : 0.135427,
"Josh Gad, Kristen Bell, Idina Menzel, Jonathan Groff & Cast of Frozen II" : 0.135309,"Disturbed" : 0.135191,"Kelsea Ballerini" : 0.135073,"Dierks Bentley" : 0.134956,"Jeremih" : 0.134839,"Jeremih & Chance The Rapper" : 0.134722,"Breaking Benjamin" : 0.134605,"Conan Gray" : 0.134488,"Journey" : 0.134372,"Oxxxymiron" : 0.134256,
"John Legend" : 0.134140,"Ariana Grande & John Legend" : 0.134024,"John Legend, Teyana Taylor, CyHi The Prynce & Malik Yusef" : 0.133908,"John Legend & Teyana Taylor" : 0.133793,"Daniel Caesar" : 0.133677,"Chelsea Cutler" : 0.133562,"Jeremy Zucker & Chelsea Cutler" : 0.133447,"Kygo & Chelsea Cutler" : 0.133333,"Flipp Dinero" : 0.133218,"Tool" : 0.133104,
"Key Glock" : 0.132990,"Weezer" : 0.132876,"Offset & Metro Boomin" : 0.132763,"Metro Boomin" : 0.132649,"Big Sean & Metro Boomin" : 0.132536,"Guns N’ Roses" : 0.132423,"G Herbo" : 0.132310,"French Montana" : 0.132197,"Marshmello & Anne-Marie" : 0.132085,"Marshmello & Bastille" : 0.131972,
"Marshmello" : 0.131860,"Logic & Marshmello" : 0.131748,"Migos & Marshmello" : 0.131636,"Far East Movement & Marshmello" : 0.131525,"Baby Keem" : 0.131414,"Avicii" : 0.131302,"Desiigner" : 0.131191,"ZAYN" : 0.131081,"T.I." : 0.130970,"Lorde" : 0.130860,
"Martin Garrix & Bebe Rexha" : 0.130749,"Bebe Rexha" : 0.130639,"David Guetta, Bebe Rexha & J Balvin" : 0.130529,"Why Don’t We" : 0.130420,"Why Don’t We & Macklemore" : 0.130310,"Kesha" : 0.130201,"Pitbull & Kesha" : 0.130092,"Jeezy" : 0.129983,"Dan Bull" : 0.129874,"Cassidy" : 0.129765,
"Trev Rich" : 0.129657,"Novelist" : 0.129549,"SMACKTOWN" : 0.129441,"DINAS" : 0.129333,"Rascal Flatts" : 0.129225,"Paramore" : 0.129118,"Pearl Jam" : 0.129010,"Lil Yachty" : 0.128903,"Classical Lullabies" : 0.128796,"Meghan Trainor" : 0.128689,
"CNCO, Meghan Trainor & Sean Paul" : 0.128583,"Sigala, Ella Eyre & Meghan Trainor" : 0.128476,"Niall Horan" : 0.128370,"Big Time Rush" : 0.128264,"Rush" : 0.128158,"William Singe" : 0.128052,"Aerosmith" : 0.127947,"K CAMP" : 0.127841,"Cage The Elephant" : 0.127736,"Upchurch" : 0.127631,
"Chief Keef" : 0.127526,"SZA" : 0.127422,"Kendrick Lamar & SZA" : 0.127317,"Michael Bublé" : 0.127213,"Alan Jackson" : 0.127108,"Lynyrd Skynyrd" : 0.127004,"The Game" : 0.126901,"Luis Fonsi & Daddy Yankee" : 0.126797,"Daddy Yankee" : 0.126693,"Lunay, Daddy Yankee & Bad Bunny" : 0.126590,
"Ozuna, Daddy Yankee & J Balvin" : 0.126487,"Anuel AA, Daddy Yankee & Karol G" : 0.126384,"Avenged Sevenfold" : 0.126281,"Cody Johnson" : 0.126178,"Skillet" : 0.126076,"Sia" : 0.125974,"Sivas" : 0.125871,"Gims" : 0.125769,"Mumford & Sons" : 0.125668,"Young Dolph" : 0.125566,
"Garth Brooks" : 0.125464,"OutKast" : 0.125363,"Sublime" : 0.125262,"Aventura" : 0.125161,"Lunay, Ozuna & Anuel AA" : 0.125060,"Charlie Puth" : 0.124959,"Lil Wayne & Charlie Puth" : 0.124859,"Britney Spears" : 0.124758,"Gorillaz" : 0.124658,"Romeo Santos" : 0.124558,
"Anuel AA & Romeo Santos" : 0.124458,"Shakira" : 0.124358,"Carlos Vives & Shakira" : 0.124259,"Prince Royce & Shakira" : 0.124159,"Brantley Gilbert" : 0.124060,"T-Pain" : 0.123961,"Pusha T" : 0.123862,"Tory Lanez & T-Pain" : 0.123763,"Lee Brice" : 0.123665,"Kelly Clarkson" : 0.123566,
"System of a Down" : 0.123468,"Ali Gatie" : 0.123370,"J Balvin & Willy William" : 0.123272,"Nicky Jam & J Balvin" : 0.123174,"J Balvin" : 0.123076,"Bad Bunny, Prince Royce & J Balvin" : 0.122979,"Rae Sremmurd" : 0.122882,"Radiohead" : 0.122784,"TOKYO’S REVENGE" : 0.122687,"TOKYO’S REVENGE & ZEDSU" : 0.122590,
"Joey Trap & Tokyo’s Revenge" : 0.122494,"Clairo" : 0.122397,"Cuco & Clairo" : 0.122301,"Tech N9ne" : 0.122204,"CUCO" : 0.122108,"Brooks & Dunn" : 0.122012,"Chris Lane" : 0.121916,"Foo Fighters" : 0.121821,"Stevie Wonder" : 0.121725,"Gabby Barrett" : 0.121630,
"Luh Kel" : 0.121534,"Riley Green" : 0.121439,"Aminé" : 0.121344,"N.W.A" : 0.121250,"Dr. Dre" : 0.121155,"Bob Marley & The Wailers" : 0.121060,"Jason Derulo" : 0.120966,"Jason Derulo & David Guetta" : 0.120872,"Hall & Oates" : 0.120778,"Van Morrison" : 0.120684,
"Korn" : 0.120590,"Nelly" : 0.120496,"Nelly Furtado" : 0.120403,"Fuerza Regida" : 0.120310,"The Killers" : 0.120216,"James TW" : 0.120123,"James Taylor" : 0.120030,"Cole Swindell" : 0.119938,"Calboy" : 0.119845,"Van Halen" : 0.119753,
"Yo Gotti" : 0.119660,"Sleepy John Estes" : 0.119568,"Jackie Greene" : 0.119476,"Arctic Monkeys" : 0.119384,"Joey Bada$$" : 0.119292,"Cassie" : 0.119201,"Rockabye Baby!" : 0.119109,"Curren$y" : 0.119018,"Bruce Springsteen" : 0.118927,"Alan Walker, Noah Cyrus & Digital Farm Animals" : 0.118836,
"Noah Cyrus" : 0.118745,"Noah Cyrus & Lil Xan" : 0.118654,"Noah Cyrus & MAX" : 0.118563,"Noah Cyrus & Tanner Alexander" : 0.118473,"NoCap" : 0.118382,"Future & Young Thug" : 0.118292,"Dree Low & Adel" : 0.118202,"OBLADAET" : 0.118112,"DigDat" : 0.118022,"NoCap & Rylo Rodriguez" : 0.117933,
"Jake Owen" : 0.117843,"Flo Rida" : 0.117754,"Flo Rida & 99 Percent" : 0.117664,"Higher Brothers" : 0.117575,"ScHoolboy Q" : 0.117486,"Young M.A" : 0.117397,"Young Maylay" : 0.117309,"Maluma" : 0.117220,"Sech, Justin Quiles & Maluma" : 0.117132,"Madonna & Maluma" : 0.117043,
"Maluma, Trap Capos & Noriel" : 0.116955,"The Beach Boys" : 0.116867,"Sus Scrofa" : 0.116779,"CashMoneyAP" : 0.116691,"No Rome" : 0.116604,"Cashmo" : 0.116516,"Cody Jinks" : 0.116429,"Casting Crowns" : 0.116341,"Ty Dolla $ign" : 0.116254,"Lil Wayne & Ty Dolla $ign" : 0.116167,
"City Girls" : 0.116080,"Dean Lewis" : 0.115994,"Martin Garrix & Dean Lewis" : 0.115907,"Whitney Houston" : 0.115820,"Bob Dylan" : 0.115734,"Train" : 0.115648,"Ozzy Osbourne" : 0.115562,"Pinkfong" : 0.115476,"Comethazine" : 0.115390,"Comethazine & A$AP Rocky" : 0.115304,
"U2" : 0.115219,"Mert" : 0.115133,"Queen & David Bowie" : 0.115048,"David Bowie" : 0.114962,"A$AP Ferg" : 0.114877,"Bon Jovi" : 0.114792,"Jon Bon Jovi" : 0.114708,"Olivia Rodrigo" : 0.114623,"Olivia Rodrigo & Julia Lester" : 0.114538,"Olivia Rodrigo & Joshua Bassett" : 0.114454,
"Olivia Rodrigo & Matt Cornett" : 0.114369,"Olivia Rodrigo, Joshua Bassett & Matt Cornett" : 0.114285,"Smokepurpp" : 0.114201,"Smokepurpp & Murda Beatz" : 0.114117,"Surfaces" : 0.114033,"Quinn XCII" : 0.113950,"Beyoncé, SAINt JHN & Wizkid" : 0.113866,"SAINt JHN" : 0.113782,"Joyner Lucas" : 0.113699,"The Neighbourhood" : 0.113616,
"Ne-Yo" : 0.113533,"Pitbull & Ne-Yo" : 0.113450,"Ne-Yo, Bebe Rexha & Stefflon Don" : 0.113367,"KYLE" : 0.113284,"Kyle Massey" : 0.113202,"Yung Gravy" : 0.113119,"Yung Gravy & bbno$" : 0.113037,"Ava Max" : 0.112954,"Alan Walker & Ava Max" : 0.112872,"Norah Jones" : 0.112790,
"DaniLeigh" : 0.112708,"ODESZA" : 0.112626,"Hayden James" : 0.112545,"Nickelback" : 0.112463,"Ciara" : 0.112382,"Jon Bellion" : 0.112301,"YBN Cordae" : 0.112219,"YBN Nahmir & YBN Cordae" : 0.112138,"Jordan Davis" : 0.112057,"Lil Keed" : 0.111976,
"Foster the People" : 0.111896,"David Guetta" : 0.111815,"Martin Garrix & David Guetta" : 0.111735,"Sean Paul & David Guetta" : 0.111654,"David Guetta & Sia" : 0.111574,"David Guetta & Afrojack" : 0.111494,"James Arthur" : 0.111414,"James Arthur & Anne-Marie" : 0.111334,"MercyMe" : 0.111254,"Marvin Gaye" : 0.111174,
"B.o.B" : 0.111095,"The Strokes" : 0.111015,"Bryce Vine" : 0.110936,"Loud Luxury & Bryce Vine" : 0.110857,"Saweetie" : 0.110778,"Saweetie & London On Da Track" : 0.110699,"Def Leppard" : 0.110620,"Snoop Dogg" : 0.110541,"JP Saxe" : 0.110462,"JP Saxe & Charlotte Lawrence" : 0.110384,
"Destiny’s Child" : 0.110305,"Vance Joy" : 0.110227,"Godsmack" : 0.110149,"Alice in Chains" : 0.110070,"Toby Keith" : 0.109992,"Major Lazer" : 0.109915,"Major Lazer & DJ Maphorisa" : 0.109837,"Daft Punk" : 0.109759,"Mary J. Blige" : 0.109681,"Andy Grammer" : 0.109604,
"Phil Collins" : 0.109527,"Mitchell Tenpenny" : 0.109449,"Bob Seger" : 0.109372,"Atmosphere" : 0.109295,"Akon" : 0.109218,"Freddie Dredd" : 0.109142,"Billy Currington" : 0.109065,"The Black Keys" : 0.108988,"Mötley Crüe" : 0.108912,"Grateful Dead" : 0.108835,
"Jason Mraz" : 0.108759,"​for KING & COUNTRY" : 0.108683,"YK Osiris" : 0.108607,"Simon & Garfunkel" : 0.108531,"Ruel" : 0.108455,"Ruelle" : 0.108379,"Avril Lavigne" : 0.108304,"Madonna" : 0.108228,"Ernia" : 0.108153,"Lupe Fiasco" : 0.108077,
"The Black Eyed Peas" : 0.108002,"​will.i.am" : 0.107927,"A Day To Remember" : 0.107852,"Marshmello & A Day to Remember" : 0.107777,"R. Kelly" : 0.107702,"Kanye West, R. Kelly & Teyana Taylor" : 0.107628,"Jeremy Zucker" : 0.107553,"Kid Rock" : 0.107479,"BONES" : 0.107404,"24kGoldn" : 0.107330,
"Lisa Loeb & Nine Stories" : 0.107256,"Lisa Loeb" : 0.107182,"Walk off the Earth & Lisa Loeb" : 0.107108,"Offset" : 0.107034,"Yungeen Ace" : 0.106960,"Bee Gees" : 0.106887,"Tove Lo" : 0.106813,"Earth, Wind & Fire" : 0.106740,"Matthew Wilder" : 0.106666,"Chase Rice" : 0.106593,
"Cavetown" : 0.106520,"Ice Cube" : 0.106447,"Julia Michaels" : 0.106374,"LANY & Julia Michaels" : 0.106301,"Maroon 5 & Julia Michaels" : 0.106228,"Beastie Boys" : 0.106155,"Scorpinox" : 0.106083,"Miguel de Unamuno" : 0.106010,"Sene" : 0.105938,"Noam Chomsky" : 0.105866,
"Jeff Le Nerf" : 0.105794,"President Jimmy Carter" : 0.105722,"Zachary Taylor" : 0.105650,"Yung Pinch" : 0.105578,"Christian Nodal" : 0.105506,"Matchbox Twenty" : 0.105434,"Polo G & Lil Tjay" : 0.105363,"Eric Bellinger" : 0.105291,"​TobyMac" : 0.105220,"Lord Huron" : 0.105149,
"Theory" : 0.105077,"Vitamin String Quartet" : 0.105006,"Two Friends" : 0.104935,"Fitz and The Tantrums" : 0.104864,"Calibre 50" : 0.104794,"Chris Tomlin" : 0.104723,"The Doors" : 0.104652,"Mac DeMarco" : 0.104582,"Denzel Curry" : 0.104511,"Brad Paisley" : 0.104441,
"Florence + The Machine" : 0.104371,"Willie Nelson" : 0.104301,"Merle Haggard & Willie Nelson" : 0.104231,"Waylon Jennings & Willie Nelson" : 0.104161,"Willie Nelson & Bobbie Nelson" : 0.104091,"Grupo Firme" : 0.104021,"Expressão Ativa" : 0.103951,"RAPTORS" : 0.103882,"Tede" : 0.103812,"3 Doors Down" : 0.103743,
"I Prevail" : 0.103674,"Seether" : 0.103604,"Dave Matthews Band" : 0.103535,"Young Breezy & RLS" : 0.103466,"$lick Nick & Young Breezy" : 0.103397,"Tulisa" : 0.103328,"Mark Knopfler" : 0.103260,"James Bay" : 0.103191,"Sadek" : 0.103122,"Sade" : 0.103054,
"Justin Moore" : 0.102986,"​gnash" : 0.102917,"T-Wayne" : 0.102849,"Nas" : 0.102781,"Young Stunners" : 0.102713,"​Biosphere" : 0.102645,"Jeff Russo" : 0.102577,"Murray Huggins, Kirk Ross, Brian Tichy & David Delhomme" : 0.102509,"Ellie Goulding" : 0.102442,"Kygo & Ellie Goulding" : 0.102374,
"John Denver" : 0.102307,"Mangaturtle" : 0.102239,"Ant Saunders" : 0.102172,"Ant Saunders & Kiaura Rose" : 0.102105,"Marca MP" : 0.102038,"Anderson .Paak" : 0.101971,"Ab-Soul, Anderson .Paak & James Blake" : 0.101904,"Bring Me The Horizon" : 0.101837,"Christina Perri" : 0.101770,"Hank Williams Jr." : 0.101703,
"Calum Scott" : 0.101637,"Calum Scott & Leona Lewis" : 0.101570,"070 Shake" : 0.101504,"070 Shake & Jessie Reyez" : 0.101437,"Rage Against the Machine" : 0.101371,"Dixie Chicks" : 0.101305,"The Head and the Heart" : 0.101239,"Russell Dickerson" : 0.101173,"Bon Iver" : 0.101107,"Vampire Weekend" : 0.101041,
"Bethel Music" : 0.100975,"Brent Faiyaz" : 0.100910,"Electric Light Orchestra" : 0.100844,"Papa Roach" : 0.100779,"Pentatonix" : 0.100713,"Maggie Rogers" : 0.100648,"Anuel AA" : 0.100583,"Karol G & Anuel AA" : 0.100518,"Anuel AA, Ñengo Flow, Farruko, Bad Bunny, Darell & Casper Mágico" : 0.100453,"Farruko, Anuel AA & Kendo Kaponi" : 0.100388,
"Dominic Fike" : 0.100323,"Halsey & Dominic Fike" : 0.100258,"Hollywood Undead" : 0.100193,"ABBA" : 0.100129,"Bas" : 0.100064}

#scores each lyrics based on the artists popularity, the uniquness of the word, and how many times the word reappears
def Indexer():
    '''scores each lyrics based on the artists popularity, the uniquness of the word, and how many times the word reappears'''
    global wordindex
    for artistname in maindict.keys():
        try:
            artistscore = artistscores[artistname]
        except:
            artistscore = .14
        for songname in maindict[artistname].keys():
            for indexnum in maindict[artistname][songname].keys():
                for word in maindict[artistname][songname][indexnum].split():
                    uniqueness = 1/(len(maindict[artistname][songname][indexnum].split()))
                    word = word.lower()
                    if word not in stopwords:
                        indexname = str(artistname) + "/" +str(songname)+ "/" + str(indexnum)
                        if word in wordindex.keys():
                            if indexname in wordindex[word].keys():
                                wordindex[word][indexname] -= 0.01
                            else:
                                wordindex[word][indexname] = 0.3 + artistscore + uniqueness
                        else:
                            wordindex[word] = {}
                            wordindex[word][indexname] = 0.3 + artistscore + uniqueness


def Saver():
    '''Saves the wordindex'''
    json.dump(wordindex, open("WordIndex.txt", 'w'))

if __name__ == "__main__":
    Loader()
    Indexer()
    Saver()



