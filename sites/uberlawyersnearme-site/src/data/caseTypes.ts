// Case types for rideshare accident law pages
export interface CaseType {
  name: string;
  slug: string;
  shortDescription: string;
  description: string;
  commonCauses: string[];
  typicalInjuries: string[];
  liabilityFactors: string[];
  potentialDefendants: string[];
  averageSettlement: string;
  keyLegalPoints: string[];
  insuranceCoverage: string;
}

export const caseTypes: CaseType[] = [
  {
    name: "Uber Passenger Injuries",
    slug: "uber-passenger-injuries",
    shortDescription: "Injuries to passengers riding in an Uber vehicle during an accident.",
    description: "Uber passenger injury cases involve people who are injured while riding as a paying passenger in an Uber vehicle. These cases typically have the strongest coverage because Uber's $1 million commercial policy is in full effect during active trips. Passengers have the clearest path to compensation since they are not at fault for the accident.",
    commonCauses: [
      "Driver negligence or distracted driving",
      "Another driver causing the collision",
      "Speeding to meet pickup times",
      "Fatigue from long driving hours",
      "Unfamiliar routes leading to errors",
      "Running red lights or stop signs",
      "Impaired driving (rare but serious)"
    ],
    typicalInjuries: [
      "Whiplash and neck injuries",
      "Spinal cord damage",
      "Traumatic brain injuries",
      "Broken bones",
      "Internal organ damage",
      "Soft tissue injuries",
      "Psychological trauma/PTSD"
    ],
    liabilityFactors: [
      "Whether Uber driver was at fault",
      "Whether third party driver caused accident",
      "Uber's $1M policy covers passengers regardless",
      "Driver's personal insurance may also apply",
      "Multiple policies may stack"
    ],
    potentialDefendants: [
      "The Uber driver (primary or shared fault)",
      "Uber Technologies Inc. (through insurance)",
      "Third-party negligent drivers",
      "Vehicle manufacturers (defects)",
      "Government entities (road conditions)"
    ],
    averageSettlement: "$50,000 - $1,000,000+",
    keyLegalPoints: [
      "Uber's $1M liability coverage applies during active trips",
      "Passengers don't need to prove driver employment status",
      "Multiple insurance policies may provide coverage",
      "No comparative fault issues for passengers in most states",
      "Uber's arbitration clause may affect dispute resolution"
    ],
    insuranceCoverage: "$1,000,000 commercial liability coverage during active trips"
  },
  {
    name: "Lyft Passenger Injuries",
    slug: "lyft-passenger-injuries",
    shortDescription: "Injuries to passengers riding in a Lyft vehicle during an accident.",
    description: "Lyft passenger injuries follow similar patterns to Uber cases. Lyft maintains $1 million in liability coverage for passengers during active trips. These cases are generally straightforward from a coverage perspective, as the passenger is a clear victim entitled to compensation.",
    commonCauses: [
      "Driver negligence",
      "Third-party driver negligence",
      "Distracted driving (GPS, phone)",
      "Speeding and aggressive driving",
      "Driver fatigue",
      "Poor vehicle maintenance",
      "Adverse weather conditions"
    ],
    typicalInjuries: [
      "Neck and back injuries",
      "Head trauma and concussions",
      "Fractured bones",
      "Lacerations and contusions",
      "Knee and leg injuries",
      "Shoulder injuries",
      "Emotional distress"
    ],
    liabilityFactors: [
      "Lyft's $1M policy applies during trips",
      "Fault of Lyft driver vs. third party",
      "Multiple coverage sources available",
      "Driver screening and background check issues"
    ],
    potentialDefendants: [
      "The Lyft driver",
      "Lyft Inc. (through insurance)",
      "Third-party negligent drivers",
      "Vehicle or parts manufacturers",
      "Road maintenance entities"
    ],
    averageSettlement: "$45,000 - $900,000+",
    keyLegalPoints: [
      "Lyft's commercial policy provides $1M coverage",
      "Coverage applies from pickup to dropoff",
      "Passengers typically don't face fault allocation",
      "Lyft's Terms of Service contain arbitration provisions",
      "Can pursue claims against multiple defendants"
    ],
    insuranceCoverage: "$1,000,000 commercial liability during active trips"
  },
  {
    name: "Rideshare Driver Injuries",
    slug: "rideshare-driver-injuries",
    shortDescription: "Injuries suffered by Uber/Lyft drivers while working on the platform.",
    description: "Rideshare driver injury cases are complex because drivers are classified as independent contractors, not employees. This affects workers' compensation eligibility and the available insurance coverage. Coverage depends heavily on which 'period' of the app the driver was in at the time of the accident.",
    commonCauses: [
      "Collisions caused by other drivers",
      "Distraction from app/navigation",
      "Fatigue from long hours",
      "Unsafe passenger behavior",
      "Road hazards and poor conditions",
      "Carjacking or assault",
      "Vehicle defects"
    ],
    typicalInjuries: [
      "Back and spinal injuries",
      "Repetitive stress injuries",
      "Traumatic brain injuries",
      "Fractures and broken bones",
      "Soft tissue damage",
      "Psychological trauma",
      "Chronic pain conditions"
    ],
    liabilityFactors: [
      "App status at time of accident (Period 1, 2, or 3)",
      "Who was at fault for collision",
      "Driver's personal auto insurance",
      "Uber/Lyft contingent coverage",
      "Independent contractor status"
    ],
    potentialDefendants: [
      "Third-party negligent driver",
      "Their insurance company",
      "Vehicle manufacturers",
      "Road maintenance entities",
      "Violent passengers (assault cases)"
    ],
    averageSettlement: "$30,000 - $500,000+",
    keyLegalPoints: [
      "Coverage varies dramatically by app status",
      "Period 1 (app on, no ride): Limited contingent coverage",
      "Period 2/3 (en route/trip): $1M coverage but must claim properly",
      "No workers' compensation in most states",
      "Can pursue third-party claims against other drivers",
      "Personal injury protection (PIP) may apply in no-fault states"
    ],
    insuranceCoverage: "Varies by period - from contingent coverage to $1M during trips"
  },
  {
    name: "Third-Party Accidents",
    slug: "third-party-accidents",
    shortDescription: "People in other vehicles or pedestrians hit by Uber/Lyft drivers.",
    description: "Third-party rideshare accidents involve people outside the Uber or Lyft vehicle who are injured by a rideshare driver. This includes other motorists, pedestrians, cyclists, and bystanders. These cases require determining the rideshare driver's fault and the app status at the time of impact.",
    commonCauses: [
      "Rideshare driver running lights/signs",
      "Distracted driving while using app",
      "Illegal turns or lane changes",
      "Speeding to reach passengers",
      "Failure to yield right of way",
      "Drunk or impaired driving",
      "Sudden stops for pickups/dropoffs"
    ],
    typicalInjuries: [
      "Severe trauma from vehicle collisions",
      "Pedestrian impact injuries",
      "Cyclist injuries",
      "Traumatic brain injuries",
      "Spinal cord damage",
      "Wrongful death",
      "Multiple fractures"
    ],
    liabilityFactors: [
      "Rideshare driver's fault for accident",
      "App period at time of collision",
      "Whether driver was logged in",
      "Third party's comparative fault",
      "Available insurance coverage"
    ],
    potentialDefendants: [
      "The rideshare driver personally",
      "Uber/Lyft (through insurance coverage)",
      "Driver's personal insurance",
      "Other negligent parties"
    ],
    averageSettlement: "$40,000 - $750,000+",
    keyLegalPoints: [
      "Must prove rideshare driver was at fault",
      "Coverage depends on app status at impact",
      "Period 3 (active trip) provides maximum $1M coverage",
      "Period 1 may only have contingent coverage",
      "Can pursue driver's personal assets if coverage insufficient",
      "Uber/Lyft insurance is primary during active trips"
    ],
    insuranceCoverage: "Period 1: $50K/$100K contingent | Period 2/3: $1M"
  },
  {
    name: "Pedestrian Hit by Rideshare",
    slug: "pedestrian-rideshare-accident",
    shortDescription: "Pedestrians struck by Uber or Lyft vehicles.",
    description: "Pedestrians hit by rideshare vehicles often suffer catastrophic injuries due to the lack of protection. These cases can involve complex liability issues, particularly around designated pickup/dropoff zones where pedestrians and rideshare vehicles frequently interact. Airport zones, entertainment districts, and urban areas see the highest frequency of these accidents.",
    commonCauses: [
      "Driver distraction looking for passenger",
      "Illegal pickups on busy streets",
      "Rushing to beat app timers",
      "Failure to yield at crosswalks",
      "Double-parking and sudden stops",
      "Driving in pedestrian-heavy areas",
      "Reversing without checking mirrors"
    ],
    typicalInjuries: [
      "Lower extremity fractures",
      "Pelvic injuries",
      "Traumatic brain injuries",
      "Spinal cord damage",
      "Internal organ damage",
      "Severe road rash/lacerations",
      "Fatal injuries"
    ],
    liabilityFactors: [
      "Driver negligence in pedestrian zone",
      "Pedestrian's right of way status",
      "App period at time of impact",
      "Location (crosswalk, sidewalk, street)",
      "Pedestrian's own negligence (jaywalking)"
    ],
    potentialDefendants: [
      "Rideshare driver",
      "Uber/Lyft (insurance coverage)",
      "Property owners (dangerous conditions)",
      "Government entities (road design)"
    ],
    averageSettlement: "$75,000 - $1,500,000+",
    keyLegalPoints: [
      "Pedestrians in crosswalks have strong right of way claims",
      "Coverage depends on driver's app status",
      "Higher damages due to severe injuries",
      "Comparative fault may reduce recovery in some states",
      "Wrongful death claims for fatal accidents"
    ],
    insuranceCoverage: "$1M coverage if during active trip, less during Period 1"
  },
  {
    name: "Airport Rideshare Accidents",
    slug: "airport-rideshare-accidents",
    shortDescription: "Accidents occurring in airport rideshare pickup/dropoff zones.",
    description: "Airport rideshare accidents occur in some of the busiest and most chaotic traffic environments. Airports have designated rideshare zones with heavy vehicle and pedestrian traffic, creating unique hazards. The stress of flight schedules, unfamiliar airport layouts, and congested pickup areas contribute to these accidents.",
    commonCauses: [
      "Congested pickup zone collisions",
      "Confusion over pickup locations",
      "Double-parking and illegal stops",
      "Pedestrian crossings in pickup areas",
      "Rushing to meet arriving passengers",
      "Terminal road congestion",
      "Merge accidents entering/exiting airport"
    ],
    typicalInjuries: [
      "Rear-end collision injuries",
      "Pedestrian injuries in pickup zones",
      "Low-speed impact injuries",
      "Whiplash and soft tissue damage",
      "Luggage-related injuries",
      "Door strikes",
      "Slip and falls exiting vehicles"
    ],
    liabilityFactors: [
      "Airport-specific traffic rules",
      "Rideshare zone regulations",
      "Multiple parties in congested areas",
      "Visibility and signage issues",
      "App status (Period 2 en route or Period 3 with passenger)"
    ],
    potentialDefendants: [
      "Rideshare driver",
      "Other rideshare/taxi drivers",
      "Airport authority (premises liability)",
      "Uber/Lyft (insurance)",
      "Other negligent drivers"
    ],
    averageSettlement: "$25,000 - $400,000",
    keyLegalPoints: [
      "Airport zones often have video surveillance",
      "Multiple witnesses typically available",
      "Airport may have special TNC rules",
      "Driver usually in Period 2 or 3 with coverage",
      "Airport authority may share liability for dangerous conditions"
    ],
    insuranceCoverage: "$1M during pickup/dropoff (active trip period)"
  },
  {
    name: "Rideshare Hit and Run",
    slug: "rideshare-hit-and-run",
    shortDescription: "Cases where a rideshare driver flees the scene of an accident.",
    description: "Rideshare hit-and-run cases present unique challenges and opportunities. While identifying the driver can be difficult, digital records from Uber and Lyft apps can help track down the responsible party. Even if the driver flees, app data showing their location, trip history, and vehicle information can be crucial evidence.",
    commonCauses: [
      "Driver panic after accident",
      "Uninsured/unlicensed drivers fleeing",
      "Impaired driving leading to flight",
      "Outstanding warrants or legal issues",
      "Immigration concerns",
      "Fear of deactivation from platform"
    ],
    typicalInjuries: [
      "All injury types depending on accident",
      "Delayed treatment due to driver fleeing",
      "Psychological trauma from abandonment",
      "Additional harm from delayed medical care"
    ],
    liabilityFactors: [
      "App records can identify fleeing driver",
      "UM/UIM coverage for unknown drivers",
      "Criminal liability for hit and run",
      "Platform data preservation critical",
      "Witness statements essential"
    ],
    potentialDefendants: [
      "Identified rideshare driver",
      "Uber/Lyft (through insurance/data)",
      "Victim's own UM/UIM coverage",
      "Crime victim compensation funds"
    ],
    averageSettlement: "$35,000 - $500,000+",
    keyLegalPoints: [
      "Act quickly to preserve app and GPS data",
      "Uber/Lyft keep detailed trip logs",
      "Can subpoena platform records",
      "UM/UIM coverage available if driver unknown",
      "Criminal charges often accompany civil case",
      "Platform may cooperate to protect reputation"
    ],
    insuranceCoverage: "Driver's TNC coverage if identified; UM/UIM if not"
  },
  {
    name: "Rideshare Sexual Assault",
    slug: "rideshare-sexual-assault",
    shortDescription: "Sexual assault or harassment by rideshare drivers against passengers.",
    description: "Sexual assault cases involving rideshare drivers are among the most traumatic. These cases often involve allegations that rideshare companies failed to adequately screen drivers or respond to prior complaints. Victims may have claims against both the individual driver and the rideshare platform for negligent hiring or retention.",
    commonCauses: [
      "Inadequate driver background checks",
      "Failure to investigate prior complaints",
      "Taking passengers to wrong destinations",
      "Late night/isolated area vulnerability",
      "Intoxicated passenger targeting",
      "Platform failure to deactivate problem drivers"
    ],
    typicalInjuries: [
      "Physical injuries from assault",
      "PTSD and psychological trauma",
      "Depression and anxiety",
      "Lost wages from inability to work",
      "Medical treatment costs",
      "Long-term therapy needs"
    ],
    liabilityFactors: [
      "Driver background check failures",
      "Prior complaints ignored by platform",
      "Negligent hiring and retention",
      "Platform safety feature failures",
      "Response to emergency during ride"
    ],
    potentialDefendants: [
      "The driver (criminal and civil)",
      "Uber/Lyft (negligent hiring/retention)",
      "Third parties who enabled assault"
    ],
    averageSettlement: "$100,000 - $5,000,000+",
    keyLegalPoints: [
      "Forced arbitration may apply (controversial)",
      "Negligent hiring/retention claims against platform",
      "Criminal prosecution separate from civil case",
      "Preservation of app communication evidence",
      "Uber safety report shows thousands of cases annually",
      "Statute of limitations may be extended for sexual assault"
    ],
    insuranceCoverage: "Commercial insurance may not cover intentional acts - direct company liability claims"
  },
  {
    name: "Autonomous Vehicle Accidents",
    slug: "autonomous-vehicle-accidents",
    shortDescription: "Accidents involving self-driving rideshare vehicles like Waymo.",
    description: "Autonomous rideshare vehicles are now operating in cities like Phoenix, San Francisco, and Los Angeles. These accidents raise novel legal questions about liability when there is no human driver. Claims may involve the autonomous vehicle company, software developers, hardware manufacturers, and others in the technology chain.",
    commonCauses: [
      "Sensor or software failures",
      "Failure to detect pedestrians/objects",
      "Unexpected driving conditions",
      "Interaction with human drivers",
      "Mapping or navigation errors",
      "Weather affecting sensors",
      "Edge case scenarios not programmed"
    ],
    typicalInjuries: [
      "Standard vehicle collision injuries",
      "Pedestrian injuries",
      "Cyclist injuries",
      "Psychological trauma from novel technology"
    ],
    liabilityFactors: [
      "Product liability for software/hardware",
      "Negligence in development/testing",
      "Failure to warn of limitations",
      "Regulatory compliance issues",
      "No human driver to blame"
    ],
    potentialDefendants: [
      "Autonomous vehicle company (Waymo, Cruise, etc.)",
      "Software developers",
      "Hardware/sensor manufacturers",
      "Rideshare platform if applicable",
      "Safety drivers (if present)"
    ],
    averageSettlement: "Highly variable - $50,000 to millions",
    keyLegalPoints: [
      "Product liability theories may apply",
      "Data preservation critical - vehicle records everything",
      "Novel legal territory - case law developing",
      "Regulatory framework varies by state",
      "Multiple parties in technology chain",
      "Companies well-funded for defense"
    ],
    insuranceCoverage: "Varies by company - typically high limits for commercial operations"
  },
  {
    name: "Rideshare DUI Accidents",
    slug: "rideshare-dui-accidents",
    shortDescription: "Accidents caused by intoxicated rideshare drivers.",
    description: "Rideshare DUI accidents are particularly egregious because passengers trust drivers to be sober and safe. These cases often result in punitive damages and may include claims against the rideshare platform for negligent screening or failure to detect impaired drivers. Criminal prosecution typically accompanies civil claims.",
    commonCauses: [
      "Alcohol impairment while driving",
      "Drug impairment (prescription or illegal)",
      "Marijuana use while driving",
      "Fatigue combined with substance use",
      "Failure of platform to detect impairment"
    ],
    typicalInjuries: [
      "Severe trauma from high-speed collisions",
      "Traumatic brain injuries",
      "Spinal cord damage",
      "Multiple fractures",
      "Internal injuries",
      "Wrongful death"
    ],
    liabilityFactors: [
      "Blood alcohol content evidence",
      "Drug test results",
      "Prior DUI history",
      "Platform screening failures",
      "Criminal conviction strengthens civil case"
    ],
    potentialDefendants: [
      "The impaired driver",
      "Uber/Lyft (negligent retention if prior incidents)",
      "Establishments that over-served driver (dram shop)",
      "Driver's personal insurance"
    ],
    averageSettlement: "$100,000 - $2,000,000+",
    keyLegalPoints: [
      "Punitive damages often available for DUI",
      "Criminal conviction aids civil case",
      "Platform may be liable for inadequate screening",
      "Blood/drug test evidence critical",
      "Higher damages due to egregious conduct",
      "Dram shop claims possible against bars"
    ],
    insuranceCoverage: "$1M TNC coverage, plus punitive damages from driver"
  },
  {
    name: "Rideshare Wrongful Death",
    slug: "rideshare-wrongful-death",
    shortDescription: "Fatal accidents involving Uber or Lyft vehicles.",
    description: "Wrongful death claims arising from rideshare accidents are among the most significant and emotionally difficult cases. Family members of those killed in rideshare accidents may be entitled to substantial compensation for their loss. These cases require careful evaluation of available insurance coverage and all potential defendants.",
    commonCauses: [
      "High-speed collisions",
      "Head-on crashes",
      "Pedestrian fatalities",
      "DUI-related deaths",
      "Failure to stop for traffic signals",
      "Catastrophic multi-vehicle accidents"
    ],
    typicalInjuries: [
      "Fatal injuries",
      "Pre-death pain and suffering",
      "Survival claims for estate"
    ],
    liabilityFactors: [
      "Cause of accident",
      "All available insurance coverage",
      "Comparative fault issues",
      "State wrongful death statutes",
      "Who can bring claim (spouse, children, parents)"
    ],
    potentialDefendants: [
      "At-fault rideshare driver",
      "Uber/Lyft insurance coverage",
      "Third-party negligent drivers",
      "Vehicle manufacturers",
      "Government entities (road conditions)"
    ],
    averageSettlement: "$500,000 - $10,000,000+",
    keyLegalPoints: [
      "State wrongful death statutes control who can sue",
      "Economic damages (lost income, support)",
      "Non-economic damages (loss of companionship)",
      "Survival action for pre-death suffering",
      "Punitive damages if egregious conduct",
      "$1M policy may be insufficient - look for additional coverage"
    ],
    insuranceCoverage: "$1M TNC coverage, plus other applicable policies"
  },
  {
    name: "Multi-Vehicle Rideshare Accidents",
    slug: "multi-vehicle-rideshare-accidents",
    shortDescription: "Complex accidents involving rideshare vehicles and multiple other vehicles.",
    description: "Multi-vehicle accidents involving rideshare are among the most complex to litigate. With multiple potential at-fault parties, various insurance policies, and competing claims, these cases require extensive investigation and experienced legal representation. Determining fault allocation among multiple defendants is critical.",
    commonCauses: [
      "Chain-reaction collisions",
      "Highway pileups",
      "Intersection multi-car crashes",
      "Multiple rideshare vehicles involved",
      "Commercial vehicle involvement",
      "Weather-related multi-car accidents"
    ],
    typicalInjuries: [
      "Multiple impact injuries",
      "Secondary collision injuries",
      "Severe trauma from multiple hits",
      "Delayed rescue/treatment",
      "Fire or explosion injuries"
    ],
    liabilityFactors: [
      "Fault allocation among multiple parties",
      "Multiple insurance policies available",
      "Order of impacts affecting liability",
      "Comparative fault percentages",
      "Joint and several liability rules"
    ],
    potentialDefendants: [
      "Multiple negligent drivers",
      "Rideshare driver(s)",
      "Uber/Lyft (multiple policies potentially)",
      "Commercial vehicle companies",
      "Government entities"
    ],
    averageSettlement: "$75,000 - $2,000,000+",
    keyLegalPoints: [
      "Multiple insurance policies may stack",
      "Comparative fault among defendants",
      "Expert accident reconstruction often needed",
      "Subrogation claims between insurers",
      "Each defendant may point finger at others",
      "Early investigation critical before evidence lost"
    ],
    insuranceCoverage: "Multiple $1M policies possible if multiple rideshare vehicles"
  }
];

export function getCaseTypeBySlug(slug: string): CaseType | undefined {
  return caseTypes.find(ct => ct.slug === slug);
}
