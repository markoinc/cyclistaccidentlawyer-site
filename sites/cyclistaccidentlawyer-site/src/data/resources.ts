// Resources data for pedestrian accident law site

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
    title: "Pedestrian Accident Checklist",
    slug: "pedestrian-accident-checklist",
    description: "A step-by-step checklist of what to do immediately after being hit as a pedestrian to protect your health and legal rights.",
    category: "checklist",
    icon: "✅",
    content: `
## Immediate Actions (At the Scene)

### 1. Safety First
- Stay where you are if seriously injured - don't try to move
- If able to move, get to a safe location away from traffic
- Call 911 immediately
- Accept medical attention even if injuries seem minor

### 2. Document Everything
- Take photos of the scene from multiple angles
- Photograph the vehicle that hit you, including license plate
- Capture traffic signals, crosswalks, signs, and road conditions
- Take photos of your injuries and any damage to personal items

### 3. Gather Information
- Get the driver's license, insurance, and contact information
- Collect names and phone numbers of all witnesses
- Note the exact location (intersection, address, landmarks)
- Record the time of the accident

### 4. What NOT to Do
- Don't apologize or admit any fault
- Don't give statements to the driver's insurance
- Don't sign anything at the scene
- Don't refuse medical attention
- Don't leave the scene before police arrive

## Within 24-48 Hours

### Medical Care
- Get a complete medical examination (ER if needed)
- Follow all treatment recommendations
- Tell doctors all symptoms, no matter how minor
- Keep all medical records and bills

### Legal Protection
- Contact a pedestrian accident attorney
- Don't give recorded statements to any insurance company
- Request a copy of the police report
- Continue documenting your injuries daily

### Documentation
- Write down everything you remember while fresh
- Continue photographing your injuries as they develop
- Keep a recovery journal noting pain levels
- Save all receipts related to the accident
`,
    keyTakeaways: [
      "Call 911 and get medical attention immediately",
      "Document everything with photos and notes",
      "Never admit fault or apologize",
      "Contact an attorney before talking to insurance",
      "Get medical care even if you feel 'fine'"
    ],
    relatedTopics: ["what-to-do-after-hit", "evidence-preservation", "dealing-with-insurance"]
  },
  {
    title: "What to Do After Being Hit by a Car",
    slug: "what-to-do-after-hit",
    description: "Comprehensive guide on the immediate steps to take after being hit by a car as a pedestrian.",
    category: "guide",
    icon: "🚨",
    content: `
## The First Minutes After Being Hit

The moments after being struck by a vehicle are critical for both your health and any future legal claim. Here's what you need to know.

### Step 1: Stay Calm and Assess

If you're conscious after being hit:
- Don't try to get up immediately
- Check yourself for obvious injuries
- Be aware that adrenaline may mask serious injuries
- Wait for emergency responders if seriously hurt

**Warning:** Many pedestrian accident victims have walked around with broken bones, internal bleeding, or head injuries they couldn't feel due to shock.

### Step 2: Get to Safety (If Possible)

If you can safely move:
- Get to the sidewalk or out of traffic
- Don't try to chase the vehicle if they flee
- Find a safe spot to wait for help

### Step 3: Call 911

Always call police, even for "minor" accidents:
- Creates official documentation
- EMTs can identify hidden injuries
- Police report crucial for insurance claims
- Driver cannot later deny the accident

### Step 4: Gather Evidence

If physically able:
- Photograph everything at the scene
- Get the driver's information
- Ask witnesses to stay or get their contact info
- Note traffic signals, weather, lighting

### Step 5: Seek Medical Attention

Even if you feel okay:
- Adrenaline masks pain
- Internal injuries may not be immediately apparent
- Head injuries often have delayed symptoms
- Medical records link injuries to accident

## Days After the Accident

### Follow Up With Doctors
- See your primary care physician within 48 hours
- Follow all recommended treatments
- Don't skip appointments

### Protect Your Rights
- Don't give statements to the other driver's insurance
- Contact a pedestrian accident attorney
- Keep a daily journal of your recovery
- Save every receipt and document

### Avoid These Mistakes
- Posting about the accident on social media
- Accepting quick settlement offers
- Signing medical authorization forms from insurance
- Missing medical appointments
`,
    keyTakeaways: [
      "Stay calm and don't move if seriously injured",
      "Always call 911 and wait for police",
      "Get medical attention even if you feel fine",
      "Document everything you can at the scene",
      "Don't give statements to the other driver's insurance"
    ],
    relatedTopics: ["pedestrian-accident-checklist", "evidence-preservation", "medical-treatment-guide"]
  },
  {
    title: "Crosswalk Laws by State",
    slug: "crosswalk-laws-by-state",
    description: "State-by-state breakdown of pedestrian crosswalk laws and how they affect your right-of-way and legal case.",
    category: "legal",
    icon: "🚶",
    content: `
## Understanding Crosswalk Laws

Crosswalk laws determine who has the right-of-way and can significantly affect liability in pedestrian accident cases.

## Key Crosswalk Concepts

### Marked vs. Unmarked Crosswalks
In most states, crosswalks exist at every intersection, whether marked with paint or not. An "unmarked crosswalk" is the natural extension of the sidewalk across the intersection.

### States Where Every Intersection is a Crosswalk
- California
- Oregon
- Washington
- And most other states

### Driver Duties at Crosswalks
In virtually all states, drivers must:
- Yield or stop for pedestrians in crosswalks
- Not overtake vehicles stopped for pedestrians
- Exercise due care to avoid hitting pedestrians

## Strong Crosswalk Law States

These states have particularly strong pedestrian protections:

**California** - Every intersection is a crosswalk. Drivers must yield to pedestrians in any crosswalk, marked or unmarked.

**New York** - Drivers must yield to pedestrians in crosswalks. NYC has additional local protections.

**Oregon** - Every intersection is a crosswalk. Drivers must stop, not just slow down.

**New Jersey** - Drivers must stop and remain stopped for pedestrians. Heavy fines for violations.

**Maine** - Strong crosswalk laws with significant fines for failure to yield.

## Pedestrian Duties

Even with right-of-way, pedestrians typically must:
- Not suddenly leave a curb into the path of a vehicle
- Obey traffic signals where present
- Use crosswalks where available within reasonable distance
- Exercise due care for their own safety

## How Crosswalk Laws Affect Your Case

### If You Were in a Crosswalk
- Clear right-of-way supports your claim
- Driver has duty to yield
- Liability usually favorable to pedestrian

### If You Were Outside a Crosswalk
- May need to prove driver still was negligent
- Comparative fault may reduce your recovery
- Driver still has duty of due care

### Jaywalking
- Crossing outside a crosswalk doesn't automatically bar your claim
- Driver still must exercise reasonable care
- Comparative negligence may apply
`,
    keyTakeaways: [
      "Most states consider every intersection a crosswalk",
      "Drivers must yield to pedestrians in crosswalks",
      "Crossing outside a crosswalk doesn't eliminate your rights",
      "Strong crosswalk states include CA, NJ, OR, ME",
      "Pedestrians still have duties even with right-of-way"
    ],
    relatedTopics: ["pedestrian-right-of-way", "comparative-fault", "proving-fault"]
  },
  {
    title: "Pedestrian Safety Tips",
    slug: "pedestrian-safety-tips",
    description: "Essential safety tips for pedestrians to reduce accident risk and stay safe while walking.",
    category: "safety",
    icon: "⚠️",
    content: `
## Staying Safe as a Pedestrian

With pedestrian fatalities at 40-year highs, following safety practices is more important than ever.

## Crossing Streets Safely

### At Intersections
- Always use crosswalks when available
- Wait for the walk signal before crossing
- Look left, right, and left again before stepping off the curb
- Make eye contact with drivers before crossing
- Continue watching for vehicles while crossing

### Mid-Block Crossings
- Only cross at designated crosswalks or corners
- If you must cross mid-block, yield to all vehicles
- Never assume drivers see you

## Visibility Matters

### During Day
- Wear bright, visible clothing
- Make eye contact with drivers
- Stay alert and aware of your surroundings

### At Night
- Wear reflective clothing or accessories
- Carry a flashlight
- Avoid dark clothing
- Walk in well-lit areas
- Be extra cautious - you're much harder to see

## Distraction Dangers

### Avoid
- Texting while walking
- Wearing headphones that block traffic sounds
- Talking on the phone in crosswalks
- Looking at your phone instead of traffic

**Hawaii is the first state to ban distracted walking.**

## Alcohol and Pedestrians

Nearly half of fatal pedestrian crashes involve alcohol - either the driver, pedestrian, or both.

- Don't walk along roads while intoxicated
- Use rideshare services instead
- Stay on sidewalks
- Be extra careful at night

## Special Situations

### Parking Lots
- Walk in designated pedestrian lanes
- Be visible and make eye contact with drivers
- Watch for backing vehicles
- Stay alert - drivers are distracted

### School Zones
- Use crossing guards when available
- Cross only at designated crossings
- Watch for turning vehicles

### Construction Zones
- Follow temporary pedestrian routes
- Don't take shortcuts through work areas
- Be alert for construction vehicles

## Teaching Children

- Hold hands with young children
- Teach them to stop at curbs
- Practice looking both ways
- Explain that cars can't stop quickly
- Never let children play near streets
`,
    keyTakeaways: [
      "Always use crosswalks and obey signals",
      "Make eye contact with drivers before crossing",
      "Wear bright or reflective clothing, especially at night",
      "Put away your phone when crossing streets",
      "Never assume a driver sees you"
    ],
    relatedTopics: ["crosswalk-laws-by-state", "child-pedestrian-safety", "night-walking-safety"]
  },
  {
    title: "Pedestrian Insurance Guide",
    slug: "insurance-guide",
    description: "Understanding insurance coverage for pedestrian accidents, including what policies may cover your injuries.",
    category: "guide",
    icon: "📋",
    content: `
## Insurance Coverage for Pedestrian Accidents

Understanding what insurance covers pedestrian accidents can be complex. Multiple policies may apply to your injuries.

## Driver's Liability Insurance

### What It Covers
The at-fault driver's liability insurance should cover:
- Medical expenses
- Lost wages
- Pain and suffering
- Property damage (phone, clothes, etc.)

### Typical Limits
Minimum liability limits vary by state, typically ranging from $15,000 to $50,000 per person. These minimums are often inadequate for serious injuries.

## Your Own Coverage Options

### Health Insurance
- Covers your medical treatment
- May seek reimbursement from accident settlement
- Provides immediate coverage while claim is pending

### Uninsured Motorist (UM) Coverage
- Applies if you're hit by a driver with no insurance
- Applies to hit-and-run accidents
- Usually part of your auto insurance policy
- **Critical coverage for pedestrians**

### Underinsured Motorist (UIM) Coverage
- Applies when driver's insurance is insufficient
- Kicks in after driver's limits exhausted
- Usually part of your auto policy

### Medical Payments Coverage (MedPay)
- Pays your medical expenses regardless of fault
- No deductible typically
- Part of your auto policy
- Quick payment while claim proceeds

### Personal Injury Protection (PIP)
- Required in "no-fault" states
- Covers medical expenses and lost wages
- Part of your auto policy
- Pays regardless of who caused the accident

## No-Fault States

In no-fault states (Florida, Michigan, New York, etc.), your own PIP insurance may be primary:
- Covers your injuries first
- Regardless of who was at fault
- May limit your ability to sue driver

## Umbrella Policies

Some drivers carry umbrella policies that provide additional coverage:
- Extra liability above standard limits
- Often $1,000,000 or more
- Important for serious injury cases

## Steps to Take

1. **Identify all applicable policies**
   - Driver's liability insurance
   - Your health insurance
   - Your auto insurance (UM/UIM, MedPay, PIP)
   - Any umbrella policies

2. **File claims appropriately**
   - Report to driver's insurance
   - Notify your own insurance
   - Consult attorney before recorded statements

3. **Don't accept quick settlements**
   - Full extent of injuries may not be known
   - Initial offers typically too low
   - Consult attorney first
`,
    keyTakeaways: [
      "Multiple insurance policies may cover your injuries",
      "Uninsured motorist coverage is critical for pedestrians",
      "Your own auto insurance may apply even on foot",
      "No-fault states have special rules",
      "Never accept a quick settlement without legal advice"
    ],
    relatedTopics: ["dealing-with-insurance", "uninsured-motorist-claims", "what-to-do-after-hit"]
  },
  {
    title: "Evidence Preservation Guide",
    slug: "evidence-preservation",
    description: "How to preserve critical evidence after a pedestrian accident to strengthen your legal case.",
    category: "guide",
    icon: "📸",
    content: `
## Why Evidence Matters

Evidence is the foundation of your pedestrian accident case. Strong evidence:
- Proves who was at fault
- Documents injury severity
- Establishes your damages
- Prevents disputes about what happened

## At the Accident Scene

### Photographs to Take
- The vehicle from all angles
- License plate clearly visible
- Vehicle damage
- Crosswalk and traffic signals
- Any skid marks or debris
- Road conditions and lighting
- Your injuries
- Your damaged belongings

### Video Documentation
- Walk around recording the scene
- Capture traffic light timing
- Note conditions verbally
- Include date/time stamp

### Witness Information
- Full names and phone numbers
- Email addresses
- Brief description of what they saw
- Where they were standing

## Physical Evidence to Preserve

### Your Belongings
- Damaged clothing (don't wash)
- Damaged shoes
- Broken phone or electronics
- Damaged bags or personal items
- Keep everything in original condition

### Medical Evidence
- All hospital records
- Imaging (X-rays, CT scans, MRIs)
- Surgery reports
- Physical therapy records
- Prescriptions and medications
- All medical bills

## Digital Evidence

### Request These Records
- Police accident report
- 911 call recordings
- Traffic camera footage
- Nearby business surveillance video
- Cell phone records of driver

### Act Quickly
- Video footage may be overwritten quickly
- Business surveillance often erased after 30 days
- Traffic camera footage may not be kept long
- Preserve requests must be made promptly

## Ongoing Documentation

### Keep a Recovery Journal
- Daily pain levels (1-10)
- Activities you can't do
- Sleep quality
- Emotional and mental effects
- Medication effects

### Financial Records
- All medical bills
- Lost wage documentation
- Transportation costs for treatment
- Home care expenses
- Any accident-related expenses
`,
    keyTakeaways: [
      "Photograph everything at the scene",
      "Preserve damaged clothing and belongings without washing",
      "Request surveillance footage immediately",
      "Keep a daily recovery journal",
      "Store all evidence securely with backups"
    ],
    relatedTopics: ["pedestrian-accident-checklist", "what-to-do-after-hit", "dealing-with-insurance"]
  },
  {
    title: "Dealing with Insurance Companies",
    slug: "dealing-with-insurance",
    description: "What to expect from insurance companies after a pedestrian accident and how to protect yourself.",
    category: "guide",
    icon: "🏦",
    content: `
## The Truth About Insurance Companies

Insurance companies are businesses focused on profit. Their goal is to:
- Pay as little as possible
- Settle quickly before you know full damages
- Find reasons to deny or reduce claims
- Shift blame to you

## Common Insurance Tactics

### Quick Settlement Offers
**The Tactic:** Offering fast cash before you know injury extent.

**Your Protection:** Never accept early settlement offers. Many injuries take weeks to fully manifest.

### Recorded Statements
**The Tactic:** Asking for recorded statements to find inconsistencies.

**Your Protection:** Politely decline until you speak with an attorney. You're not required to give one.

### Blame Shifting
**The Tactic:** Suggesting you were at fault (jaywalking, distraction, etc.).

**Your Protection:** Don't admit any fault. Let evidence speak.

### Surveillance
**The Tactic:** Watching your social media and activities.

**Your Protection:** Stay off social media. Don't post about your accident or activities.

### Delaying Tactics
**The Tactic:** Dragging out the process hoping you'll give up.

**Your Protection:** An attorney can apply pressure and file suit if needed.

## What to Do

### DO:
- Report the accident to police
- Get medical attention immediately
- Document everything
- Consult an attorney before negotiating
- Be patient - good settlements take time

### DON'T:
- Give recorded statements without an attorney
- Accept the first offer
- Sign broad medical releases
- Post about your accident on social media
- Admit fault to anyone
- Guess about facts you don't remember

## When to Get an Attorney

Consider hiring a pedestrian accident attorney if:
- You have serious injuries
- Fault is disputed
- Insurance is delaying or denying
- You're being offered a low settlement
- You're unsure of your claim's value

**Most pedestrian accident attorneys work on contingency - no fee unless you win.**
`,
    keyTakeaways: [
      "Insurance companies prioritize profit over fair settlements",
      "Never accept quick settlements before knowing full injuries",
      "Don't give recorded statements without an attorney",
      "Stay off social media during your claim",
      "Most attorneys work on contingency - no upfront cost"
    ],
    relatedTopics: ["insurance-guide", "evidence-preservation", "what-to-do-after-hit"]
  },
  {
    title: "Medical Treatment After Being Hit",
    slug: "medical-treatment-guide",
    description: "Guide to getting proper medical care after being hit by a car as a pedestrian.",
    category: "guide",
    icon: "🏥",
    content: `
## Why Medical Treatment Matters

Proper medical treatment after being hit by a car is crucial for:
1. Your health and recovery
2. Your legal case

Gaps in treatment or refusing care can be used against you.

## Immediate Medical Care

### Emergency Room
Go to the ER if you experience:
- Loss of consciousness
- Head injury of any kind
- Severe pain
- Difficulty breathing
- Numbness or tingling
- Visible injuries or bleeding
- Confusion
- Abdominal pain

### What to Tell Medical Staff
- You were hit by a car as a pedestrian
- Describe ALL symptoms, even minor ones
- Mention any pain, no matter how slight
- Be honest about how you feel

## Common Pedestrian Accident Injuries

### Head Injuries
- Concussions
- Traumatic brain injury (TBI)
- Skull fractures
- Cognitive impairment

### Spinal Injuries
- Herniated discs
- Vertebral fractures
- Spinal cord damage
- Paralysis

### Orthopedic Injuries
- Broken legs, arms, pelvis
- Knee injuries
- Hip fractures
- Ankle and foot injuries

### Soft Tissue
- Internal organ damage
- Internal bleeding
- Muscle and ligament tears
- Severe bruising

### Psychological
- PTSD
- Anxiety about crossing streets
- Depression
- Sleep disorders

## Follow-Up Care

### Within 24-48 Hours
- See your primary care doctor
- Follow all ER recommendations
- Start recommended treatments

### Ongoing Treatment
- Attend ALL appointments
- Follow treatment plans exactly
- Don't skip or reschedule
- Document everything

### Specialists You May Need
- Orthopedic surgeon
- Neurologist
- Physical therapist
- Pain management specialist
- Psychologist or psychiatrist

## Medical Documentation

**Critical Records to Keep:**
- ER admission and discharge papers
- All imaging results
- Surgery reports
- Doctor's notes from every visit
- Physical therapy records
- Prescription records
- All billing statements

**Organize Chronologically** and make copies of everything.
`,
    keyTakeaways: [
      "Always get medical attention after being hit - adrenaline masks injuries",
      "Tell doctors ALL symptoms, even minor ones",
      "Follow all treatment plans without gaps",
      "Keep copies of all medical records",
      "Mental health treatment is valid and important"
    ],
    relatedTopics: ["what-to-do-after-hit", "evidence-preservation", "dealing-with-insurance"]
  },
  {
    title: "Pedestrian Right-of-Way Laws",
    slug: "pedestrian-right-of-way",
    description: "Understanding when pedestrians have the right-of-way and how it affects accident liability.",
    category: "legal",
    icon: "⚖️",
    content: `
## Understanding Right-of-Way

Right-of-way determines who has the legal priority to proceed. For pedestrians, this varies by situation and location.

## When Pedestrians Have Right-of-Way

### In Crosswalks
- Marked crosswalks: YES
- Unmarked crosswalks (at intersections): Usually YES
- Mid-block crossings: Usually NO

### At Traffic Signals
- Walk signal: YES
- Don't Walk signal: NO
- Steady yellow/red: Generally NO

### Outside Crosswalks
- Pedestrians generally must yield to vehicles
- BUT drivers must still exercise due care

## Driver Duties

Regardless of right-of-way, drivers must:
- Exercise due care to avoid hitting pedestrians
- Yield to pedestrians in crosswalks
- Stop for pedestrians with white canes or guide dogs
- Reduce speed in school zones and residential areas
- Watch for pedestrians when turning

## How Right-of-Way Affects Your Case

### You Had Right-of-Way
- Establishes driver negligence
- Strengthens your claim
- May still need to prove driver was negligent

### You Did NOT Have Right-of-Way
- Doesn't automatically bar your claim
- Driver may still have been negligent
- Comparative fault may reduce your recovery
- You may still recover damages

## Comparative Negligence

Most states use comparative negligence:
- Your damages reduced by your percentage of fault
- Example: If you're 20% at fault, you recover 80%

### Contributory Negligence States
(Alabama, Maryland, North Carolina, Virginia, DC)
- ANY fault may bar your entire recovery
- Need experienced attorney in these states

## Special Right-of-Way Rules

### Blind Pedestrians
- Have right-of-way everywhere
- White cane signals right-of-way

### School Zones
- Enhanced pedestrian protections
- Reduced speed limits
- Crossing guards have authority

### Emergency Vehicles
- Pedestrians must yield to emergency vehicles
`,
    keyTakeaways: [
      "Pedestrians in crosswalks generally have right-of-way",
      "Drivers must always exercise due care",
      "Lack of right-of-way doesn't eliminate your claim",
      "Comparative fault may reduce but not eliminate recovery",
      "Contributory negligence states have strict rules"
    ],
    relatedTopics: ["crosswalk-laws-by-state", "proving-fault", "comparative-fault-explained"]
  },
  {
    title: "Pedestrian Accident Settlement Calculator Guide",
    slug: "settlement-calculator-guide",
    description: "Learn how pedestrian accident settlements are calculated and what factors affect your compensation amount.",
    category: "legal",
    icon: "🧮",
    content: `
## How Settlements Are Calculated

Pedestrian accident settlements consider multiple factors to determine fair compensation.

## Economic Damages

### Medical Expenses
- Emergency room costs
- Hospital stays
- Surgery costs
- Physical therapy
- Future medical needs
- Prescription medications
- Medical equipment

### Lost Wages
- Time missed from work
- Reduced earning capacity
- Future lost earnings
- Lost benefits and bonuses

### Property Damage
- Personal belongings damaged
- Electronics (phone, watch, etc.)
- Clothing

## Non-Economic Damages

### Pain and Suffering
- Physical pain experienced
- Ongoing chronic pain
- Severity and duration of suffering

### Emotional Distress
- PTSD from the accident
- Anxiety and depression
- Fear of walking/crossing streets

### Loss of Enjoyment
- Inability to pursue hobbies
- Reduced quality of life
- Loss of consortium

## Multiplier Method

Many settlements use a multiplier:
1. Add up all economic damages
2. Multiply by 1.5 to 5 based on severity
3. Add economic damages back

### Multiplier Factors
- 1.5-2x: Minor injuries, quick recovery
- 2-3x: Moderate injuries, some ongoing effects
- 3-4x: Serious injuries, significant impact
- 4-5x: Catastrophic injuries, permanent disability

## Per Diem Method

Calculate daily compensation for pain:
1. Determine a reasonable daily rate
2. Multiply by days of recovery
3. Add economic damages

## Factors That Increase Value

- Clear driver liability
- Multiple witnesses
- Dash cam or surveillance footage
- Severe or permanent injuries
- Impact on career
- Young victim with long-term needs
`,
    keyTakeaways: [
      "Economic damages include all financial losses",
      "Non-economic damages cover pain and suffering",
      "Multiplier method commonly used for calculation",
      "Severity of injuries significantly impacts value",
      "Documentation is essential for maximum recovery"
    ],
    relatedTopics: ["calculating-pedestrian-accident-damages", "medical-expense-documentation", "negotiating-pedestrian-accident-settlement"]
  },
  {
    title: "Choosing a Pedestrian Accident Lawyer",
    slug: "choosing-pedestrian-lawyer",
    description: "Key factors to consider when selecting an attorney for your pedestrian accident case.",
    category: "legal",
    icon: "👨‍⚖️",
    content: `
## Why You Need a Specialized Attorney

Pedestrian accidents have unique legal considerations:
- Specific traffic laws for pedestrians
- Complex liability determinations
- Higher injury severity typically
- Different insurance coverage issues

## What to Look For

### Experience
- Years handling pedestrian cases
- Track record of settlements/verdicts
- Familiarity with local courts
- Knowledge of pedestrian-specific laws

### Resources
- Ability to fund investigation
- Access to expert witnesses
- Staff to handle your case
- Technology for case management

### Communication
- Responsive to calls/emails
- Explains legal process clearly
- Keeps you updated regularly
- Available to answer questions

### Reputation
- Client reviews and testimonials
- Peer ratings (Martindale, Avvo)
- Professional memberships
- Awards and recognition

## Questions to Ask

### About Their Experience
1. How many pedestrian accident cases have you handled?
2. What were the outcomes?
3. Have you tried cases in court?
4. Are you familiar with our local courts?

### About Your Case
5. What do you think my case is worth?
6. What challenges do you foresee?
7. How long might this take?
8. What is your strategy?

### About Fees
9. What is your contingency fee percentage?
10. What costs will I be responsible for?
11. Do you advance case costs?
12. What happens if we lose?

## Red Flags

- Guarantees specific results
- Pressures you to sign immediately
- Won't explain the fee agreement
- Doesn't return calls promptly
- Sends a non-attorney to meet you
- Handles too many different case types

## Free Consultations

Most pedestrian accident attorneys offer:
- Free initial case evaluation
- No obligation to hire
- Assessment of case strength
- Explanation of legal options
`,
    keyTakeaways: [
      "Choose an attorney experienced in pedestrian cases",
      "Ask about their track record and resources",
      "Understand the fee structure completely",
      "Look for good communication skills",
      "Avoid attorneys who guarantee results"
    ],
    relatedTopics: ["when-to-hire-pedestrian-accident-attorney", "contingency-fee-arrangements", "what-to-expect-from-attorney"]
  },
  {
    title: "Understanding No-Fault Insurance and Pedestrians",
    slug: "no-fault-insurance-pedestrians",
    description: "How no-fault insurance laws affect pedestrian accident claims in different states.",
    category: "legal",
    icon: "📋",
    content: `
## What Is No-Fault Insurance?

No-fault insurance means your own insurance pays for your injuries regardless of who caused the accident.

## No-Fault States

The following states have no-fault insurance:
- Florida
- Hawaii
- Kansas
- Kentucky (choice)
- Massachusetts
- Michigan
- Minnesota
- New Jersey (choice)
- New York
- North Dakota
- Pennsylvania (choice)
- Utah

## How It Works for Pedestrians

### Your Own Coverage
- If you have auto insurance, your PIP covers you
- If hit by a car, driver's insurance may cover you
- Health insurance as secondary coverage

### What PIP Covers
- Medical expenses
- Lost wages (percentage)
- Replacement services
- Funeral expenses

### Limits on Lawsuits
In no-fault states, you can only sue if:
- Injuries exceed a threshold (serious/permanent)
- Medical expenses exceed monetary threshold
- Death occurred

## Verbal vs Monetary Thresholds

### Verbal Threshold States
Must prove serious injury:
- Significant disfigurement
- Permanent injury
- Bone fracture
- Loss of body function

### Monetary Threshold States
Medical expenses must exceed amount:
- Varies by state ($2,000-$5,000+)
- Once exceeded, can sue for all damages

## Pedestrian-Specific Rules

### New York
- Pedestrians can get PIP from driver's insurance
- Can sue if serious injury threshold met

### Michigan
- Unlimited PIP benefits available
- Strong pedestrian protections

### Florida
- Must have your own PIP or health insurance
- Can sue for permanent injury
`,
    keyTakeaways: [
      "No-fault affects 12 states plus some choice states",
      "PIP covers your injuries regardless of fault",
      "Thresholds limit when you can file a lawsuit",
      "Pedestrians have some special protections",
      "An attorney can navigate these complex rules"
    ],
    relatedTopics: ["no-fault-states-pedestrian-claims", "uninsured-motorist-coverage-pedestrians", "dealing-with-insurance"]
  },
  {
    title: "Long-Term Effects of Pedestrian Accident Injuries",
    slug: "long-term-injury-effects",
    description: "Understanding the lasting physical, emotional, and financial impacts of pedestrian accident injuries.",
    category: "guide",
    icon: "🩺",
    content: `
## Physical Long-Term Effects

### Traumatic Brain Injury (TBI)
- Cognitive difficulties
- Memory problems
- Personality changes
- Seizure disorders
- Chronic headaches

### Spinal Cord Injuries
- Paralysis (partial or complete)
- Chronic pain
- Loss of sensation
- Bladder/bowel dysfunction
- Respiratory issues

### Orthopedic Injuries
- Chronic joint pain
- Limited range of motion
- Arthritis development
- Need for future surgeries
- Hardware complications

### Soft Tissue Injuries
- Chronic pain syndromes
- Fibromyalgia development
- Reduced flexibility
- Ongoing treatment needs

## Emotional & Psychological Effects

### Post-Traumatic Stress Disorder
- Flashbacks to the accident
- Nightmares
- Avoidance of crossing streets
- Hypervigilance around traffic
- Panic attacks

### Depression and Anxiety
- Social isolation
- Changes in relationships
- Difficulty working
- Loss of independence
- Grief over lost abilities

## Financial Long-Term Impacts

### Medical Costs
- Ongoing treatment
- Medications
- Medical equipment
- Home modifications
- Future surgeries

### Career Impact
- Reduced earning capacity
- Career change required
- Early retirement
- Lost promotions
- Retraining costs

### Life Care Costs
- Home healthcare
- Assisted living
- Transportation needs
- Personal care assistance

## Documenting Future Damages

### Life Care Plan
- Comprehensive needs assessment
- Projected lifetime costs
- Expert medical input

### Vocational Expert
- Lost earning capacity
- Career limitations
- Retraining needs

### Economist
- Present value calculations
- Inflation adjustments
- Lost benefits value
`,
    keyTakeaways: [
      "Pedestrian accidents often cause life-altering injuries",
      "TBI and spinal injuries have extensive long-term effects",
      "Psychological impacts require professional treatment",
      "Future damages must be carefully documented",
      "Life care plans help ensure full compensation"
    ],
    relatedTopics: ["traumatic-brain-injury-pedestrian-accidents", "spinal-cord-injuries-pedestrians", "calculating-pedestrian-accident-damages"]
  },
  {
    title: "Hit-and-Run Pedestrian Accident Guide",
    slug: "hit-and-run-guide",
    description: "What to do if you're injured by a driver who flees the scene and how to pursue compensation.",
    category: "guide",
    icon: "🚗",
    content: `
## Immediate Steps After Hit-and-Run

### At the Scene
1. Call 911 immediately
2. Try to remember vehicle details:
   - Make, model, color
   - License plate (any part)
   - Direction of travel
   - Distinguishing features
3. Look for witnesses
4. Note any nearby cameras
5. Get medical attention

### Information to Gather
- Witness names and contacts
- Security camera locations
- Time and exact location
- Weather conditions
- Traffic signal status

## How Hit-and-Run Drivers Get Caught

### Investigation Methods
- Surveillance camera footage
- Witness statements
- Vehicle debris analysis
- Paint transfer evidence
- License plate readers
- Social media tips

### Timeline
- Police prioritize serious injuries
- Most solved within 48 hours if at all
- Cold cases can still be solved later

## Getting Compensation

### Uninsured Motorist Coverage
- Your own auto insurance
- Covers hit-and-run accidents
- May include medical and lost wages
- Check your policy limits

### If You Don't Have UM Coverage
- Health insurance for medical bills
- Crime victim compensation funds
- Civil lawsuit if driver found

### If Driver Is Found
- Can sue driver directly
- Their insurance (if any) pays
- Criminal restitution possible

## State Crime Victim Funds

Most states have victim compensation funds:
- Cover medical expenses
- Lost wages assistance
- Counseling costs
- Application required
- Income limits may apply

## Increasing Chances of Finding Driver

- File police report immediately
- Canvass for witnesses
- Check for cameras yourself
- Post on social media
- Contact local media
- Offer reward through attorney
`,
    keyTakeaways: [
      "Act quickly to preserve evidence",
      "Note any vehicle details you can remember",
      "Your UM coverage may provide compensation",
      "State victim funds can help with costs",
      "Many hit-and-run drivers are eventually found"
    ],
    relatedTopics: ["hit-and-run-pedestrian-accidents", "uninsured-motorist-coverage-pedestrians", "evidence-collection-pedestrian-accidents"]
  },
  {
    title: "Pedestrian Accidents Involving Children",
    slug: "child-pedestrian-accident-guide",
    description: "Special legal considerations and protections when a child is injured as a pedestrian.",
    category: "guide",
    icon: "👶",
    content: `
## Why Child Cases Are Different

### Legal Standards
- Children held to lower standard of care
- "What would a reasonable child do?"
- Age and experience considered
- Very young children may have no contributory fault

### Higher Driver Duty
- Drivers must anticipate children
- Extra caution in:
  - School zones
  - Residential areas
  - Parks and playgrounds
  - Ice cream truck areas

## Common Scenarios

### School Zone Accidents
- Crossing to/from school
- School bus loading zones
- Crossing guard present
- Before/after school activities

### Neighborhood Accidents
- Playing in residential streets
- Darting from between cars
- Chasing balls or toys
- Riding bikes on sidewalks

### Parking Lot Accidents
- Shopping centers
- School parking lots
- Events and activities
- Backing accidents

## Special Damages Considerations

### Future Medical Care
- Growing bones may need multiple surgeries
- Psychological effects during development
- Lifetime of care for serious injuries

### Educational Impact
- Special education needs
- Tutoring during recovery
- Delayed development
- College planning adjustments

### Future Lost Earnings
- Career potential affected
- Lifetime earning capacity
- Earlier retirement age

## Legal Process Differences

### Court Approval Required
- Settlement must be approved by judge
- Guardian ad litem may be appointed
- Funds often held in trust

### Statute of Limitations
- Usually tolled until age 18
- Time to file starts at adulthood
- Varies by state

### Who Can Sue
- Parent or guardian files suit
- Lawsuit in child's name
- Parent may have separate claim for:
  - Medical expenses paid
  - Loss of child's services

## Protecting the Settlement

### Structured Settlements
- Payments over time
- Protected from misuse
- Tax advantages

### Trust Accounts
- Court-supervised
- Professional management
- Disbursed at adulthood
`,
    keyTakeaways: [
      "Children are held to lower standards of care",
      "Drivers have heightened duty around children",
      "Future damages are especially important",
      "Court approval required for settlements",
      "Settlements protected until adulthood"
    ],
    relatedTopics: ["child-pedestrian-accidents", "pedestrian-accidents-involving-minors", "school-zone-pedestrian-accidents"]
  },
  {
    title: "Pedestrian Accident Medical Treatment Guide",
    slug: "pedestrian-medical-treatment",
    description: "Understanding medical treatment after a pedestrian accident and how it affects your legal case.",
    category: "guide",
    icon: "🏥",
    content: `
## Immediate Medical Care

### Emergency Room
When to go to ER:
- Any loss of consciousness
- Head or neck pain
- Difficulty breathing
- Severe pain anywhere
- Visible broken bones
- Heavy bleeding

### What Happens at ER
- Triage assessment
- Imaging (X-rays, CT scans)
- Treatment of acute injuries
- Pain management
- Referrals for follow-up

## Follow-Up Care

### Primary Care Doctor
- Ongoing symptom monitoring
- Referrals to specialists
- Medication management
- Work status documentation

### Specialists You May Need
- Orthopedic surgeon
- Neurologist
- Physical therapist
- Pain management doctor
- Psychologist/psychiatrist
- Chiropractor

## Treatment Documentation

### Why It Matters
- Proves injury severity
- Shows treatment necessity
- Establishes medical costs
- Documents recovery timeline
- Supports future needs claims

### What to Document
- All appointments kept
- Treatments received
- Medications prescribed
- Medical bills
- Mileage to appointments
- Time missed from work

## Gap in Treatment Problems

### Why Gaps Hurt Your Case
- Insurance claims you weren't injured
- Suggests injuries weren't serious
- Defense argues injuries unrelated to accident
- Reduces credibility

### Valid Reasons for Gaps
- Financial constraints (document this)
- Doctor availability
- COVID-19 delays
- Other documented reasons

## Treatment on a Lien

### Medical Liens Explained
- Doctor treats now, gets paid from settlement
- No out-of-pocket costs during treatment
- Ensures continuous care
- Common in personal injury cases

### Pros and Cons
Pros:
- No upfront costs
- Access to specialists
- Treatment documentation

Cons:
- Lien must be paid from settlement
- May be reduced through negotiation
- Some doctors don't accept liens
`,
    keyTakeaways: [
      "Always seek immediate medical attention",
      "Follow all treatment recommendations",
      "Avoid gaps in medical treatment",
      "Document everything thoroughly",
      "Treatment on lien is available if needed"
    ],
    relatedTopics: ["medical-records-pedestrian-claims", "medical-expense-documentation", "medical-treatment-guide"]
  },
  {
    title: "Pedestrian Accidents and Rideshare Vehicles",
    slug: "rideshare-pedestrian-guide",
    description: "Understanding liability when pedestrians are hit by Uber, Lyft, or other rideshare drivers.",
    category: "guide",
    icon: "📱",
    content: `
## Rideshare Accident Complexity

Accidents involving Uber, Lyft, and other rideshare services have unique liability issues.

## Insurance Coverage Periods

### Period 0 - App Off
- Driver's personal insurance only
- Rideshare company not liable
- Standard pedestrian accident case

### Period 1 - App On, Waiting for Ride
- Limited rideshare insurance kicks in
- Uber/Lyft: $50K per person/$100K per accident
- Covers liability if personal insurance denies

### Period 2 - En Route to Passenger
- Full rideshare insurance active
- Uber/Lyft: $1 million liability
- Covers pedestrian injuries

### Period 3 - Passenger in Vehicle
- Full rideshare insurance active
- $1 million liability coverage
- Highest level of protection

## Determining Which Period

### Evidence Needed
- Driver's app status at time of accident
- GPS records from rideshare company
- Passenger testimony
- Driver's statement

### Why It Matters
- Determines available insurance
- Affects total compensation
- Identifies responsible parties

## Filing Claims

### Multiple Potential Sources
1. Driver's personal auto insurance
2. Rideshare company's commercial policy
3. Uninsured/underinsured motorist coverage
4. Driver personally

### Steps to Take
- Report accident to rideshare company
- Get driver's personal insurance info
- File claim with rideshare
- Consult attorney for guidance

## Common Challenges

### Distracted Driving
- Watching app for rides
- Following GPS directions
- Rushing to pick up passengers

### Proving Driver Status
- Companies may resist disclosure
- Legal process to obtain records
- Attorney can subpoena data

## Rideshare Company Policies

### Uber
- James River Insurance Company
- $1M coverage during trips
- Limited coverage when app on

### Lyft
- Similar coverage structure
- May vary by state
- Policy limits same as Uber
`,
    keyTakeaways: [
      "Coverage depends on driver's app status",
      "Highest coverage when passenger in vehicle",
      "Multiple insurance sources may apply",
      "Legal help needed to navigate claims",
      "Rideshare companies may resist providing data"
    ],
    relatedTopics: ["rideshare-pedestrian-accidents", "proving-fault-pedestrian-accident", "dealing-with-insurance"]
  },
  {
    title: "Pedestrian Accident Witness Guide",
    slug: "witness-guide",
    description: "How witness testimony strengthens your pedestrian accident case and how to secure it.",
    category: "guide",
    icon: "👁️",
    content: `
## Importance of Witnesses

Witness testimony can:
- Corroborate your account
- Establish driver negligence
- Counter false claims
- Describe injuries observed
- Document scene conditions

## Types of Witnesses

### Eyewitnesses
- Saw the accident happen
- Most valuable testimony
- Can describe vehicle speed, signals, etc.

### Occurrence Witnesses
- Arrived immediately after
- Saw positions of vehicles/victims
- Observed initial injuries

### Expert Witnesses
- Accident reconstruction
- Medical experts
- Vocational specialists
- Economic experts

## Finding Witnesses

### At the Scene
- Ask anyone nearby
- Get names and phone numbers
- Note where they were standing
- Ask what they saw

### After the Scene
- Check nearby businesses
- Review surveillance footage
- Post on social media
- Check with responding officers

### Canvassing
- Return to scene at same time
- Ask regular pedestrians/workers
- Leave contact information
- Check for regular witnesses

## Preserving Testimony

### Witness Statements
- Get written statements quickly
- Record video statements (with permission)
- Note date, time, location of statement
- Have attorney conduct formal interview

### Why Time Matters
- Memories fade quickly
- Witnesses may move away
- Details become confused
- Defense can challenge credibility

## Witness Credibility Issues

### Strong Witnesses
- No relationship to either party
- Good vantage point
- Consistent statements
- No reason to lie

### Weak Witnesses
- Friends/family of a party
- Didn't actually see accident
- Inconsistent statements
- Potential bias

## Working with Your Attorney

### What Attorneys Do
- Conduct formal interviews
- Obtain signed declarations
- Issue subpoenas if needed
- Prepare witnesses for deposition/trial

### Protecting Witnesses
- Keep contact info confidential
- Don't coach their testimony
- Let attorney handle contact
- Preserve written statements
`,
    keyTakeaways: [
      "Witnesses significantly strengthen cases",
      "Gather contact information at the scene",
      "Get written statements as soon as possible",
      "Independent witnesses are most credible",
      "Let your attorney handle formal witness preparation"
    ],
    relatedTopics: ["evidence-collection-pedestrian-accidents", "proving-fault-pedestrian-accident", "expert-witnesses-pedestrian-cases"]
  },
  {
    title: "Pedestrian Accidents and Surveillance Footage",
    slug: "surveillance-footage-guide",
    description: "How to locate and preserve video evidence that can prove your pedestrian accident case.",
    category: "guide",
    icon: "📹",
    content: `
## Why Video Evidence Matters

Surveillance footage can:
- Show exactly what happened
- Prove driver negligence
- Counter false accusations
- Establish timing and speed
- Demonstrate injuries

## Types of Video Evidence

### Traffic Cameras
- Red light cameras
- Speed cameras
- Department of Transportation cameras
- Often publicly accessible

### Business Surveillance
- Store security cameras
- Bank ATM cameras
- Gas station cameras
- Restaurant outdoor cameras

### Private Cameras
- Ring doorbells
- Home security systems
- Dash cams from other vehicles
- Building security systems

### Vehicle Cameras
- Dash cams
- Rideshare vehicle cameras
- Commercial vehicle cameras
- Bus cameras

## Finding Footage

### Where to Look
- Businesses facing the intersection
- Traffic camera locations
- Residential Ring/Nest cameras
- Parking lot cameras
- ATMs

### Time Is Critical
- Most systems overwrite in 7-30 days
- Some delete after 72 hours
- Act immediately to preserve

## Preserving Footage

### Preservation Letters
- Send written request to retain footage
- Creates legal obligation to preserve
- Include specific date, time, location
- Send certified mail

### Attorney Subpoenas
- Legal demand for footage
- Prevents deletion
- Forces compliance

### What Your Attorney Does
- Identifies potential sources
- Sends preservation letters
- Issues subpoenas
- Obtains and analyzes footage
- Works with video experts

## Using Footage in Your Case

### Analysis
- Frame-by-frame review
- Speed calculations
- Timeline establishment
- Enhancement of poor quality

### Challenges
- Poor camera angles
- Obstructions
- Quality issues
- Gaps in coverage

## Privacy Considerations

### Whose Permission Needed
- Property owner for private cameras
- Business owner for store footage
- Homeowner for Ring cameras
- Government for public cameras
`,
    keyTakeaways: [
      "Video evidence can prove your entire case",
      "Act within 72 hours to preserve footage",
      "Send preservation letters immediately",
      "Multiple sources of footage may exist",
      "An attorney can subpoena reluctant parties"
    ],
    relatedTopics: ["evidence-collection-pedestrian-accidents", "proving-fault-pedestrian-accident", "witness-guide"]
  },
  {
    title: "Social Media and Your Pedestrian Accident Case",
    slug: "social-media-accident-case",
    description: "How social media can help or hurt your pedestrian accident claim and best practices to follow.",
    category: "legal",
    icon: "📱",
    content: `
## How Social Media Can Hurt Your Case

### Posts Used Against You
- Photos showing physical activity
- Check-ins at locations
- Comments about feeling fine
- Vacation or party photos
- Employment updates

### Defense Tactics
- Monitor your accounts
- Subpoena deleted content
- Friend your friends
- Take screenshots
- Hire investigators

### Real Examples
- Claimed couldn't walk, posted hiking photo
- Said too depressed to work, posted party pics
- Claimed severe pain, checked in at gym

## Best Practices During Case

### What NOT to Do
- Don't post about the accident
- Don't discuss your injuries
- Don't post physical activities
- Don't discuss your lawsuit
- Don't friend strangers

### Privacy Settings
- Set everything to private
- Review friend requests carefully
- Audit existing friends
- Check tagged photos settings
- Review location sharing

### What's Safe
- Keep posting ordinary updates
- Share neutral content
- Don't go completely dark (looks suspicious)
- Don't delete old posts (spoliation)

## Using Social Media Positively

### Finding Witnesses
- Post asking for witnesses
- Share in local groups
- Community members may help

### Documenting Driver
- Check if driver posted about accident
- Screenshots of admissions
- Evidence of prior bad behavior
- Posts showing impairment

## Legal Discovery Issues

### What They Can Access
- Anything public
- Deleted content through subpoena
- Private messages potentially
- Account metadata

### What's Protected
- Attorney-client communications
- Truly private posts (sometimes)
- Content clearly unrelated to case

## Special Considerations

### Don't Delete
- Deletion = spoliation of evidence
- Can result in sanctions
- Looks like hiding something
- Courts can force recovery

### Don't Make New Accounts
- Can be discovered
- Suggests consciousness of guilt
- Complicates your case
`,
    keyTakeaways: [
      "Assume everything you post will be seen",
      "Don't post about your accident or injuries",
      "Make all accounts private immediately",
      "Don't delete posts - it can hurt your case",
      "Social media can help find witnesses"
    ],
    relatedTopics: ["evidence-collection-pedestrian-accidents", "dealing-with-insurance", "protecting-your-settlement"]
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
