"""Starter content for Virasat.

Everything here is demo material. The people are fictional; the places, crafts and
old texts are real, and each text says plainly what it is and how well it is attested.
Photographs are hotlinked from Pexels (free licence).
"""

from datetime import datetime, timedelta

import db


def px(photo_id, w=1400):
    return (f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg"
            f"?auto=compress&cs=tinysrgb&w={w}")


def days_ago(n):
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d %H:%M")


PLACES = [
    dict(slug="jaipur", name="Jaipur", state="Rajasthan", region="North-west India",
         accent="#e0788a", hero=px(16534739, 2000), best_time="October to March",
         languages="Hindi, Rajasthani, English",
         tags="craft,architecture,desert,textile,pottery,royal",
         tagline="A city drawn on a grid in 1727, still full of the families who built it.",
         intro="Jaipur was planned as nine blocks around a palace, with whole streets given to "
               "craft guilds. Potters, block printers, lac workers and cooks still live in those "
               "streets. People here share the pink city they actually live in, not the postcard."),
    dict(slug="varanasi", name="Varanasi", state="Uttar Pradesh", region="Gangetic plain",
         accent="#e8894d", hero=px(31072582, 2000), best_time="November to February",
         languages="Hindi, Bhojpuri, Urdu, Sanskrit",
         tags="river,ritual,weaving,pilgrimage,music,textile",
         tagline="A city on a river bend where the day starts before the sun.",
         intro="Varanasi has been lived in continuously for around three thousand years. Silk "
               "weavers work pit looms in Madanpura, boatmen row the same stretch their families "
               "always have, and scholars still read Sanskrit on the steps at dawn."),
    dict(slug="kutch", name="Kutch", state="Gujarat", region="Western salt desert",
         accent="#6f93e6", hero=px(19220904, 2000), best_time="November to February",
         languages="Kutchi, Gujarati, Sindhi",
         tags="desert,textile,craft,nomadic,salt,embroidery",
         tagline="A white salt desert where every community signs its name in thread.",
         intro="Kutch was an island for part of every year until the monsoon flats dried. Its "
               "herders and artisans each carry a distinct embroidery, print or pot, and after the "
               "2001 earthquake many villages rebuilt their houses and their crafts together."),
    dict(slug="kochi", name="Kochi", state="Kerala", region="Malabar coast",
         accent="#46b38b", hero=px(12593493, 2000), best_time="October to March",
         languages="Malayalam, Konkani, English",
         tags="coast,trade,performance,spice,water,theatre",
         tagline="A harbour that kept a little of everyone who ever sailed in.",
         intro="Ships came to this coast for pepper for two thousand years. Jewish, Portuguese, "
               "Dutch, Gujarati and Konkani families live within a few streets, Kathakali artists "
               "train for years before they are allowed on stage, and the old nets still need six men."),
    dict(slug="ladakh", name="Ladakh", state="Ladakh", region="Trans-Himalaya",
         accent="#4fb3c9", hero=px(5015007, 2000), best_time="June to September",
         languages="Ladakhi, Hindi, English",
         tags="mountain,monastery,painting,high-desert,buddhist,winter",
         tagline="High desert villages where winter is the season for painting and stories.",
         intro="Ladakh sits above three thousand metres on the old salt and pashmina routes. "
               "Water is counted, villages are small, and monasteries are working places rather "
               "than monuments. Most of the art gets made in the frozen months."),
    dict(slug="hampi", name="Hampi", state="Karnataka", region="Deccan plateau",
         accent="#c98f6b", hero=px(18331785, 2000), best_time="October to February",
         languages="Kannada, Telugu, English",
         tags="ruins,stone,river,empire,temple,carving",
         tagline="The ruins of an empire among boulders, and the carvers who still cut that stone.",
         intro="In the 1500s Hampi was one of the largest cities in the world, capital of the "
               "Vijayanagara empire, until it was sacked in 1565. Carving families around it still "
               "work the same grey granite, and across the river women weave banana fibre."),
]

