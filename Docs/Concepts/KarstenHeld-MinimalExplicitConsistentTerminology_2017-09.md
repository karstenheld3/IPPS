<DevSystem APAPALAN=false />

# Minimal Explicit Consistent Terminology

Karsten Held, September 2017

MECT is a communication strategy and means "Use minimal explicit consistent terminology within a defined field of interaction". The field can be a business, a document, a factory, a product, a process, a team or a meeting.

**Minimal** means you should use just one name for one thing. If something already has a widely accepted and working name, use that. Minimal also means stable terminology over time and across different contexts. If it's horsepower, then it's horsepower. Efficiency in understanding is more important than technical correctness.

**Explicit** means you should not rely on implicit knowledge. Humans are born with zero implicit knowledge. By using explicit, self-describing terms you make life easier for inexperienced people and teach them what things are and how they work. A good name evokes the right association field. The word "button" is much easier to understand than terms like "actiontrigger" or "on-off-provider". Its association field is much stronger and it does not require much interpretation. We all know what a button is. Resist lecturing people by choosing obscure, technical, or implicit wording. Choose words that exist in everybody's daily life. This way you build on shared experiences and common knowledge.

**Consistent** means you should use your terminology everywhere within your field of interaction and always in the same way. Repetition helps people recognize connections and learn the correct associations. It also makes things predictable. If others use different terminology, provide translations and descriptions so that everybody can easily adapt and cooperate.

By following this strategy, you get predictable, safe and efficient communication. It helps you avoid misunderstandings, establish clarity and keep dependencies, ambiguities and feedback loops at a minimum. If communication is clear, people can act independently. Carefully chosen words lead to efficient mental models that are compatible with each other. They reduce the complexity of processes because people spend less time managing friction and noisy communication.

MECT does not advocate minimum communication. If more words lead to less questions and misunderstandings, then use more words. MECT only tells you to keep your term fragmentation low and be compatible with yourself. It's like LEGO for communication - every piece has a distinctive purpose and fits well with all other pieces.

I once had the chance of working in the financial sector. My work was all about stocks, dividends, corporate actions, trading, volumes, executions, tickers, symbols, quotes, prices, fills, futures, options, underlyings and derivatives. At first I was overwhelmed by sheer amount of concepts, procedures and conventions. To make matters worse, it didn't relate much to anything in my daily life. But it all became clearer when I started to use the Bloomberg terminal. It was a computer with two monitors and a special keyboard where you had keys like "Corp", "Index", and "Cmdty". It was our gateway to the world of real-time information. All you had to do was to enter some commands and press some keys and it instantly showed you the price graph of a stock or the composition of an index or the properties of a special bond. It also had a pretty good help system that explained everything.

By learning the commands of the Bloomberg terminal I learned how the financial industry was structured and how things worked. By listing all futures for a given index I learned what an underlying was. The sequence of text commands made that clear. The daily use of these commands helped me remember the names and meanings of lots of abstract concepts. The best thing was that you could reuse the Bloomberg terminology in documents, emails and phone calls. It was tightly aligned with how professionals really talked. Every view, object, page and function in this system had a single short command that closely reflected its descriptive name. "OMON" stood for "Option Monitor", "FXR" was "Foreign Exchange Rates", "MCS" lead to "Multi Currency Settlement" where you could look up banking holidays. If Bloomberg users talk about an index they talk about entering a name and then pressing the "Index" button. You can quickly exchange incredible amounts of information on the phone with a system like that.

The Bloomberg system of tickers, names, mnemonics, conventions and commands made it possible to speak in a consistent and precise language. It taught you the structure and relation of objects, served as a search and query language and allowed incredible fast navigation through convention and unification.

I later expanded its concept of unique and predictable mnemonics to futures and options where no unified naming convention existed. We called that a FUTOP-ID: an ID for futures and options. It made heavy use of existing Bloomberg conventions for the underlyings and allowed us to parse the inventory data of 12 different banks on a daily basis and match it against our internal systems. What came to us as "Call on Dow Jones EStoxx 50 with a strike of 4400 that expires in february 2008" became transformed into a FUTOP-ID of "CALL-DJESTOXX50@4400EX2008-02" and could now be matched against another "ESTOXX 50 Call at 4400 (Feb 2008)" that got converted to that same FUTOP-ID.

