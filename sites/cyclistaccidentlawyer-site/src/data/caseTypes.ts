// Case types for bicycle accident law pages
export interface CaseType {
  name: string;
  slug: string;
  shortDescription: string;
  description: string;
  commonCauses: string[];
  typicalInjuries: string[];
  liabilityFactors: string[];
  averageSettlement: string;
  keyLegalPoints: string[];
}

export const caseTypes: CaseType[] = [
  {
    name: "Dooring Accidents",
    slug: "dooring-accidents",
    shortDescription: "Crashes when vehicle occupants open doors into cyclists' paths.",
    description: "Dooring accidents occur when a driver or passenger opens their vehicle door into the path of an approaching cyclist. These crashes often happen suddenly, giving cyclists no time to react. The cyclist may hit the door directly, be thrown from their bike, or swerve into traffic. Dooring is one of the most common and dangerous types of urban cycling crashes.",
    commonCauses: [
      "Driver failing to check mirror before opening door",
      "Passenger not looking for cyclists",
      "Hurried exit from vehicles",
      "Rideshare pickups and dropoffs",
      "Delivery vehicle occupants",
      "Parallel parking in bike lanes"
    ],
    typicalInjuries: [
      "Broken collar bones and shoulders",
      "Facial injuries and dental damage",
      "Traumatic brain injuries",
      "Road rash and lacerations",
      "Broken arms and wrists",
      "Spinal injuries"
    ],
    liabilityFactors: [
      "State dooring laws requiring checking before opening",
      "Whether cyclist was in marked bike lane",
      "Visibility conditions",
      "Whether door opener was driver or passenger",
      "Rideshare company policies"
    ],
    averageSettlement: "$25,000 - $250,000 depending on injury severity",
    keyLegalPoints: [
      "Vehicle occupants have a legal duty to check for cyclists",
      "Many states have specific dooring statutes",
      "Cyclist right-of-way in bike lanes is protected",
      "Rideshare companies may share liability",
      "Secondary impacts with traffic can increase damages"
    ]
  },
  {
    name: "Right-Hook Accidents",
    slug: "right-hook-accidents",
    shortDescription: "Crashes when vehicles turn right across a cyclist's path.",
    description: "Right-hook accidents happen when a motor vehicle makes a right turn across the path of a cyclist traveling straight in the same direction. The driver may overtake the cyclist and turn immediately, or turn without seeing the cyclist alongside. These crashes often result in the cyclist being struck by the side of the vehicle or run over by its wheels.",
    commonCauses: [
      "Driver failing to check mirrors before turning",
      "Driver not seeing cyclist in blind spot",
      "Driver passing cyclist then turning immediately",
      "Driver misjudging cyclist's speed",
      "Large vehicle blind spots",
      "Distracted driving"
    ],
    typicalInjuries: [
      "Crushing injuries from vehicle wheels",
      "Broken bones throughout body",
      "Head and brain injuries",
      "Internal organ damage",
      "Spinal cord injuries",
      "Fatal injuries in severe cases"
    ],
    liabilityFactors: [
      "Driver's duty to yield to through traffic",
      "Whether driver signaled the turn",
      "Presence of bike lane",
      "Driver's speed before turning",
      "Cyclist's visibility and position"
    ],
    averageSettlement: "$50,000 - $500,000+ depending on injury severity",
    keyLegalPoints: [
      "Turning vehicles must yield to through traffic",
      "Drivers must check for cyclists before turning",
      "Blind spots don't excuse failure to look",
      "Commercial vehicle companies may be liable",
      "Bike boxes and infrastructure can affect cases"
    ]
  },
  {
    name: "Left-Cross Accidents",
    slug: "left-cross-accidents",
    shortDescription: "Crashes when oncoming vehicles turn left across a cyclist's path.",
    description: "Left-cross accidents occur when an oncoming vehicle turns left and crosses the path of a cyclist traveling straight. The driver typically misjudges the cyclist's speed or fails to see them at all. The cyclist strikes the side of the turning vehicle, often resulting in the rider being thrown over or into the vehicle.",
    commonCauses: [
      "Driver underestimating cyclist speed",
      "Inattentional blindness to cyclists",
      "Rushing to complete the turn",
      "Distracted driving",
      "Obstructed view from other traffic",
      "Inadequate intersection design"
    ],
    typicalInjuries: [
      "Impact injuries to head and torso",
      "Being thrown over vehicle",
      "Broken bones from impact",
      "Head and facial injuries",
      "Soft tissue damage",
      "Psychological trauma"
    ],
    liabilityFactors: [
      "Driver's clear duty to yield to oncoming traffic",
      "Cyclist's visibility and lighting",
      "Traffic signal status",
      "Intersection sight lines",
      "Driver's claimed vs. actual observation"
    ],
    averageSettlement: "$40,000 - $400,000 depending on injury severity",
    keyLegalPoints: [
      "Left-turning vehicles always yield to oncoming traffic",
      "SMIDSY ('Sorry, I didn't see you') is not a valid defense",
      "Cyclist speed doesn't eliminate driver's duty",
      "Intersection design may create additional liability",
      "Distraction evidence can increase damages"
    ]
  },
  {
    name: "Rear-End Collisions",
    slug: "rear-end-collisions",
    shortDescription: "Crashes when vehicles strike cyclists from behind.",
    description: "Rear-end collisions occur when a motor vehicle strikes a cyclist from behind. These crashes often happen when drivers are distracted, speeding, or fail to give adequate space. Rear-end crashes can be especially devastating because cyclists cannot see the danger approaching and have no opportunity to brace or evade.",
    commonCauses: [
      "Distracted driving (phone use)",
      "Tailgating or following too closely",
      "Speeding and inability to stop",
      "Impaired driving",
      "Sun glare affecting visibility",
      "Poor lighting conditions"
    ],
    typicalInjuries: [
      "Spinal cord injuries",
      "Traumatic brain injuries",
      "Internal bleeding",
      "Broken bones",
      "Whiplash-type injuries",
      "Fatal injuries"
    ],
    liabilityFactors: [
      "Driver's duty to maintain safe following distance",
      "Evidence of distraction or impairment",
      "Speed at time of impact",
      "Cyclist's lighting and reflective equipment",
      "Road conditions and visibility"
    ],
    averageSettlement: "$75,000 - $1,000,000+ for serious injuries",
    keyLegalPoints: [
      "Following drivers are almost always at fault",
      "Cyclists have a right to use the road",
      "Distracted driving may support punitive damages",
      "Serious injuries often result in larger settlements",
      "Hit-and-run rear collisions have special considerations"
    ]
  },
  {
    name: "Intersection Accidents",
    slug: "intersection-accidents",
    shortDescription: "Crashes at intersections involving failure to yield or signal violations.",
    description: "Intersection accidents encompass all crashes occurring at street crossings, including right-of-way violations, signal violations, and failure to yield. Intersections are the most dangerous locations for cyclists because they concentrate conflict points between cyclists and motor vehicles.",
    commonCauses: [
      "Running red lights or stop signs",
      "Failure to yield right-of-way",
      "Right turns on red without checking",
      "Left turns across bike lanes",
      "Blocked views from large vehicles",
      "Inadequate intersection design"
    ],
    typicalInjuries: [
      "All types of impact injuries",
      "Broken bones",
      "Head and brain injuries",
      "Internal injuries",
      "Road rash",
      "Crushing injuries in severe cases"
    ],
    liabilityFactors: [
      "Traffic signal status",
      "Right-of-way rules",
      "Witness observations",
      "Camera footage",
      "Police report findings"
    ],
    averageSettlement: "$30,000 - $500,000 depending on circumstances",
    keyLegalPoints: [
      "Cyclists have equal right-of-way to motor vehicles",
      "Signal violations establish negligence per se",
      "Bike boxes and bike signals affect right-of-way",
      "Multiple vehicles may share liability",
      "City may be liable for poor intersection design"
    ]
  },
  {
    name: "Hit-and-Run Accidents",
    slug: "hit-and-run-accidents",
    shortDescription: "Crashes where the driver flees the scene without stopping.",
    description: "Hit-and-run accidents occur when a driver strikes a cyclist and leaves the scene without stopping to provide information or assistance. These cases present unique challenges because the at-fault driver may not be identified. However, victims still have options for compensation through their own insurance and other sources.",
    commonCauses: [
      "Driver panic after crash",
      "Impaired or unlicensed drivers",
      "Uninsured drivers",
      "Drivers with warrants",
      "Late-night incidents with fewer witnesses",
      "High-speed roads"
    ],
    typicalInjuries: [
      "All types of bicycle accident injuries",
      "Often more severe due to higher speeds",
      "Delayed treatment if cyclist incapacitated",
      "Psychological trauma from abandonment"
    ],
    liabilityFactors: [
      "Identification of the driver",
      "Available insurance coverage",
      "Uninsured motorist coverage",
      "Criminal investigation outcome",
      "Witness availability"
    ],
    averageSettlement: "Varies widely based on whether driver is found",
    keyLegalPoints: [
      "Police investigation is critical",
      "UM/UIM coverage may apply",
      "Criminal restitution possible if driver caught",
      "Medical payments coverage helps immediately",
      "Evidence preservation is time-sensitive"
    ]
  },
  {
    name: "Commercial Vehicle Accidents",
    slug: "commercial-vehicle-accidents",
    shortDescription: "Crashes involving trucks, buses, delivery vehicles, and other commercial vehicles.",
    description: "Commercial vehicle accidents involve crashes with trucks, buses, delivery vehicles, taxis, rideshare vehicles, and other commercial operators. These cases often result in more severe injuries due to vehicle size and may involve multiple liable parties including drivers, companies, and insurers.",
    commonCauses: [
      "Large vehicle blind spots",
      "Wide turning radius",
      "Driver fatigue or pressure",
      "Delivery time pressure",
      "Improper training",
      "Company policy violations"
    ],
    typicalInjuries: [
      "Crushing injuries",
      "Severe fractures",
      "Traumatic brain injuries",
      "Spinal cord injuries",
      "Internal organ damage",
      "Fatal injuries"
    ],
    liabilityFactors: [
      "Federal motor carrier regulations",
      "Company negligent hiring/training",
      "Vehicle maintenance records",
      "Driver logs and hours",
      "Company policies and procedures"
    ],
    averageSettlement: "$100,000 - $2,000,000+ for serious injuries",
    keyLegalPoints: [
      "Commercial insurance policies are larger",
      "Multiple parties may be liable",
      "Federal regulations may apply",
      "Evidence preservation is critical",
      "Black box and log data are important"
    ]
  },
  {
    name: "Drunk/Impaired Driver Accidents",
    slug: "drunk-impaired-driver-accidents",
    shortDescription: "Crashes caused by drivers under the influence of alcohol or drugs.",
    description: "Impaired driver accidents involve cyclists struck by drivers under the influence of alcohol, drugs, or medications. These cases often result in severe injuries because impaired drivers have delayed reactions and poor judgment. Criminal charges typically accompany civil claims, which may support punitive damages.",
    commonCauses: [
      "Alcohol impairment",
      "Drug impairment (legal or illegal)",
      "Prescription medication effects",
      "Drowsy driving",
      "Distracted driving"
    ],
    typicalInjuries: [
      "Severe impact injuries",
      "Higher fatality rate",
      "Multiple injury sites",
      "Traumatic brain injuries",
      "Spinal cord injuries"
    ],
    liabilityFactors: [
      "Blood alcohol concentration",
      "Drug test results",
      "Criminal conviction",
      "Witness observations of impairment",
      "Bar or social host liability"
    ],
    averageSettlement: "$100,000 - $1,000,000+ plus potential punitive damages",
    keyLegalPoints: [
      "Impairment establishes clear negligence",
      "Punitive damages may be available",
      "Dram shop laws may create bar liability",
      "Criminal case outcome affects civil claim",
      "Insurance may not cover punitive damages"
    ]
  },
  {
    name: "Road Hazard Accidents",
    slug: "road-hazard-accidents",
    shortDescription: "Crashes caused by potholes, debris, dangerous grates, and road defects.",
    description: "Road hazard accidents occur when dangerous conditions on the road cause cyclists to crash. This includes potholes, debris, dangerous drainage grates, uneven pavement, and construction hazards. Cities and property owners may be liable for failing to maintain safe road conditions.",
    commonCauses: [
      "Potholes and road deterioration",
      "Dangerous drainage grates",
      "Loose gravel or debris",
      "Construction zone hazards",
      "Uneven pavement",
      "Railroad and streetcar tracks"
    ],
    typicalInjuries: [
      "Over-handlebar crashes",
      "Broken collar bones",
      "Head injuries",
      "Wrist and arm fractures",
      "Road rash",
      "Hip and pelvis injuries"
    ],
    liabilityFactors: [
      "Government knowledge of hazard",
      "Time hazard existed",
      "Maintenance schedules",
      "Prior reports or complaints",
      "Industry safety standards"
    ],
    averageSettlement: "$20,000 - $200,000 depending on injuries and liability",
    keyLegalPoints: [
      "Government claims have short deadlines",
      "Notice requirements must be met",
      "Prior incidents strengthen claims",
      "Design immunity may limit some claims",
      "Private property rules differ from public"
    ]
  },
  {
    name: "Distracted Driver Accidents",
    slug: "distracted-driver-accidents",
    shortDescription: "Crashes caused by drivers distracted by phones, passengers, or other activities.",
    description: "Distracted driver accidents involve crashes where the driver's attention was diverted from the road. Cell phone use is the most common distraction, but eating, passengers, entertainment systems, and other activities also cause crashes. Evidence of distraction can significantly strengthen a bicycle accident claim.",
    commonCauses: [
      "Texting while driving",
      "Phone calls",
      "Navigation apps",
      "Social media use",
      "Eating and drinking",
      "Adjusting vehicle controls"
    ],
    typicalInjuries: [
      "All types of bicycle crash injuries",
      "Often more severe due to no evasive action",
      "Higher fatality rate",
      "Multiple impact injuries"
    ],
    liabilityFactors: [
      "Cell phone records",
      "Witness observations",
      "Dashcam footage",
      "Driver admissions",
      "Accident reconstruction"
    ],
    averageSettlement: "$50,000 - $500,000+ with distraction evidence",
    keyLegalPoints: [
      "Cell phone records are discoverable",
      "Texting laws create negligence per se",
      "Distraction evidence increases liability",
      "May support punitive damages",
      "Commercial drivers face stricter rules"
    ]
  },
  {
    name: "Sidewalk and Path Accidents",
    slug: "sidewalk-path-accidents",
    shortDescription: "Crashes occurring on sidewalks, multi-use paths, and bike paths.",
    description: "Sidewalk and path accidents involve crashes in areas shared with pedestrians or on designated bike paths. These may involve conflicts with pedestrians, obstacles, or vehicles crossing paths. Legal rights vary by location and path type.",
    commonCauses: [
      "Vehicle crossing path without yielding",
      "Pedestrian conflicts",
      "Path design defects",
      "Surface hazards",
      "Visibility issues at crossings",
      "E-bike speed differentials"
    ],
    typicalInjuries: [
      "Lower speed but still significant injuries",
      "Falls and fractures",
      "Collision injuries",
      "Head injuries",
      "Wrist and arm injuries"
    ],
    liabilityFactors: [
      "Right-of-way rules for the specific path",
      "Path design and maintenance",
      "Speed appropriateness",
      "Crossing driver's duty to yield",
      "Property owner maintenance"
    ],
    averageSettlement: "$10,000 - $150,000 depending on circumstances",
    keyLegalPoints: [
      "Cyclists may or may not have path priority",
      "Drivers crossing paths must yield",
      "Path maintenance creates owner liability",
      "Local laws govern path use",
      "Speed regulations may affect liability"
    ]
  },
  {
    name: "Parking Lot Accidents",
    slug: "parking-lot-accidents",
    shortDescription: "Crashes occurring in parking lots, garages, and private property.",
    description: "Parking lot accidents happen when cyclists are struck while riding through parking areas. Drivers backing out of spaces, turning without looking, and driving too fast are common causes. Property owners may share liability for dangerous conditions.",
    commonCauses: [
      "Drivers backing out without looking",
      "Drivers not checking for cyclists before turning",
      "Poor visibility in garages",
      "Excessive speed in lots",
      "Inadequate lighting",
      "Poor traffic flow design"
    ],
    typicalInjuries: [
      "Usually moderate due to lower speeds",
      "Falls and fractures",
      "Impact injuries",
      "Head injuries if not wearing helmet"
    ],
    liabilityFactors: [
      "Driver's duty of care in lots",
      "Property owner maintenance",
      "Lighting and visibility",
      "Signage and traffic control",
      "Cyclist's right to be in the area"
    ],
    averageSettlement: "$15,000 - $100,000 depending on injuries",
    keyLegalPoints: [
      "Drivers owe duty of care in parking lots",
      "Property owners have maintenance obligations",
      "Private property rules differ from public roads",
      "Premises liability may apply",
      "Insurance coverage may differ"
    ]
  }
];

export function getCaseTypeBySlug(slug: string): CaseType | undefined {
  return caseTypes.find(ct => ct.slug === slug);
}

export function getCaseTypeCount(): number {
  return caseTypes.length;
}