# Old texts tied to each place. The `note` field is where honesty about the source lives.
TEXTS = [
    ("jaipur", "Vastu Shastra: the nine-square plan", "Treatises compiled c. 6th-11th century CE",
     "Sanskrit", "Shilpa and Vastu texts such as the Manasara and Mayamata",
     "The town is set out as a square divided into nine squares. The centre belongs to the deity, "
     "the ring around it to the ruler and the crafts, and the outer ring to those who come and go. "
     "Streets run to the cardinal directions so that wind and water know where to travel.",
     "Paraphrase, not a quotation. Jaipur was laid out in 1727 to a nine-block plan credited to "
     "Vidyadhar Bhattacharya, who worked from this family of texts. A hill forced one block to be "
     "moved, which is why the grid is not perfect."),
    ("jaipur", "Prithviraj Raso", "Attributed to the 12th century; surviving versions are later",
     "Braj Bhasha", "Attributed to the court poet Chand Bardai",
     "The poem tells of Prithviraj Chauhan, his court, his battles and his elopement with "
     "Samyogita, in the voice of a poet who claims to have stood beside him.",
     "Loved as literature, unreliable as history. The oldest surviving versions are centuries "
     "later than the events, and historians treat most of the detail as legend."),
    ("varanasi", "Kashi Khanda, from the Skanda Purana", "Compiled c. 13th-14th century CE",
     "Sanskrit", "A section of the Skanda Purana devoted to Kashi",
     "Kashi is described as the city resting on Shiva's trident, untouched even when the rest of "
     "the world dissolves. It names the ghats, the wells and the shrines, and tells pilgrims the "
     "order in which to walk them.",
     "Paraphrase. The text is devotional geography rather than a chronicle, but it is the reason "
     "many of the ghats are still walked in the order they are."),
    ("varanasi", "The first sermon at Sarnath", "Traditionally c. 5th century BCE; written down later",
     "Pali", "Dhammacakkappavattana Sutta, Pali canon",
     "At the deer park near Varanasi the Buddha is said to have taught the middle way between "
     "indulgence and severity, and the four truths that follow from it, to five companions.",
     "Paraphrase. Sarnath is ten kilometres from the ghats. The Pali canon was carried orally for "
     "generations before it was written down."),
    ("kutch", "The Dholavira signboard", "Harappan, c. 2500-1900 BCE", "Indus script (undeciphered)",
     "Found above a gateway at Dholavira in Kutch; held by the Archaeological Survey of India",
     "Ten large signs, each about 37 cm high, once inlaid in gypsum on a wooden board that fell and "
     "left its letters lying in order in the ground.",
     "Nobody can read it. Every published translation is a guess. It is the longest known Indus "
     "inscription and it sits in the same district as the embroidery and the salt flats."),
    ("kutch", "Kutchi dohas of the herders", "Oral tradition, centuries old", "Kutchi",
     "Sung by Maldhari herders in the Banni grassland",
     "Short couplets about rain that does not come, a buffalo that strays, a daughter married into "
     "a far village, and the stars used to find the way home across the flats.",
     "Oral and still changing. Nothing here is fixed in a manuscript, which is exactly why members "
     "are recording what their grandparents sing."),
    ("kochi", "Periplus of the Erythraean Sea", "Greek, 1st century CE", "Koine Greek",
     "An anonymous merchant's handbook to the Indian Ocean trade",
     "It lists Muziris on this coast as a port rich in pepper and malabathrum, reached with the "
     "summer monsoon wind, where ships from Egypt lie at anchor and take on cargo.",
     "Paraphrase. Muziris has not been located with certainty; Pattanam, north of Kochi, is the "
     "leading candidate from excavation."),
    ("kochi", "The Kochi copper plates", "c. 1000 CE", "Old Malayalam in Vatteluttu script",
     "Copper plates kept by the Paradesi synagogue community in Mattancherry",
     "A ruler grants a merchant named Joseph Rabban rights over a settlement: tolls, a palanquin, a "
     "lamp by day, and the trade of the port, to him and his descendants.",
     "The plates are real and still in Kochi. The exact date and the identity of the ruler are "
     "argued over by historians."),
    ("ladakh", "La-dvags rgyal-rabs, the Chronicles of Ladakh",
     "Compiled 17th century from older records", "Classical Tibetan",
     "Royal chronicle of the Namgyal kings",
     "It traces the kings of Ladakh from legendary ancestors down to the builders of Leh palace, "
     "listing the monasteries each founded and the treaties each signed.",
     "A court record: reliable about monasteries and lineages, partisan about wars."),
    ("ladakh", "Inscriptions in the Alchi temples", "c. 11th-12th century CE", "Tibetan and Sanskrit",
     "Painted and carved dedications at the Alchi Chos-khor, Ladakh",
     "Short dedications naming who paid for a wall, which artists painted it, and the merit the "
     "donor hoped to gain for their family.",
     "Rare because they name the painters. The murals are among the oldest surviving in the "
     "western Himalaya and are extremely fragile."),
    ("hampi", "Amuktamalyada", "Early 16th century", "Telugu",
     "Attributed to Krishnadevaraya, king of Vijayanagara",
     "Between the story of the poet-saint Andal, the king sets down advice on ruling: keep the "
     "tanks and canals repaired, tax lightly in bad years, and treat the forest peoples as allies "
     "rather than enemies.",
     "Paraphrase. Authorship by the king is the traditional attribution and is generally accepted, "
     "though court poets likely had a hand in it."),
    ("hampi", "Domingo Paes on Vijayanagara", "c. 1520", "Portuguese",
     "Account of a Portuguese horse trader who lived in the city",
     "He describes a city as large as Rome, with bazaars selling rubies by the heap, irrigation "
     "channels cut through rock, and a festival where the king weighs himself against gold.",
     "An eyewitness, but an outsider dazzled by wealth. Read it beside the inscriptions, which care "
     "more about temple grants and water works."),
]