If you can convert a vague collection of properties into a predictable and unambiguous form you can easily compare, sort and identify, match, join, and count everything using computers. No brainpower required. That's the essence of language: How you express things with minimum effort so that others understand you instantly and can process information very fast without errors and misunderstandings. The Bloomberg ecosystem is one of the greatest examples of MECT put into practice.

---

Ten years later I worked for an automotive company that sold various measurement devices to garages. They had a tablet based software for entering damages and performing car checks. The software itself had 4 different names and the screens had names like "Welcome screen", "Car Ticket Manager", and "Data Center", "Customer Screen". At the first look it might seem reasonable to name screens like that. But once you try to predict what you will see on those screens you discover the problems of unspecific meta-terms. A "Welcome screen" can contain anything. "Data Center" is even more unspecific.

The software was conceptually developed in Germany and programmed in Hungary without any shared technical document that defined a common terminology. The programmers could name things as they liked. And so they did. A "garage" became a "service" here and a "workshop" there and the software managed "car tickets" in the user interface that that where called "service events" internally. These service events contained service tickets that resulted from checklists that contained checkpoints that contained questions and collected answers but sometimes also measurement data that was associated with 5 different types of measurement modules. Can you still follow me?

Besides using a lot of ambiguous meta-words like "service", "module", "event" and "ticket" and inconsistent naming the whole system was also somewhat over-engineered. These introduced objects naturally required even more names. One day I searched for the location of the license plate and car type that were stored within a car ticket (= the service event). I found it stored in the measurement data object of a 6th type of measurement module called "Info Measurement Module". That is pretty confusing right? Why should the license plate be stored in a "measurement module" when it has nothing to do with measurements?

The whole confusion with terminology gave birth to serious data modeling problems. As the company grew, other products and systems came into existence that modeled their data differently. And they again named things differently. Very understandably they didn't want to adapt their colleagues confusing terminology. It was like building the tower of babel: Lots of different teams speaking different languages but essentially dealing with the same thing: a vehicle (car, bus, whatever) being repaired.

These experiences above often left me asking "What is so difficult in naming and modeling things correctly?" When working in domains with well-designed, consistent and modular terminology, everything seemed so straightforward and easy. But once I entered those Babel-like places, productivity decreased and arguments, meetings, and feedback-loops dominated the daily business. So what was the root cause that divided those two worlds? The answer lies in a better question: "Why is creating a consistent and unambiguous language and agreeing about it so difficult?" I think it is because of three reasons:

1. **It forces you to write things down.** Which enables others to test your assumptions, identify gaps of interpretation and discover ambiguities and conceptual flaws. Some people will intentionally try to avoid this the beginning of a project. But it has to be done anyway because you'll have to name things some way or the other. This will bring in criticism and arguments. But changing words on a sheet of paper is a lot cheaper than changing entire processes or operational systems. If you get this right, you might be able to agree on stable naming conventions. Which is the basis for efficient mental models that can serve as the DNA for your field of action. But if not, you will leave everybody frustrated. Negotiating conventions bears the risk of not succeeding or agreeing on a bunch of crappy compromises. That's one reason why people avoid it in the beginning: The fear of having to commit yourself and not being able to reach an agreement.

2. **Changes are poorly managed.** Once you agreed on a written set of definitions, you will also have to agree about changes. It is very likely that you will not get it absolutely right the first time. Incorporating the right amount of changes again is a lot of work. Even if people see the benefits of a change, habits are more difficult to change than thoughts. So you have to be very conservative. Successful long-term projects show that a slow and minimalistic approach is healthier than dictating and recalling changes in a hurry. Often managers change their terminology to death and people lose track of how things should work together properly.

3. **The impact of language is underestimated.** People think it's just words and they can change them at any time later. But words represent concepts and their association fields define the mental models we build to predict the outcome of our actions. Once people incorporated mental models they are very unlikely to change them. Often, when building a system or designing a processes your main focus is getting ready in time. It's not discussing terminology and edge cases. But not agreeing on terminology allows incompatible mental models to coexist and grow undetected. Sooner or later they will collide, cause misunderstandings and result in errors. They will divide a team into schools of thought, lead into fierce arguments and bring everything to a halt. Language is the operating system of the human mind. It determines what you can accept and how you are able to exist. Creating a common language is a continuous, time-consuming effort. Very often team leaders fail to recognize how important it is.

