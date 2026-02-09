// Resources data for motorcycle accident law site

export interface ResourceData {
  title: string;
  slug: string;
  description: string;
  category: "guide" | "checklist" | "legal" | "safety";
  icon: string;
  content: string;
  keyTakeaways: string[];
  relatedTopics: string[];
}

export const resources: ResourceData[] = [
  {
    title: "Motorcycle Accident Checklist",
    slug: "motorcycle-accident-checklist",
    description: "A step-by-step checklist of what to do immediately after a motorcycle accident to protect your health and legal rights.",
    category: "checklist",
    icon: "✅",
    content: `
## Immediate Actions (At the Scene)

### 1. Safety First
- Move to a safe location if possible
- Turn off your motorcycle to prevent fire
- Check yourself for injuries before moving
- Call 911 immediately

### 2. Document Everything
- Take photos of all vehicles involved
- Photograph road conditions, debris, skid marks
- Capture traffic signals, signs, and weather conditions
- Get photos of your injuries and gear damage

### 3. Exchange Information
- Get driver's license numbers
- Collect insurance information
- Write down license plate numbers
- Get contact info for all witnesses

### 4. What NOT to Do
- Don't admit fault or apologize
- Don't discuss the accident details with other drivers
- Don't refuse medical attention
- Don't post about the accident on social media

## Within 24-48 Hours

### Medical Care
- Get a complete medical examination
- Follow all treatment recommendations
- Keep all medical records and bills
- Document your pain levels daily

### Legal Protection
- Contact a motorcycle accident attorney
- Don't give recorded statements to insurance
- Preserve your damaged gear as evidence
- Request a copy of the police report

### Documentation
- Write down everything you remember
- Continue photographing your injuries
- Keep a recovery journal
- Save all receipts related to the accident
`,
    keyTakeaways: [
      "Call 911 and document everything at the scene",
      "Never admit fault or apologize",
      "Get medical attention even if you feel fine",
      "Contact an attorney before talking to insurance",
      "Preserve all evidence including damaged gear"
    ],
    relatedTopics: ["what-to-do-after-crash", "evidence-preservation", "dealing-with-insurance"]
  },
  {
    title: "What to Do After a Motorcycle Crash",
    slug: "what-to-do-after-crash",
    description: "Comprehensive guide on the immediate steps to take after a motorcycle accident to protect your health, rights, and potential compensation.",
    category: "guide",
    icon: "🚨",
    content: `
## The First Minutes Matter

The actions you take immediately after a motorcycle crash can significantly impact your health and any future legal claim. Here's what you need to know.

### Step 1: Assess Your Condition

Before anything else, take a moment to assess your injuries:
- Can you move all your limbs?
- Do you feel dizzy or confused?
- Is there any visible bleeding?
- Do you have difficulty breathing?

**Important:** Adrenaline can mask serious injuries. Many riders have walked around after crashes with broken bones or internal injuries they couldn't feel.

### Step 2: Call for Help

Dial 911 even if the accident seems minor:
- Police create an official accident report
- EMTs can identify hidden injuries
- Documentation starts immediately

### Step 3: Move to Safety (If Possible)

If you can safely move:
- Get off the roadway
- Move your motorcycle if it's creating a hazard
- Find a safe spot away from traffic

### Step 4: Gather Evidence

This is crucial for your legal case:
- Photograph everything from multiple angles
- Record a video walking around the scene
- Get witness names and phone numbers
- Note the exact time and location

### Step 5: Limit What You Say

- Give basic information to police
- Don't admit fault to anyone
- Don't discuss who caused the accident
- Don't give statements to the other driver's insurance

## The Days After Your Crash

### Medical Follow-Up
Even if you went to the ER, follow up with your doctor within 24-48 hours. Some injuries take time to manifest.

### Legal Consultation
Contact a motorcycle accident attorney before:
- Giving any recorded statements
- Signing any documents
- Accepting any settlement offers
- Posting anything on social media

### Preserve Evidence
- Don't repair your motorcycle yet
- Keep your damaged riding gear
- Save all receipts and documents
- Continue documenting your injuries
`,
    keyTakeaways: [
      "Adrenaline can mask serious injuries - always get checked",
      "Police reports are crucial for your claim",
      "Document everything with photos and video",
      "Never admit fault or sign anything without legal advice",
      "Follow up with doctors even after ER visits"
    ],
    relatedTopics: ["motorcycle-accident-checklist", "evidence-preservation", "medical-treatment-guide"]
  },
  {
    title: "Helmet Laws by State",
    slug: "helmet-laws-by-state",
    description: "State-by-state breakdown of motorcycle helmet laws, including universal helmet laws, partial requirements, and how helmet use affects your legal case.",
    category: "legal",
    icon: "⛑️",
    content: `
## Understanding Helmet Laws

Motorcycle helmet laws vary significantly across the United States. Understanding your state's requirements is important not just for compliance, but because helmet use can affect your personal injury claim.

## Universal Helmet Law States (19 states + DC)

These states require ALL motorcycle riders and passengers to wear helmets:

- Alabama, California, Georgia, Louisiana, Maryland
- Massachusetts, Mississippi, Missouri, Nebraska, Nevada
- New Jersey, New York, North Carolina, Oregon, Tennessee
- Vermont, Virginia, Washington, West Virginia
- District of Columbia

## Partial Helmet Law States (28 states)

These states require helmets for certain riders (usually under 18 or 21):

**Under 18:**
- Alaska, Arizona, Colorado, Hawaii, Idaho
- Indiana, Kansas, Maine, Minnesota, Montana
- New Mexico, North Dakota, Ohio, Oklahoma, South Dakota
- Utah, Wisconsin, Wyoming

**Under 21:**
- Arkansas, Delaware, Florida, Kentucky, Michigan
- Pennsylvania, Rhode Island, South Carolina, Texas

## No Helmet Law States (3 states)

- Illinois
- Iowa
- New Hampshire

## How Helmet Use Affects Your Case

### Contributory Negligence
In some states, not wearing a helmet can reduce your compensation if you suffered head injuries. The defense may argue you contributed to your own injuries.

### Comparative Fault
Many states use comparative negligence, where your compensation may be reduced by your percentage of fault. Not wearing a helmet could be considered partial fault for head injuries.

### Best Practice
Regardless of the law, wearing a DOT-approved helmet significantly reduces your risk of fatal head injury and strengthens your legal position if you're in an accident.
`,
    keyTakeaways: [
      "19 states plus DC require all riders to wear helmets",
      "28 states have partial helmet laws based on age",
      "3 states have no helmet requirements at all",
      "Not wearing a helmet can reduce your compensation",
      "Always wear a DOT-approved helmet regardless of law"
    ],
    relatedTopics: ["gear-guide", "lane-splitting-laws"]
  },
  {
    title: "Lane Splitting Laws",
    slug: "lane-splitting-laws",
    description: "Complete guide to lane splitting and lane filtering laws across the US, including where it's legal, where it's illegal, and pending legislation.",
    category: "legal",
    icon: "🛣️",
    content: `
## What is Lane Splitting?

Lane splitting (also called lane sharing, white-lining, or filtering) is the practice of riding a motorcycle between lanes of slow-moving or stopped traffic. Lane filtering typically refers to moving between lanes at a stoplight.

## Where Lane Splitting is Legal

### California
The only state where lane splitting is explicitly legal. Guidelines recommend:
- Traffic speed under 30 mph
- Motorcycle speed no more than 10 mph faster than traffic
- Avoid splitting near large vehicles, on curves, or at exits

### Montana
Lane filtering is legal when:
- Traffic is stopped
- Speed limit is 50 mph or less
- Motorcycle travels no more than 20 mph

### Utah
Lane filtering (not splitting) is legal when:
- Traffic is stopped
- Speed limit is 45 mph or less
- Motorcycle travels no more than 15 mph

### Arizona
Lane filtering is legal when:
- Traffic is stopped
- Speed limit is 45 mph or less
- Motorcycle travels no more than 15 mph

## Where Lane Splitting is Illegal

Lane splitting is explicitly illegal or not addressed (therefore risky) in all other states. Getting caught can result in:
- Traffic citations
- Fines
- Points on your license
- Complications with insurance claims if in an accident

## Pending Legislation

Several states have considered lane splitting or filtering bills:
- Texas, Oregon, Washington, Connecticut, Maryland, Massachusetts

Check current legislation in your state, as laws are evolving.

## If You're in a Lane Splitting Accident

If you were lane splitting when an accident occurred:
- Document that you were following safe practices
- Note traffic conditions and your speed
- Consult with a motorcycle accident attorney
- In California, safe lane splitting shouldn't affect your claim
- In other states, it may complicate your case
`,
    keyTakeaways: [
      "California is the only state where lane splitting is fully legal",
      "Montana, Utah, and Arizona allow lane filtering under specific conditions",
      "Lane splitting is illegal or unaddressed in most states",
      "Safe lane splitting practices are important for your legal case",
      "Laws are evolving - check your state's current legislation"
    ],
    relatedTopics: ["helmet-laws-by-state", "insurance-guide"]
  },
  {
    title: "Motorcycle Gear Guide for Safety",
    slug: "gear-guide",
    description: "Essential motorcycle safety gear guide covering helmets, jackets, pants, boots, and gloves - what to look for and why it matters for crashes and claims.",
    category: "safety",
    icon: "🦺",
    content: `
## Why Gear Matters

Proper motorcycle gear can be the difference between walking away from a crash and life-changing injuries. It also matters for your legal case - proper gear shows you were a responsible rider.

## The Essential Gear

### Helmets 🪖
The most important piece of gear.

**What to Look For:**
- DOT certification (minimum standard)
- Snell certification (higher standard)
- ECE 22.05 certification (European standard)
- Proper fit - snug but not uncomfortable
- Full-face for maximum protection

**Why It Matters:**
Helmets reduce fatal head injury risk by 37% and head injury risk by 69%.

### Jackets 🧥
Protection for your torso, back, and arms.

**What to Look For:**
- CE-rated armor in shoulders, elbows, back
- Abrasion-resistant material (leather or textile)
- High-visibility colors or reflective elements
- Proper ventilation for comfort
- Secure closure system

### Pants 👖
Your legs are vulnerable in crashes.

**What to Look For:**
- CE-rated knee and hip armor
- Reinforced seams and slide zones
- Connection points to jacket
- Riding jeans with Kevlar at minimum

### Boots 👢
Protect your feet and ankles.

**What to Look For:**
- Above-ankle height
- Reinforced toe and heel
- Oil-resistant sole
- Secure closure (no laces to catch)
- CE certification for impact protection

### Gloves 🧤
Your hands hit the ground first in most crashes.

**What to Look For:**
- Knuckle protection
- Palm sliders
- Secure wrist closure
- Proper fit for control operation

## Gear and Your Legal Case

Wearing proper gear demonstrates responsible riding:
- Shows you took reasonable precautions
- Reduces severity of injuries (lowering medical costs)
- Defeats arguments about contributory negligence
- Gear condition documents crash severity

**Always preserve your damaged gear as evidence after a crash.**
`,
    keyTakeaways: [
      "Helmets reduce fatal head injury risk by 37%",
      "Look for CE-rated armor in jackets and pants",
      "Boots should be above-ankle with reinforced areas",
      "Proper gear demonstrates responsible riding",
      "Preserve damaged gear as evidence after crashes"
    ],
    relatedTopics: ["helmet-laws-by-state", "motorcycle-accident-checklist", "evidence-preservation"]
  },
  {
    title: "Motorcycle Insurance Guide",
    slug: "insurance-guide",
    description: "Understanding motorcycle insurance coverage types, requirements, and how to ensure you're protected if you're in an accident.",
    category: "guide",
    icon: "📋",
    content: `
## Types of Motorcycle Insurance

Understanding your coverage options is essential before and after an accident.

### Liability Coverage
**Required in most states**

Covers damage and injuries you cause to others:
- Bodily Injury Liability: Medical costs, lost wages, pain and suffering for others
- Property Damage Liability: Repairs to other vehicles and property

**Recommendation:** Carry more than state minimums. Minimum coverage often isn't enough.

### Collision Coverage
**Optional but recommended**

Covers damage to your motorcycle when you hit another vehicle or object, regardless of fault.

### Comprehensive Coverage
**Optional but recommended**

Covers non-collision damage:
- Theft
- Vandalism
- Fire
- Natural disasters
- Animal collisions

### Uninsured/Underinsured Motorist (UM/UIM)
**Critical coverage**

Protects you when the other driver:
- Has no insurance
- Has insufficient insurance
- Flees the scene (hit-and-run)

**This is possibly the most important coverage you can have.** Many drivers are uninsured or underinsured.

### Medical Payments (MedPay)
Covers your medical expenses regardless of fault. Pays quickly without waiting for claim resolution.

### Personal Injury Protection (PIP)
In no-fault states, covers:
- Medical expenses
- Lost wages
- Essential services
- Funeral expenses

## What Coverage Do You Need?

**Minimum Recommendation:**
- State minimum liability (preferably higher)
- Uninsured/Underinsured Motorist coverage
- Medical Payments coverage

**Ideal Coverage:**
- 100/300/100 liability coverage
- Matching UM/UIM coverage
- Collision and comprehensive
- MedPay or PIP
- Accessory coverage for gear and modifications

## After an Accident

- Report the accident to your insurance promptly
- Don't accept quick settlements
- Understand your policy limits
- Consider how each coverage applies
- Consult an attorney before recorded statements
`,
    keyTakeaways: [
      "Liability coverage is required but minimums often aren't enough",
      "Uninsured/Underinsured Motorist coverage is critical",
      "Medical Payments provides quick payment regardless of fault",
      "Review your policy annually and after any changes",
      "Consult an attorney before accepting any settlement"
    ],
    relatedTopics: ["dealing-with-insurance", "what-to-do-after-crash"]
  },
  {
    title: "Evidence Preservation Guide",
    slug: "evidence-preservation",
    description: "How to preserve critical evidence after a motorcycle accident to strengthen your legal case and maximize compensation.",
    category: "guide",
    icon: "📸",
    content: `
## Why Evidence Matters

Evidence is the foundation of your motorcycle accident case. Strong evidence:
- Proves who was at fault
- Documents the severity of your injuries
- Establishes your damages
- Prevents disputes about what happened

## At the Accident Scene

### Photographs to Take
- All vehicles from multiple angles
- License plates
- Damage details (close-ups)
- Skid marks and road debris
- Traffic signs and signals
- Weather and road conditions
- Your injuries
- Your damaged gear

### Video Documentation
- Walk around recording the entire scene
- Capture the surrounding area
- Record any visible injuries
- Note the date and time verbally

### Witness Information
- Full names and phone numbers
- Email addresses if possible
- Brief description of what they saw
- Note where they were standing

## Physical Evidence to Preserve

### Your Motorcycle
- Don't repair it before documentation
- Request photos from the repair shop
- Keep all damaged parts
- Preserve the condition as evidence

### Your Gear
- Helmet (keep even if damaged)
- Jacket, pants, gloves, boots
- Any clothing worn during crash
- Keep items in a clean, dry place
- Don't wash or repair anything

### Medical Evidence
- All hospital records
- Imaging (X-rays, MRIs, CT scans)
- Prescriptions and medications
- Medical bills and receipts
- Doctor's notes and recommendations

## Digital Evidence

### Request These Records
- Police accident report
- 911 call recordings
- Traffic camera footage
- Nearby business surveillance video
- Cell phone records (of other driver)

### Your Own Documentation
- Screenshot any relevant social media posts
- Download your dashcam/helmet cam footage
- Back up all photos to cloud storage
- Create a written timeline of events

## Ongoing Documentation

### Keep a Recovery Journal
- Daily pain levels (1-10 scale)
- Activities you cannot do
- Emotional and mental health notes
- Sleep quality
- Medication effects

### Financial Records
- All medical bills
- Lost wage documentation
- Travel expenses for treatment
- Home modification costs
- Any accident-related expenses
`,
    keyTakeaways: [
      "Photograph everything at the scene from multiple angles",
      "Preserve your motorcycle and gear without repairs",
      "Request traffic camera and surveillance footage quickly",
      "Keep a daily recovery journal",
      "Store all evidence securely with backups"
    ],
    relatedTopics: ["motorcycle-accident-checklist", "what-to-do-after-crash", "dealing-with-insurance"]
  },
  {
    title: "Dealing with Insurance Companies",
    slug: "dealing-with-insurance",
    description: "What to expect from insurance companies after a motorcycle accident and how to protect yourself from common tactics that reduce your settlement.",
    category: "guide",
    icon: "🏦",
    content: `
## The Truth About Insurance Companies

Insurance companies are businesses focused on profit. Their goal is to:
- Pay as little as possible on claims
- Settle quickly before you know your full damages
- Find reasons to deny or reduce claims
- Protect their insured (not you)

Understanding their tactics helps you protect yourself.

## Common Insurance Company Tactics

### Quick Settlement Offers
**The Tactic:** Offering fast cash before you know the extent of your injuries.

**Your Protection:** Never accept early settlement offers. Many injuries take weeks or months to fully manifest.

### Recorded Statements
**The Tactic:** Asking for a recorded statement to find inconsistencies they can use against you.

**Your Protection:** Politely decline until you speak with an attorney. You're not required to give a recorded statement to the other driver's insurance.

### Blame Shifting
**The Tactic:** Suggesting you were partially at fault, reducing their payout.

**Your Protection:** Document everything and don't admit any fault. Let the evidence speak.

### Medical Records Fishing
**The Tactic:** Requesting broad access to your medical history to find pre-existing conditions.

**Your Protection:** Only authorize release of records related to accident injuries. Consult an attorney before signing releases.

### Lowball Offers
**The Tactic:** Making an initial offer far below fair value, hoping you'll negotiate up only slightly.

**Your Protection:** Know your claim's value before negotiating. An attorney can provide a realistic range.

### Delay Tactics
**The Tactic:** Dragging out the process hoping you'll give up or accept less due to financial pressure.

**Your Protection:** An attorney can apply pressure and file suit if necessary.

## What to Do

### DO:
- Report the accident to your own insurance
- Document everything
- Keep all receipts and records
- Consult an attorney before negotiating
- Be patient - good settlements take time

### DON'T:
- Give recorded statements without an attorney
- Accept the first offer
- Sign broad medical releases
- Post about your accident on social media
- Admit fault to anyone

## When to Get an Attorney

Consider hiring a motorcycle accident attorney if:
- You have significant injuries
- Fault is disputed
- Multiple parties are involved
- Insurance is offering a low settlement
- You're unsure of your claim's value
- The insurance company is delaying

**Most motorcycle accident attorneys work on contingency - no fee unless you win.**
`,
    keyTakeaways: [
      "Insurance companies prioritize profit over fair settlements",
      "Never accept quick settlement offers before knowing full damages",
      "Don't give recorded statements without attorney guidance",
      "Be cautious about signing medical release forms",
      "Most motorcycle attorneys work on contingency - no upfront cost"
    ],
    relatedTopics: ["insurance-guide", "evidence-preservation", "what-to-do-after-crash"]
  },
  {
    title: "Medical Treatment After a Motorcycle Accident",
    slug: "medical-treatment-guide",
    description: "Guide to getting proper medical care after a motorcycle accident, understanding common injuries, and how medical documentation affects your legal case.",
    category: "guide",
    icon: "🏥",
    content: `
## Why Medical Treatment Matters

Proper medical treatment after a motorcycle accident is crucial for two reasons:
1. Your health and recovery
2. Your legal case

Gaps in treatment or refusing care can be used against you to claim your injuries aren't serious.

## Immediate Medical Care

### Emergency Room
Go to the ER if you experience:
- Any loss of consciousness
- Severe pain anywhere
- Difficulty breathing
- Numbness or tingling
- Visible injuries or bleeding
- Confusion or disorientation
- Nausea or vomiting

**Even if you feel "fine," adrenaline masks injuries. Get checked.**

### What to Tell Medical Staff
- This is from a motorcycle accident
- Describe all symptoms, even minor ones
- Mention any pain, no matter how slight
- Be honest about mechanism of injury

## Common Motorcycle Accident Injuries

### Head and Brain Injuries
- Concussions
- Traumatic brain injury (TBI)
- Skull fractures
- Cognitive impairment

### Spinal Injuries
- Herniated discs
- Spinal cord damage
- Vertebral fractures
- Paralysis

### Orthopedic Injuries
- Broken bones
- Joint dislocations
- Ligament tears
- Fractures requiring surgery

### Soft Tissue Injuries
- Road rash (severe burns)
- Muscle tears
- Internal organ damage
- Nerve damage

### Psychological Injuries
- PTSD
- Anxiety
- Depression
- Fear of riding

## Follow-Up Care

### Within 24-48 Hours
- See your primary care doctor
- Follow all ER recommendations
- Start any prescribed therapy

### Ongoing Treatment
- Attend all appointments
- Follow treatment plans exactly
- Don't skip or reschedule
- Document your progress

### Specialists You May Need
- Orthopedic surgeon
- Neurologist
- Physical therapist
- Pain management specialist
- Mental health professional

## Medical Documentation for Your Case

**Critical Records:**
- ER admission and discharge papers
- Imaging results (X-rays, MRI, CT)
- Surgery reports
- Doctor's notes at each visit
- Physical therapy progress notes
- Prescription records
- Billing statements

**Keep Everything:**
- Make copies of all documents
- Request records in writing
- Organize chronologically
- Note any recommendations you followed
`,
    keyTakeaways: [
      "Always get medical attention after an accident - adrenaline masks injuries",
      "Document all symptoms, even minor ones",
      "Follow all treatment plans without gaps",
      "Keep copies of all medical records and bills",
      "Mental health treatment is valid and documentable"
    ],
    relatedTopics: ["what-to-do-after-crash", "evidence-preservation", "dealing-with-insurance"]
  }
];

// Helper functions
export function getResourceBySlug(slug: string): ResourceData | undefined {
  return resources.find(r => r.slug === slug);
}

export function getResourcesByCategory(category: ResourceData["category"]): ResourceData[] {
  return resources.filter(r => r.category === category);
}

export function getAllResourceSlugs(): string[] {
  return resources.map(r => r.slug);
}