# handle, name, place, craft, bio, monetized, payout, joined days ago
MEMBERS = [
    ("kamla", "Kamla Devi Prajapat", "jaipur", "Blue pottery",
     "Third generation in a quartz-and-cobalt yard in Amba Bari. I teach two apprentices every winter.",
     1, "UPI", 240),
    ("yusuf", "Mohammed Yusuf Chhipa", "jaipur", "Block printing",
     "I print with blocks my father carved, and still boil my own black from iron and jaggery.",
     1, "Bank account", 210),
    ("rukmani", "Rukmani Devi Sharma", "jaipur", "Home cooking",
     "I cook the way my mother-in-law taught me in 1971. I am here for the recipes, not for selling.",
     0, "", 180),
    ("ramesh", "Ramesh Majhi", "varanasi", "River life",
     "Mallah family, five generations of boatmen. I row at dawn and sleep in the afternoon.",
     1, "UPI", 300),
    ("abdul", "Abdul Rahim Ansari", "varanasi", "Banarasi weaving",
     "Kadhua weaver in Madanpura. One sari takes my son and me eighteen to forty days.",
     1, "Bank account", 275),
    ("meera", "Meera Shukla", "varanasi", "Photography",
     "I study history and photograph the ghats before class. Everything I post is free to look at.",
     0, "", 95),
    ("jabbar", "Jabbar Khatri", "kutch", "Ajrakh printing",
     "Ninth generation printer. We rebuilt our dye works at Ajrakhpur after the 2001 earthquake.",
     1, "UPI", 260),
    ("raniben", "Rani Ben Ahir", "kutch", "Embroidery",
     "Twenty-two of us stitch in the afternoons. I post our patterns so they are not forgotten.",
     0, "", 150),
    ("sivan", "Sivan Nair", "kochi", "Kathakali",
     "Eleven years of training before my first lead role. I write about what the make-up means.",
     1, "UPI", 230),
    ("mary", "Mary Joseph", "kochi", "Kitchen notebooks",
     "I am copying out my grandmother's 1958 recipe notebook before the ink goes.",
     0, "", 120),
    ("lobzang", "Lobzang Tundup", "ladakh", "Thangka painting",
     "I grind my colours from stone. A large thangka takes me four months, mostly in winter.",
     1, "Bank account", 205),
    ("stanzin", "Stanzin Angmo", "ladakh", "Writing",
     "I run three rooms in Sabu and write down what the old people in the village remember.",
     0, "", 140),
    ("mallappa", "Mallappa Shilpi", "hampi", "Granite carving",
     "Forty years with a chisel. My grandfather worked on restoring the Vittala pillars.",
     1, "UPI", 190),
    ("aditi", "Aditi Rao", "hampi", "Travel writing",
     "I came for a weekend in 2019 and keep going back. I write what the guidebooks leave out.",
     0, "", 110),
]