The described MECT principle will help you detect where things go wrong. You can precisely tell people what to improve, how to do it and why it's important. Once you have understood the importance of being a "gardener of communication", you can use these tools to shape language and let it grow into a stable and efficient communication platform. If everything feels like being in the right place and having the right name, people will adopt your terminology and your ideas will spread. Growth will be a lot easier and your field of interaction will attract productive people and sharp minds.

---

## Hall of Fail

### The Apartment That Was Both C and D

In March 2026, a tenant signed a rental contract for an apartment in Portugal. The contract clearly stated: "Fração C, 1º Andar Direito" (Fraction C, 1st Floor Right). The tenant used this address to register with four utility providers: electricity, water, gas, and internet. Everything seemed clear.

Weeks later, the tenant noticed mail wasn't arriving. After investigation, the landlord clarified: "Fração C is only for property registry purposes. The correct postal address is 1º D." It turned out that Portuguese buildings use two overlapping letter systems:

- **Fração (A, B, C...)** = Legal property registry designation (for deeds, taxes, contracts)
- **Floor position (D, E, F...)** = Physical location indicator (D=Direito/Right, E=Esquerdo/Left, F=Frente/Front)

So "Fração C" and "1º D" both correctly described the same apartment - using different systems for different purposes. The letter "C" identified which legal unit it was; the letter "D" identified which side of the floor it was on. Two valid identifiers, same namespace (single uppercase letters), completely different meanings.

The tenant now had to contact all four utility providers to update the address. The confusion cost time, caused missed deliveries, and created administrative overhead - all because a single letter in an address could mean two different things depending on context.

**MECT violation:** Using the same symbol space (letters A-Z) for two unrelated classification systems (legal fractions vs floor positions) without explicit disambiguation. A better design would use distinct namespaces: "FR-C" for fraction, "1D" for floor position, or simply spell out "Fração C, Lado Direito" to make both systems explicit.

---

Emails do not have titles, they have subjects
People do not have emails, they get emails and have email addresses.
Flights do not have targets, they have destinations
People do not have names and surnames, they have first, middle and last names. A person's name cannot be composed of itself and a surname because this would introduce recursive logic.
A license plate does not identify a car, it identifies a license to drive a car and that car that might change.

Bad: "Can you please remove all asterisks and hyphens?"
Good: "Can you please remove the following characters: asterisk ('*' U+002A), hyphen-minus ('-' U+02D), minus sign ('-' U+2212)? U+xxxx is the unicode notation where xxxx is the hexadecimal character code.

Bad: Comma-separated list of all emails for mailing that will be sent out on a monthly basis to those customers who have ordered more than $1m over the last 2 years.
Good: Email adresses for Montly Very Important Customers Mailing (MVIC) in comma-separated format (e.g. "a@b.com,c@d.com"). VIC = customer who has generated more than USD 1 million turnover within the last 2 years.

Maybe it should be renamed to "Minimal Exclusive Explicit Consistent Terminology" because

This document should be rewritten in the pyramid form:

Title: Use MECT for better communication

Why?

1. Eliminates misunderstandings and feedback loops

How?

1.1. Eliminates homonyms (same word, different meaning) and separates and names fields of application (context)

Why is that good? Predictability, learning the structure of things, easier to remember

1.2. Keeps changes at a minimum

Why is that good? Predictability, safety, building blocks for other communication

1.3. Ensures that everything that is needed for action is communicated, expliciti

Why

2. Forces you to define your language and be predictable

## Examples

Bad: "The Determinants of the infant mortality rate in the United States."
Good: "How many babies did die in the United States of America between 1991 and 2004 and what where the main causes?"
Q1: What is a determinant? A: It means causes. Things that influence other things.
Q2: How do determinants affect things? A: A lot. Determinants are the major causes.
Q3: What are infants? A: Babies.
Q4: What does mortality mean? A: It means death.
Q5: What is a rate? A: How much of something.
Q6: How does it relate to mortality?
Q7: The United States of America or Mexico?

## Interesting Stuff

The following examples demonstrate how complex concepts are condensed into single words. These words can then be reused in new situations to precisely describe how a desired philosophy should be applied and what outcome is expected.

This is a centerpiece of Japanese world-class engineering: The language allows people to adapt and apply vast amounts of experience and knowledge in new contexts because the language can absorb these new words and acts as a wisdom compression and transport protocol.

Like in programming languages, entire frameworks can be reused in new kinds of software because they are designed according to a philosophy that can serve multiple purposes and ensure highest quality in all kinds of applications.

---

Sashimono was named after putting two wooden pieces together without using nails.It seems delicate, but we are using special techniques called "HOZO" which is using the hidden notch and groove to lock the two wooden pieces.

Sashimono has special feature which is using a few metal parts as possible and special technique called "Hukiurushi-shiage" which is coating and wiping with Japanese lacquer more than 10 times. Another point of Edo-Sashimono is one product made by one craftsman for whole process.

Sashimono classified into two, "KYO-SASHIMONO" and "EDO-SASHIMONO"

Dashi is a versatile ingredient that simply means 'stock' in Japan. That being said, it takes a bit of practice to know when to remove the kombu and bonito in order to extract the right amount of flavor. Plus, there's straining involved. Any recipe that calls for a strainer can't be entirely effortless. However, the main ingredient to watch out for in dashi is MSG.

MSG makes everything taste better but is something that the extremely health conscious will avoid. For anyone concerned regarding additives or trying to pursue a more natural diet any store bought dashi mixes that use this enhancer should be avoided, although it is rare find to be able to track down one that doesn't contain MSG ? they do exist, especially if you whip up your own in the kitchen at home. What exactly is MSG?

To help you understand the MSG component here is a quick explanation of why MSG can be a concern to some people. MSG is the sodium salt of glutamic acid, one of the most abundant naturally occurring non-essential amino acids. It has been classified by the U.S Food and Drug Administration as generally recognised as safe. MSG is used to improve the overall taste of certain foods, adding MSG means lowering the salt that is put into certain foods, as we all know excessive salt is a bad thing that can lead to instant side effects or on very rare occurrences complications later in life. MSG is safe when eaten at customary levels, but you have to keep a watchful eye over it as studies have shown that excess consumption can lead to headaches, heart palpitations, breathing difficulties, nausea and vomiting. Some tend to avoid MSG rich foods because they are sensitive to the additive, others don't see any side effects. Monitored and ingested in small doses MSG is categorised as perfectly safe. Imagine a food that not only has a wonderful natural power to transform a nice dish to a great dish, but is also great for you with numerous health benefits. Well, you're in luck because there is such a food and it has a rather

---

long but hopefully memorable name "katsuobushi". You may have come across this from time to time when enjoying Japanese food, perhaps you knew it, perhaps not. For many people, the first time katsuobushi catches their eye is when they are served a warm Japanese dish and see lots of something that looks a lot like pencil shavings wriggling about on their plate. Well, I for one remember such an experience and remember the joy of learning that nothing was still alive on my plate. Katsuobushi is dried bonito shavings and it is very, very, very good for you.

Kyudo is the Japanese martial art of archery. Experts in kyudo are referred to as kyudoka (弓道家). Kyudo is based on kyujutsu ("art of archery"), which originated with the samurai class of feudal Japan.[1] Kyudo is practised by thousands of people worldwide. As of 2005, the International Kyudo Federation had 132,760 graded members.[2]

Dojo[edit] Kyudo dojos (training halls, aka "kyudojo") vary in style and design from school to school, and from country to country. In Japan, most dojos have roughly the same layout; an entrance, a large dojo area, typically with a wooden floor and a high ceiling, a position for practice targets (Called makiwara), and a large open wall with sliding doors, which, when opened, overlooks an open grassy area and a separate building, the matoba which houses a sand hillock and the targets, placed 28 metres from the dojo floor. In kyudo there are three kinds of practice (geiko): mitori geiko - receiving with the eyes the style and technique of an advanced archer, kufu geiko - learning and keeping in mind the details of the technique and spiritual effort to realize it and kazu geiko - repetition through which the technique is personified in one's own shooting.[9]

Beginners start with a rubber practice bow and by practising the movements of hassetsu. The second step for a beginner is to do karabiki training with a bow without an arrow to learn handling of the bow and performing hassetsu until full draw. Handling and maintenance of the equipment is also part of the training. After given permission by the teacher beginners start practicing with the glove and arrow. Next steps may vary from teacher to teacher, but include practising first yugamae, then the draw and last release and shooting at makiwara. A beginner starting to shoot at the mato may be asked to shoot from half or three-quarters of the usual distance.[10]