# handle, place, kind, title, body, cover, [(extra image, caption)]
POSTS = [
    ("kamla", "jaipur", "story", "The blue that isn't clay",
     "People pick up a bowl in my yard and say, what beautiful clay. I laugh, because there is no "
     "potter's clay in it at all. Our pots are ground quartz, a little Multani mitti, powdered "
     "glass, borax and katira gum from a tree.\n\n"
     "The craft came from Persia by way of the Mughals, first as tiles for mosques and palaces. In "
     "the 1800s Maharaja Sawai Ram Singh II brought craftsmen to Jaipur and opened a school of art. "
     "My husband's grandfather learnt there. After independence the craft nearly died, and families "
     "like ours kept one kiln going when there were no buyers.\n\n"
     "The dough has no stretch, so we cannot throw it on a wheel. We press it into moulds, dry it in "
     "the shade for days and sand it by hand. Then we paint: cobalt oxide for the deep blue, copper "
     "oxide for the turquoise. Every blue you see was a grey powder the day before.\n\n"
     "We fire once, low, for about six hours. If the weather turns or someone opens the kiln early, "
     "half the pots crack. When you hold a piece, you are holding a week of waiting.",
     px(7245524), [(px(39265943), "Pots drying in the shade, waiting for the brush"),
                   (px(19195961), "The same cobalt, on a palace wall: the craft arrived as tiles")]),
    ("yusuf", "jaipur", "story", "Three thousand blocks and my father's hands",
     "In our workshop there is a wall of teak blocks, three thousand of them. My father carved most "
     "of them. When I press one onto cloth the flower comes out exactly as he cut it forty years ago.\n\n"
     "Sanganeri print is known for small, fine flowers on a white ground. We print by hand, one block "
     "at a time, lining up each impression by eye. A bedcover can take more than two thousand "
     "presses, and a crooked one shows from across the room.\n\n"
     "Our black is syahi: rusted iron, jaggery and water, left to ferment for weeks. It smells "
     "terrible and it never fades. For red we boil madder root; for yellow, pomegranate rind.",
     px(28389703), [(px(5505438), "Carving a new block takes about a week")]),
    ("rukmani", "jaipur", "writing", "What we cook when there is no water",
     "Rajasthani cooking is shaped by a simple fact: for most of the year there is not much water. "
     "So we cook in milk, in buttermilk, in ghee. Ker and sangri are desert berries and beans that "
     "keep for a year once dried.\n\n"
     "Dal baati is baked in the embers of a dung fire, not boiled. The baati cracks open and you "
     "pour ghee into the crack. My mother-in-law taught me to listen for the sound it makes when it "
     "is ready, a hollow knock, like knuckles on a door.",
     px(8818723), []),
    ("meera", "varanasi", "photo", "Six mornings on the ghats",
     "I photograph between five and seven, before my classes. The light is grey, then brass, then "
     "gone. Nobody performs for the camera at that hour; people are simply washing, praying, "
     "sleeping, arguing about the price of milk.\n\n"
     "I do not photograph at Manikarnika. Ramesh bhai told me once that for the families on those "
     "steps it is the worst morning of their lives, and I have not pointed a camera there since.",
     px(31072582), [(px(38941451), "Boats waiting for first light"),
                    (px(35729427), "The same steps at night"),
                    (px(36887958), "Evening aarti, from the water")]),
    ("abdul", "varanasi", "story", "Eighteen days for one sari",
     "My loom sits in a pit in the floor so my legs can work the pedals. My father's loom sat in the "
     "same pit.\n\n"
     "There are two ways to make the motifs on a Banarasi sari. The quick way runs the extra thread "
     "across the whole width and cuts the loose floats away behind. In kadhua each flower is woven "
     "on its own with a small shuttle, only where it is needed. Turn a kadhua sari over and the back "
     "is almost as clean as the front.\n\n"
     "A power-loom copy takes a few hours and sells in the same shops under the same name. The only "
     "thing that protects us is people who know the difference.",
     px(31508152), [(px(6332015), "Warp threads, counted and tied by hand")]),
    ("ramesh", "varanasi", "story", "The river before sunrise",
     "We are Mallah. Five generations that I can name have rowed this stretch, and probably many "
     "more. My grandfather used to say the Ganga belongs to everyone but the oars belong to us.\n\n"
     "Between five and seven the river is still and the ghats wake one at a time: first the bells, "
     "then the bathers, then the washermen slapping cloth on stone. By nine it is loud and full of "
     "motorboats and I go home to sleep.\n\n"
     "People always ask if I get tired of it. It is the same river, but it is never the same morning.",
     px(38941445), []),
    ("jabbar", "kutch", "story", "Ajrakh means keep it for today",
     "Some say the word comes from azrak, blue in Arabic, for the indigo. My grandmother said it "
     "comes from aaj rakh, keep it for today, because the cloth has to rest a day between every "
     "stage. I prefer her version.\n\n"
     "A piece is printed with a resist of lime and gum, dipped in indigo, printed again with alum so "
     "the madder will hold, boiled, washed, sun-dried and printed again. Both sides are printed so "
     "exactly that you cannot tell front from back.\n\n"
     "Everything depends on water. The river at Dhamadka began to carry iron and our colours dulled; "
     "then the 2001 earthquake took the houses. We bought land together and built a new village. We "
     "called it Ajrakhpur.",
     px(3778061), [(px(19220904), "The Rann, a few hours north of the dye works")]),
    ("raniben", "kutch", "painting", "What the patterns say",
     "An Ahir blouse tells you which village a woman is from and often which family. The pinwheel is "
     "a well; the little parrots are for a wedding; the heavy mirror work is for the bride.\n\n"
     "We cut mirrors from mica once. Now they come from a shop in Bhuj, but the stitch that holds "
     "them is the same buttonhole frame my grandmother used. I post the patterns here because nobody "
     "wrote them down, and the girls who could stitch them are getting older.",
     px(5467615), []),
    ("sivan", "kochi", "story", "Three hours in the chair",
     "People who see Kathakali for the first time think the faces are masks. They are not. Every "
     "line is painted on my skin, and the white frame around my jaw, the chutti, is built up from "
     "rice paste and lime, layer by layer, by another artist.\n\n"
     "The colour tells you who I am before I move. Green, pacha, is for noble heroes. A red streak "
     "on the green means a proud man with a dark side. Black is for hunters and forest people.\n\n"
     "Near the end I put a chundapoovu seed under my eyelid so the whites of my eyes go red and the "
     "back row can follow them in the lamplight. By the time the lamp is lit I am not Sivan.",
     px(31843397), [(px(8610533), "On stage, the story is told with eyes and hands"),
                    (px(33881519), "The finished face, ready for the lamp")]),
    ("mary", "kochi", "text", "My grandmother's notebook, page 14",
     "The notebook is from 1958 and the ink has gone brown. This page is appam batter: raw rice "
     "soaked four hours, ground with grated coconut and a spoon of cooked rice, left overnight with "
     "a little toddy to rise.\n\n"
     "She wrote the quantities in old measures, a changazhi of rice, and I have been converting them "
     "to cups as I copy. Where a word is smudged I have left a gap rather than guess.",
     px(8818667), [(px(5504609), "The spice tins she measured from, in the order she kept them")]),
    ("lobzang", "ladakh", "story", "Grinding the mountain into colour",
     "Every colour in my thangkas was once a rock: lapis for blue, malachite for green, cinnabar for "
     "red, a kind of chalk for white. I grind them for hours in a stone bowl with water and glue. A "
     "small jar of good blue takes me two days.\n\n"
     "The canvas is cotton, coated with chalk and glue and polished with a smooth stone until it "
     "shines like paper. Then I draw the grid. Every deity has fixed proportions, and they are in "
     "texts painters have followed for centuries.\n\n"
     "The eyes are painted last. It is called opening the eyes. After that it is not a painting any "
     "more, and a lama blesses it before it goes to a house or a monastery.",
     px(6650435), [(px(15804654), "Hemis, where the great thangka is shown every twelve years")]),
    ("stanzin", "ladakh", "writing", "What the village remembers about water",
     "Before the pipes came, every field in Sabu was watered by kuhl channels dug along the contour, "
     "and a man called the churpon decided whose turn it was. He kept no register. He remembered.\n\n"
     "The old people say the glacier above us used to reach a rock they can point to. It does not "
     "reach it now. The young men build ice stupas in winter instead, freezing the stream into a "
     "cone that melts late, when the barley needs it.",
     px(19710158), [(px(20078363), "Prayer flags above the valley")]),
    ("mallappa", "hampi", "story", "The stone remembers the chisel",
     "Granite does not forgive. With sandstone you can correct a mistake; granite remembers every "
     "blow. That is why the Vijayanagara carvers were respected. They cut pillars that ring like "
     "bells and a chariot out of stone.\n\n"
     "I began at twelve by sharpening my grandfather's chisels. For two years I was not allowed to "
     "touch a statue, only to square blocks and cut straight lines.\n\n"
     "Please do not climb the old carvings for photographs. They have survived five hundred years "
     "and a war; they should survive our holidays.",
     px(6242546), [(px(29016844), "Figures cut in the Vijayanagara style"),
                   (px(18331785), "The stone chariot at the Vittala temple")]),
    ("aditi", "hampi", "writing", "The boulders were here first",
     "Everyone photographs the chariot. Almost nobody sits on Hemakuta hill at six in the evening, "
     "where the small early shrines are and the granite goes the colour of a peach.\n\n"
     "The empire lasted two hundred years. The boulders have been there for two and a half billion "
     "and will outlast the photographs of both of us.",
     px(37609537), [(px(38297408), "The old bazaar street, where the rubies were sold by the heap")]),
]