Advanced beginners and advanced shooters practise shooting at makiwara, mato and some with omato.

A kyudoka practising on a makiwara

Makiwara is a specially designed straw target (not to be confused with makiwara used in karate). The makiwara is shot at from a very close range (about seven feet, or the length of the archer's strung yumi when held horizontally from the centerline of the archer's body). Because the target is so close and the shot most certainly will hit, the archer can concentrate on refining technique rather than on the arrow's arc.

Mato is the normal target for most kyudo practitioners. Mato sizes and shooting distances vary, but most common is hoshi mato thirty-six centimeters (or 12 sun, a traditional Japanese measurement equivalent to approximately 3.03 cm) in diameter shot at from a distance of twenty-eight metres. For competitions and examinations kasumi mato is used. For ceremonies it is most common to use hoshi mato which is the same as kasumi mato but with different markings.

Omato is the mato used for long distance enteki shooting at 60 m distance. The diameter of omato is 158 cm. There are separate competitions also for enteki shooting.[10]

There are three levels of skill:

Toteki, the arrow hits the target.

Kanteki, the arrow pierces the target.

Zaiteki, the arrow exists in the target.[11] (figuratively speaking)

---

## MECT Presentation Slides

### Slide 1: MECT Article Pyramid

```
1) Efficient Communication
2) Q: How to avoid errors, misunderstandings and feedback-loops?
3) A: By using the MECT principle.

4) Situation: Fuzzy, unclear and incomplete communication costs time, money and energy.

5) Complication: How can we avoid that? → 6) By using the MECT principle. → Why?

7) Because:
   A) Reduced complexity
   B) Easier communication
   C) Increased safety & predictability
   D) Less cost, more efficiency
```

### Slide 2: The MECT Principle Makes Communication More Efficient

| It reduces complexity | It increases accessibility | Predictable & safe | Reduces cost, increases efficiency |
|-|-|-|-|
| uses Conventions | Easy to learn | No ambiguities | Stable |
| fosters Consistent | Easy to understand | No duplicates | Interoperable |
| Reality-aligned | Easy to remember | No homonyms | Extendable |
| Less References | | | |

### Slide 3: Hall Of Fail - Name Collision

**Name collision in data structures:**

Bad: Column "Name" containing sub-columns "Name" and "Vorname" (recursive, ambiguous)
Good: Column "Name" containing "First Name" and "Last Name" (explicit, no collision)

**Bad request:**
> I noticed that for "Samsung Battery Charger" the availability date "10/11/2017" had a typo.

Problems: Missing identifier, non-ISO date, no explicit state change, no call to action

**Good request:**
> Please change the availability date for article number 87568752 "Samsung Battery Charger" from 2017-10-11 to 2017-11-10.

### Slide 4: Hall Of Fail - Ball Bearing

Name collision: Both the individual ball AND the entire bearing assembly are called "ball bearing". Without explicit terminology (e.g., "bearing ball" vs "ball bearing assembly"), confusion is inevitable.

### Slide 5: Hall Of Fail - Verbose Naming

**Bad:**
> The "Refresh" script cleans up the data by copying only the valid data into the new database. It creates a Migration logfile.

Problem: "refresh", "clean up", "migration", "copy valid data" all refer to the same procedure.

**Good:**
> The "DataCleanup" script creates a new database containing only valid data. It writes errors to the "DataCleanup" logfile.

**Good:**
> The "DropInvalidData" script creates a new database without invalid data. It writes errors to the "DropInvalidData" logfile.

**Principle:** So präzise wie möglich. So wenig wie nötig. / As precise as possible. As little as necessary.

### Slide 6: MECT Tools

```
                    Manuals, Specifications              Systems, Implementations
                    ─────────────────────────────────────────────────────────────────
Names [Identify]    avoid collisions, remove noise,      Objects & Properties
Codes, Acronyms,    distinguish states, ensure           Identifiers, Names, Syntax
Symbols, IDs,       referenceability, enable             Representation Primitives
Mnemonics, Icons    composability
                    ─────────────────────────────────────────────────────────────────
Lists [Group]       remove redundancies & duplicates,    Master Data & Views
Glossars, Dicts,    ensure exhaustiveness,               Table & Column Names,
Tables, References, ensure consistency,                  Column Types
Enumerations        synonyms & translations
                    ─────────────────────────────────────────────────────────────────
Models [Relate]     topology & proximity,                Data Representation
Hierarchies,        containment & traversability,        & UI Controls
Structures,         navigation efficiency                Data Models, Relations
Diagrams, Dep.cies
                    ─────────────────────────────────────────────────────────────────
Procedures [Execute] communication,                      Actions & Business Logic
How-Tos, Plans,     transactions & reversability,        Operational Data, View
Processes,          detect & validate states             Models, Update Mechanisms
Workflows
                    ─────────────────────────────────────────────────────────────────
        Audits, Assessments, Revisions    |    Tests, Code Reviews, Releases
```

### Slide 7: What is a Polyseme?

**Polysemy** is the capacity for a sign (word, phrase, or symbol) to have multiple meanings, usually related by contiguity of meaning within a semantic field. Polysemy is distinct from homonymy - which is an accidental similarity between two words (such as bear the animal, and the verb to bear); while homonymy is often a mere linguistic coincidence, polysemy is not.

**Martin Fowler (about Bounded Context):**
> "Early in my career I worked with a electricity utility - here the word 'meter' meant subtly different things to different parts of the organization: was it the connection between the grid and a location, the grid and a customer, the physical meter itself (which could be replaced if faulty). These subtle polysemes could be smoothed over in conversation but not in the precise world of computers. Time and time again I see this confusion recur with polysemes like 'Customer' and 'Product'."

### Slide 8: Plain Language (plainlanguage.gov)

- **Write for your audience.** Make sure you know who your audience is - don't guess or assume.

- **Organize.** State the document's purpose and its bottom line. Put the most important information at the beginning and include background information (when necessary) toward the end. Limit levels to three or fewer. Use lots of useful headings. Use question headings over statement headings over topic headings.

- **Address one person, not a group.** Write short sections. Avoid long, dense paragraphs.

- **Words matter.** They are the most basic building blocks of written and spoken communication. Choose your words carefully - be precise and concise. Verbs tell your audience what to *do*. Make sure they know *who* does what. Use active voice. Not "It must be done.", but "You must do it." Use passive voice when the law is the actor.

- **Use "must" for an obligation, "must not" for a prohibition, "may" for a discretionary action, and "should" for a recommendation.**

### Slide 9: Ambiguous Terms

Example: The word "Cardinality" has completely different meanings depending on context:

- **Cardinality (data modeling):** The relationship of one-to-many, many-to-many, one-to-one between tables
- **Cardinality (mathematics):** The number of elements in a set (e.g., set {2, 4, 6} has cardinality of 3)

Same word, different Wikipedia pages, different fields, different mental models. Without explicit context boundaries, confusion is guaranteed.

### Slide 10: Example for Term Unification (German Energy Sector)

**Problem:** Multiple overlapping terms for grid connection points: "Lieferstelle", "Entnahmestellen", "Einspeisestelle", "Ausspeisestelle", "Messstelle", "Zählpunkt" - often used synonymously and contradictorily.

**Solution (Feb 2018):** Two unified terms replaced all of them:

- **Marktlokation (MaLo-ID):** The billing/accounting point in the grid where electricity is withdrawn or fed in. A purely financial and accounting construct.

- **Messlokation:** The location of the actual physical measurement, delivering the measured values for electricity generated or consumed within the Marktlokation.

The old "Zählpunktbezeichnung" (meter point ID) continues to identify the Messlokation. This unification simplified and standardized market communication across the entire energy industry.

### Slide 11: Plain Language - Before/After Examples

**Wordiness**
- Bad: When the process of freeing a vehicle that has been stuck results in ruts or holes, the operator will fill the rut or hole created by such activity before removing the vehicle from the immediate area.
- Good: If you make a hole while freeing a stuck vehicle, you must fill the hole before you drive away.

**Confusing plural**
- Bad: Individuals and organizations wishing to apply must file applications with the appropriate offices in a timely manner.
- Good: You must apply at least 30 days before you need the certification. a. If you are an individual, apply at the State office in the State where you reside. b. If you are an organization, apply at the State office in the State where your headquarters is located.

**Address with "you"**
- Bad: The applicant must provide his or her mailing address and his or her identification number.
- Good: You must provide your mailing address and identification number.

**Informative headings**
- Bad: § 254.12 Applications.
- Good: § 254.12 How do I apply for a grant under this part?