# handle, place, title, price, duration, capacity, summary, details, image
EXPERIENCES = [
    ("kamla", "jaipur", "Paint a blue pottery tile in my yard", 1800, "3 hours", 6,
     "Quartz dough, moulds, cobalt, and a tile of your own fired with the next batch.",
     "We start where the dough is pressed into moulds, walk past the pots drying in the shade, and "
     "then sit down to paint. You will use the same cobalt and copper oxide we use. Your tile is "
     "fired with the next batch and posted to you. The yard is closed on firing days.",
     px(7245524)),
    ("yusuf", "jaipur", "Print your own dupatta in Sanganer", 1500, "3.5 hours", 8,
     "Choose from three thousand blocks and print a cotton dupatta in natural black and madder.",
     "You will learn to line the blocks up by eye, which is harder than it looks, and print a "
     "dupatta to take home. I will show you how syahi is fermented from iron and jaggery. Wear "
     "clothes you do not mind staining; natural dye does not wash out.",
     px(28389703)),
    ("ramesh", "varanasi", "Dawn on the river with a Mallah family", 900, "2 hours", 5,
     "Rowed, not motored, from Assi towards Panchganga as the ghats wake up.",
     "Meet me at Assi ghat at 5:15 with a shawl. I row north and tell you the story of each ghat. At "
     "Manikarnika I will ask you to put the camera down, and I will tell you why.",
     px(38941451)),
    ("abdul", "varanasi", "Sit beside a kadhua loom", 1100, "2 hours", 6,
     "Watch a sari woven motif by motif, and learn to tell handloom from power loom.",
     "My son and I will be working. You can sit at the edge of the pit and ask anything. I will also "
     "take you to the shop where the jacquard cards are punched, which nobody thinks to visit.",
     px(31508152)),
    ("jabbar", "kutch", "Ajrakh: from the indigo vat to the river wash", 2200, "4 hours", 6,
     "Print a resist, dip it in indigo, and wash the red up from under the black.",
     "You will work through the first stages on a stole of your own, which we finish and post to you "
     "once it has rested. Lunch with the family. Closed shoes and clothes you can ruin.",
     px(3778061)),
    ("sivan", "kochi", "Watch the make-up, then the performance", 2000, "4 hours", 10,
     "Three hours of chutti being built, then a scene by oil lamp with front-row seats.",
     "Sit in the green room while the face is made, quietly, and I will answer questions afterwards. "
     "Before the scene I will teach you a handful of the hand gestures so you can follow the story.",
     px(31843397)),
    ("lobzang", "ladakh", "Grind pigments in a thangka studio", 2500, "3 hours", 4,
     "Malachite and lapis in a stone bowl, and the first lines of a lotus on prepared canvas.",
     "The studio is my living room, so four people at most. You will prepare a small panel, grind "
     "colour, and draw a lotus on the grid. Butter tea included, whether you like it or not.",
     px(6650435)),
    ("mallappa", "hampi", "Carve your first motif in granite", 1700, "3 hours", 5,
     "Hold a chisel the old way and cut a lotus petal into a granite tile you keep.",
     "Goggles and gloves provided, and a tile each. Mornings only; the stone and the afternoon sun "
     "together are too much. Your hands will shake for the first half hour. Everyone's do.",
     px(6242546)),
]

# handle, place, title, medium, price, story, image
ARTWORKS = [
    ("kamla", "jaipur", "Peacock charger, cobalt and turquoise", "Blue pottery", 6800,
     "The peacock is Rajasthan's bird of the monsoon; its call means rain is near. Persian potters "
     "painted birds among vines, and when the craft reached Jaipur the vines stayed but the birds "
     "became peacocks. Each tail feather is one stroke. Fired once, low, so no two blues match.",
     px(7245524)),
    ("yusuf", "jaipur", "Bootidar bedcover, syahi and madder", "Hand-block print", 5400,
     "A booti is a small scattered flower and Sanganer is known for making them tiny. This cover "
     "carries more than two thousand impressions, each lined up by eye. The black is fermented from "
     "rusted iron and jaggery for three weeks; it darkens with washing instead of fading.",
     px(28389703)),
    ("abdul", "varanasi", "Kadhua shikargah sari", "Banarasi silk", 48000,
     "Shikargah means hunting ground: deer, riders and trees fill the field, a pattern the Mughal "
     "court wore. Every animal was woven separately with a small shuttle, so the back is nearly as "
     "clean as the front. Thirty-four days on the pit loom for my son and me.",
     px(31508152)),
    ("jabbar", "kutch", "Double-sided Ajrakh stole", "Ajrakh print", 3800,
     "Printed on both sides so exactly that there is no wrong side. The central star is the one the "
     "herders use to find north. Fourteen stages of printing, dyeing, washing and resting over "
     "sixteen days.",
     px(3778061)),
    ("raniben", "kutch", "Mirror-work panel", "Ahir embroidery", 7500,
     "Parrots, a peacock and the pinwheel of a well. Three of us stitched it over six weeks in the "
     "afternoons, and each signed her own corner in thread.",
     px(5467615)),
    ("sivan", "kochi", "Pacha face study", "Natural pigment on handmade paper", 3200,
     "We practise the make-up on paper before we work on a face. Same pigments: manayola, a yellow "
     "mineral, mixed with indigo for the green, and chayilyam for the lips. This is a pacha "
     "character, a noble hero.",
     px(33881519)),
    ("lobzang", "ladakh", "Ashtamangala door panel", "Mineral pigment on poplar", 18500,
     "The eight auspicious symbols painted above doors across Ladakh to bless whoever walks under "
     "them: parasol, fish, vase, lotus, conch, endless knot, banner, wheel. Every colour ground by "
     "hand; the gold laid last, after the dedication.",
     px(6650435)),
    ("mallappa", "hampi", "Dancers of Vijayanagara, granite panel", "Stone carving", 22000,
     "The Mahanavami platform is carved with dancers, musicians and processions from the king's "
     "court. This is one frieze at half size, cut with the same kind of chisels. Drawn and redrawn "
     "in chalk for a week before the first cut, because granite forgives nothing.",
     px(29016844)),
]