### Slide 12: Plain Language - Voice and Verbs

**Active voice**
- Bad: The lake was polluted by the company.
- Good: The company polluted the lake.

**Active voice**
- Bad: Bonds will be withheld in cases of non-compliance with all permits and conditions.
- Good: We will withhold your bond if you don't comply with all permit terms and conditions.

**Simplest verb**
- Bad: These sections describe types of information that would satisfy the application requirements of Circular A-110 as it would apply to this grant program.
- Good: These sections tell you how to meet the requirements of Circular A-110 for this grant program.

**Avoid hidden verb**
- Bad: To trace the missing payment, we need to carry out a review of the Agency's accounts so we can gain an understanding of the reason the error occurred.
- Good: To trace the missing payment, we need to review the Agency's accounts so we understand the reason the error occurred.

**Avoid hidden verb**
- Bad: This means we must undertake the calculation of new figures for the congressional hearing.
- Good: This means we must calculate new figures for the congressional hearing.

### Slide 13: Plain Language - Avoid "shall"

- Bad: Where the land is occupied by a settler, the applicant shall serve notice on the settler by registered mail showing the amount and kind of timber he has applied for.
- Good: You must notify any settler, by registered mail, that you have applied to use timber from your lease. Include in your notice the amount and the kind of timber you intend to use as fuel.

### Slide 14: It's Not Just Semantics, It's Not the Same Thing

Words that sound similar but have different meanings - precision matters:

- Independence ≠ Interdependence
- Affect ≠ Effect
- Accuracy ≠ Precision
- Incest ≠ Incense
- Having judgement ≠ being judgemental
- Trainer ≠ Socializer ≠ Indoctrinator ≠ Educator
- Cunning ≠ Clever
- Corny ≠ Tacky
- Development (increase in capacity or capability) ≠ Growth (increase in size or number)
- Receiver ≠ Recipient
- Predater ≠ Predicator
- Travel Time ≠ Time Travel
- Simple ≠ simplistic
- Account (Issue) ≠ Account (Bank)

### Slide 15: Naming Problems

- **"EmptyCollectionKey"** → Is it the key of an empty collection, or is the key of the collection empty? → **"KeyOfEmptyCollection"** is better

- **Microsoft Teams naming collision:** When in Microsoft Teams I have more than 1 Team, what do I call this collection of objects? Do I say I have 3 Teams in Teams? My teams in Teams? What do I mean when I say "When I go to my Teams?"

### Slide 16: Naming and Describing Things - Structure

- **Start with most explicit name** → "Project Start Date", "Project End Date"

- **Identify variations and specifiers and put them before the name** → "Planned Project Start Date", "Approved Project Start Date", "Actual Project Start Date"

- **Identify states and conditions and put them after the name** → "Project Start Date Status" ("Planned", "Approved", etc.), "Planned Project Start Date Accepted" (TRUE/FALSE)

- **Define short/long Mnemonics and Aliases for internal/external usage** → external: ACTUAL_PROJECT_START_DATE, APSD → internal: START_DATE, SD

- **Describe naming and spelling rules according to domain coding styles**

### Slide 17: Naming and Describing Things - Description Types

**4 types of descriptions:**
- **Intentional description:** describes the intent that lead to the introduction of the object/idea
- **Functional description** ("black-box" view): describes how the intent is going to be achieved by modeling a function
- **Technical description** ("engine-room" view): describes how the function is going to be achieved
- **Contextual description:** describes structural or procedural dependencies and relations

**Naming procedures:**
- **By describing the Output** (This should be default)
  - "Generate Traffic Metrics" is better than "Analyze Traffic"
  - "Notify Pending Order Customers" is better than "Check Order State"
- **By describing the Input**
- **By describing the mechanism**

### Slide 18: When Writing Documents

- Provide heading numbers to make chapters and paragraphs referenceable
- Describe how information should be referenced and stick to standards if possible

### Slide 19: When Creating Lists

- Provide two identifiers per row: An index and a key
- Use topology by grouping related items together. As groups get more important, introduce indexes and keys for groups.

### Slide 20: Applied MECT

Real-world examples of MECT in practice:

- **Music** → The note system ("F#", "Ab") - precise, universal, minimal
- **Electronics** → Resistor Names, Part naming schemes - standardized identification across the industry