COMMENTS = [
    ("s1", "meera", "I have walked past your lane a hundred times and never knew the blue was stone."),
    ("s1", "aditi", "The week of waiting line stopped me. Thank you for writing it down."),
    ("s4", "ramesh", "The light you caught on the third one is exactly how it is at six."),
    ("s5", "aditi", "I bought a 'Banarasi' in a mall last year. Now I know what I actually bought."),
    ("s9", "mary", "My uncle played kathi roles. He used to come home still half green."),
    ("s12", "stanzin", "We freeze the stream into cones here too. Same worry, different valley."),
    ("s13", "aditi", "The boulders were here first, and your chisels are the only thing that argues back."),
]


# The bloom gallery on each place page. The first picture sits in the middle;
# the rest open around it like petals. Every caption describes that actual photograph.
GALLERIES = {
    "jaipur": [
        (16534739, "Hawa Mahal's pink lattice, built in 1799 so the women of the court could watch the street unseen"),
        (7245524, "Blue pottery tiles: ground quartz, not clay, under cobalt and copper"),
        (28389703, "A printing block being cut by hand in Sanganer"),
        (36470562, "Amber Fort above the Maota lake, an hour before the buses"),
        (19195961, "A palace room painted in the same cobalt the potters grind"),
        (984534, "A sweet shop in the walled city, older than the road outside it"),
        (5438965, "The same facade after dark, when the crowds have gone"),
    ],
    "varanasi": [
        (31072582, "A man praying at the water's edge, a little after five"),
        (38941451, "Wooden boats tied up, waiting for first light"),
        (36887958, "The evening aarti, lamps and marigolds, seen from the water"),
        (31508152, "A handloom mid-weave, the pattern held on cards above it"),
        (35729427, "The ghats at night, when the steps belong to the dogs"),
        (6332015, "Warp threads counted and tied by hand before a sari begins"),
        (38941445, "Mallah boats on the Ganga, their oars worn smooth"),
    ],
    "kutch": [
        (19220904, "The road across the Rann, salt flats to the horizon on both sides"),
        (3778061, "Offcuts on the floor of a printing workshop in Bhuj"),
        (23808903, "The night sky over the salt, with no town lights for fifty kilometres"),
        (5467615, "Mirror-worked cloth and henna, the week before a wedding"),
        (29230111, "A decorated camel resting between journeys"),
        (30199251, "Carved stone from Gujarat's old stepwell builders"),
        (7804406, "One plate, shared, at the end of the day's work"),
    ],
    "kochi": [
        (12593493, "The cheenavala nets at Fort Kochi, each one worked by six men"),
        (31843397, "A Kathakali actor in the green room, three hours before the lamp"),
        (8610533, "On stage, where the story is told with the eyes and the hands"),
        (32054122, "The same nets at sunset, counterweighted with river stones"),
        (35347829, "Backwater channels south of the harbour"),
        (33881519, "The finished face: rice paste, lime and mineral colour"),
        (962464, "A kettuvallam moving between the coconut palms"),
    ],
    "ladakh": [
        (5015007, "Stupas and prayer flags at Thiksey, above the Indus valley"),
        (6650435, "A prayer-wheel pavilion painted in ground mineral colours"),
        (19710158, "Lamayuru, built into the folds of its own valley"),
        (20078363, "Flags printed with prayers, left for the wind to read"),
        (15804654, "Hemis, where the giant thangka is unrolled once in twelve years"),
        (33792527, "A monastery courtyard between prayers"),
        (17934993, "The Maitreya at Diskit, facing the Nubra valley"),
    ],
    "hampi": [
        (18331785, "The stone chariot at the Vittala temple, cut from granite blocks"),
        (29016844, "Dancers and musicians carved along a platform wall"),
        (37609537, "A temple courtyard, empty in the middle of the day"),
        (6242546, "Hammer and chisel on granite, the way it has always been done"),
        (38297408, "The pillared halls of the old bazaar street"),
        (4079565, "Panels cut into a temple wall, worn down by five hundred years"),
        (32216135, "The builders who came before them, a few hours away"),
    ],
}


def fill():
    """Write the starter content into an empty database."""
    place_id = {}
    for p in PLACES:
        place_id[p["slug"]] = db.execute(
            "INSERT INTO places (slug, name, state, region, tagline, intro, hero, accent,"
            " best_time, languages, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (p["slug"], p["name"], p["state"], p["region"], p["tagline"], p["intro"], p["hero"],
             p["accent"], p["best_time"], p["languages"], p["tags"]))

    for slug, pictures in GALLERIES.items():
        for order, (photo, caption) in enumerate(pictures):
            db.execute("INSERT INTO place_images (place_id, url, caption, ord) VALUES (?,?,?,?)",
                       (place_id[slug], px(photo), caption, order))

    for slug, title, era, lang, source, passage, note in TEXTS:
        db.execute(
            "INSERT INTO texts (place_id, title, era, language, source, passage, note)"
            " VALUES (?,?,?,?,?,?,?)",
            (place_id[slug], title, era, lang, source, passage, note))

    member_id = {}
    for handle, name, slug, craft, bio, monetized, payout, joined in MEMBERS:
        member_id[handle] = db.execute(
            "INSERT INTO members (handle, name, place_id, bio, craft, avatar, monetized, payout,"
            " joined) VALUES (?,?,?,?,?,?,?,?,?)",
            (handle, name, place_id[slug], bio, craft, "", monetized, payout, days_ago(joined)))
        db.execute("INSERT INTO interests (member_id, place_id) VALUES (?,?)",
                   (member_id[handle], place_id[slug]))

    post_key = {}
    for i, (handle, slug, kind, title, body, cover, extras) in enumerate(POSTS, start=1):
        pid = db.execute(
            "INSERT INTO posts (member_id, place_id, kind, title, body, cover, created)"
            " VALUES (?,?,?,?,?,?,?)",
            (member_id[handle], place_id[slug], kind, title, body, cover, days_ago(60 - i * 3)))
        post_key[f"s{i}"] = pid
        for order, (url, caption) in enumerate(extras):
            db.execute("INSERT INTO images (post_id, url, caption, ord) VALUES (?,?,?,?)",
                       (pid, url, caption, order))
        for liker in list(member_id.values())[: 3 + (i % 6)]:
            db.execute("INSERT OR IGNORE INTO appreciations (post_id, member_id) VALUES (?,?)",
                       (pid, liker))

    for key, handle, body in COMMENTS:
        db.execute("INSERT INTO comments (post_id, member_id, body, created) VALUES (?,?,?,?)",
                   (post_key[key], member_id[handle], body, days_ago(5)))

    exp_id = {}
    for handle, slug, title, price, duration, cap, summary, details, image in EXPERIENCES:
        exp_id[title] = db.execute(
            "INSERT INTO experiences (member_id, place_id, title, summary, details, price,"
            " duration, capacity, image, created) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (member_id[handle], place_id[slug], title, summary, details, price, duration, cap,
             image, days_ago(40)))

    art_id = {}
    for handle, slug, title, medium, price, story, image in ARTWORKS:
        art_id[title] = db.execute(
            "INSERT INTO artworks (member_id, place_id, title, medium, story, price, image,"
            " created) VALUES (?,?,?,?,?,?,?,?)",
            (member_id[handle], place_id[slug], title, medium, story, price, image, days_ago(30)))

    # A few requests already waiting, so a seller's dashboard has something in it.
    seeded = [
        ("experience", exp_id["Paint a blue pottery tile in my yard"], "aditi", "kamla",
         "Two of us, both beginners. Is the morning slot alright?", 4, 2, 3600, "pending"),
        ("experience", exp_id["Paint a blue pottery tile in my yard"], "meera", "kamla",
         "I would like to photograph the yard as well, if that is allowed.", 9, 1, 1800, "accepted"),
        ("art", art_id["Peacock charger, cobalt and turquoise"], "stanzin", "kamla",
         "Would you consider 6,000 for the charger? I would carry it home by hand.", 2, 1, 6000,
         "pending"),
        ("experience", exp_id["Dawn on the river with a Mallah family"], "aditi", "ramesh",
         "Three of us, Friday if the river is calm.", 6, 3, 2700, "accepted"),
    ]
    for kind, ref, frm, to, message, in_days, guests, amount, status in seeded:
        date = (datetime.now() + timedelta(days=in_days)).strftime("%Y-%m-%d")
        db.execute(
            "INSERT INTO requests (kind, ref_id, from_id, to_id, message, date, guests, amount,"
            " status, created) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (kind, ref, member_id[frm], member_id[to], message, date, guests, amount, status,
             days_ago(3)))
