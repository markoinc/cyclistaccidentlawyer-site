export interface CaseType {
  slug: string;
  title: string;
  shortTitle: string;
  description: string;
  icon: string;
  commonInjuries: string[];
  averageSettlement: string;
  keyFacts: string[];
  content: string;
}

export const caseTypes: CaseType[] = [
  {
    slug: "dooring-accidents",
    title: "Bicycle Dooring Accident Lawyer",
    shortTitle: "Dooring Accidents",
    description: "Injured when a car door opened into your path? Learn about your legal rights and how to recover compensation.",
    icon: "🚗",
    commonInjuries: ["Broken collarbone", "Head injuries", "Road rash", "Shoulder injuries", "Facial lacerations"],
    averageSettlement: "$25,000 - $150,000",
    keyFacts: [
      "One of the most common urban cycling accidents",
      "Driver or passenger who opens door is typically liable",
      "Protected bike lanes reduce dooring risk",
      "Many cities have specific anti-dooring laws"
    ],
    content: "Dooring accidents occur when a vehicle occupant opens their door into the path of an oncoming cyclist. These crashes often happen suddenly, giving cyclists no time to react. The impact can throw riders into traffic, causing secondary collisions with moving vehicles."
  },
  {
    slug: "right-hook-accidents",
    title: "Right Hook Bicycle Accident Lawyer",
    shortTitle: "Right Hook Crashes",
    description: "Hit by a vehicle turning right? These dangerous intersection accidents require experienced legal representation.",
    icon: "↩️",
    commonInjuries: ["Broken bones", "TBI", "Spinal injuries", "Internal bleeding", "Leg fractures"],
    averageSettlement: "$50,000 - $500,000+",
    keyFacts: [
      "Driver fails to check for cyclists before turning",
      "Often occurs at intersections with bike lanes",
      "Large trucks and buses have significant blind spots",
      "Usually results in serious injuries"
    ],
    content: "Right hook accidents happen when a vehicle passes a cyclist and then immediately turns right, cutting across the cyclist's path. These crashes are especially common with large commercial vehicles that have significant blind spots on their right side."
  },
  {
    slug: "hit-and-run",
    title: "Bicycle Hit and Run Accident Lawyer",
    shortTitle: "Hit and Run",
    description: "Driver fled after hitting you? Time is critical to identify the driver and preserve evidence.",
    icon: "🏃",
    commonInjuries: ["Various severe injuries", "TBI", "Broken bones", "Spinal cord damage", "Psychological trauma"],
    averageSettlement: "$75,000 - $1,000,000+",
    keyFacts: [
      "Time is critical for evidence preservation",
      "Uninsured motorist coverage may apply",
      "Police investigation essential",
      "Witnesses and surveillance footage crucial"
    ],
    content: "Hit and run bicycle accidents add another layer of complexity to an already traumatic experience. When a driver flees the scene, victims face challenges identifying the at-fault party. However, experienced attorneys can work with police, access traffic cameras, and locate witnesses."
  },
  {
    slug: "intersection-accidents",
    title: "Intersection Bicycle Accident Lawyer",
    shortTitle: "Intersection Crashes",
    description: "Intersections are the most dangerous places for cyclists. Learn your rights after an intersection crash.",
    icon: "🔀",
    commonInjuries: ["Head trauma", "Multiple fractures", "Internal injuries", "Spinal damage", "Traumatic injuries"],
    averageSettlement: "$50,000 - $750,000+",
    keyFacts: [
      "Most dangerous location for cyclists",
      "Drivers running red lights common cause",
      "Left turns across cyclist path frequent",
      "Poor visibility often a factor"
    ],
    content: "Intersections are where most fatal bicycle accidents occur. Cyclists face threats from vehicles running red lights, making illegal turns, and failing to yield. Even with dedicated bike signals, intersection crashes remain common due to driver negligence and poor infrastructure design."
  },
  {
    slug: "bike-lane-violations",
    title: "Bike Lane Violation Accident Lawyer",
    shortTitle: "Bike Lane Violations",
    description: "Vehicle entered the bike lane and hit you? Drivers who violate bike lanes can be held liable.",
    icon: "🛤️",
    commonInjuries: ["Road rash", "Broken bones", "Concussion", "Soft tissue injuries", "Wrist fractures"],
    averageSettlement: "$20,000 - $200,000",
    keyFacts: [
      "Vehicles illegally entering bike lanes",
      "Double-parked cars forcing cyclists out",
      "Delivery vehicles common violators",
      "Protected lanes safer than painted lines"
    ],
    content: "Bike lanes are meant to protect cyclists, but when drivers illegally enter these spaces, serious accidents occur. Whether a vehicle was parked, driving, or crossing without yielding, the driver may be liable for injuries caused by bike lane violations."
  },
  {
    slug: "road-hazard-accidents",
    title: "Road Hazard Bicycle Accident Lawyer",
    shortTitle: "Road Hazards",
    description: "Crashed due to potholes, debris, or poor road design? Government entities may be liable.",
    icon: "🕳️",
    commonInjuries: ["Collarbone fractures", "Wrist injuries", "Head trauma", "Hip injuries", "Road rash"],
    averageSettlement: "$15,000 - $150,000",
    keyFacts: [
      "Potholes, cracks, and debris common causes",
      "Government entities may be liable",
      "Strict notice requirements often apply",
      "Documentation of hazard critical"
    ],
    content: "Not all bicycle accidents involve vehicles. Road hazards like potholes, debris, missing signage, and poor design can cause serious crashes. When government negligence in maintaining roads causes injuries, victims may have claims against the responsible public entity."
  },
  {
    slug: "rear-end-collisions",
    title: "Rear-End Bicycle Collision Lawyer",
    shortTitle: "Rear-End Collisions",
    description: "Hit from behind while cycling? These devastating crashes often result in severe injuries.",
    icon: "💥",
    commonInjuries: ["Spinal injuries", "TBI", "Internal bleeding", "Multiple fractures", "Paralysis"],
    averageSettlement: "$100,000 - $1,000,000+",
    keyFacts: [
      "Often caused by distracted drivers",
      "High-speed impacts cause severe injuries",
      "Driver almost always at fault",
      "Cyclists have no time to react"
    ],
    content: "Rear-end bicycle collisions occur when a vehicle strikes a cyclist from behind. These crashes are particularly dangerous because cyclists have no warning and cannot take evasive action. Distracted driving, speeding, and impaired driving are common causes."
  },
  {
    slug: "left-cross-accidents",
    title: "Left Cross Bicycle Accident Lawyer",
    shortTitle: "Left Cross Crashes",
    description: "Hit by an oncoming vehicle turning left? These high-impact crashes cause serious injuries.",
    icon: "↪️",
    commonInjuries: ["Multiple fractures", "Head injuries", "Internal injuries", "Pelvic fractures", "Spinal damage"],
    averageSettlement: "$75,000 - $500,000+",
    keyFacts: [
      "Vehicle turns left into cyclist's path",
      "Driver often claims they didn't see cyclist",
      "High-speed impacts common",
      "Intersection design often a factor"
    ],
    content: "Left cross accidents happen when an oncoming vehicle turns left across a cyclist's path. The turning driver often claims they didn't see the cyclist, but visibility is the driver's responsibility. These high-impact crashes frequently result in catastrophic injuries."
  },
  {
    slug: "commercial-vehicle-accidents",
    title: "Commercial Vehicle Bicycle Accident Lawyer",
    shortTitle: "Commercial Vehicles",
    description: "Hit by a truck, bus, or delivery vehicle? Commercial vehicle accidents involve complex liability.",
    icon: "🚛",
    commonInjuries: ["Catastrophic injuries", "Wrongful death", "Amputation", "Severe TBI", "Paralysis"],
    averageSettlement: "$200,000 - $5,000,000+",
    keyFacts: [
      "Larger vehicles cause more severe injuries",
      "Multiple liable parties possible",
      "Commercial insurance provides more coverage",
      "FMCSA regulations may apply to trucks"
    ],
    content: "Accidents involving commercial vehicles—trucks, buses, delivery vehicles—often result in catastrophic injuries or death due to the size and weight of these vehicles. These cases are complex because multiple parties may be liable, including the driver, company, and vehicle owner."
  },
  {
    slug: "distracted-driver-accidents",
    title: "Distracted Driver Bicycle Accident Lawyer",
    shortTitle: "Distracted Drivers",
    description: "Hit by a driver who was texting or distracted? Prove negligence and recover compensation.",
    icon: "📱",
    commonInjuries: ["Various severe injuries", "TBI", "Spinal injuries", "Broken bones", "Death"],
    averageSettlement: "$50,000 - $500,000+",
    keyFacts: [
      "Texting while driving major cause",
      "Phone records can prove distraction",
      "Higher negligence may lead to punitive damages",
      "Many states have distracted driving laws"
    ],
    content: "Distracted driving is a leading cause of bicycle accidents. When drivers text, use apps, or are otherwise distracted, they fail to see cyclists. Phone records, witness testimony, and accident reconstruction can prove distraction and strengthen your case."
  },
  {
    slug: "drunk-driver-accidents",
    title: "Drunk Driver Bicycle Accident Lawyer",
    shortTitle: "Drunk Drivers",
    description: "Hit by an impaired driver? Victims of drunk driving crashes may recover additional damages.",
    icon: "🍺",
    commonInjuries: ["Catastrophic injuries", "Death", "TBI", "Spinal damage", "Severe trauma"],
    averageSettlement: "$100,000 - $2,000,000+",
    keyFacts: [
      "Criminal charges don't guarantee civil recovery",
      "Punitive damages often available",
      "Dram shop laws may apply",
      "BAC evidence crucial"
    ],
    content: "When a drunk driver hits a cyclist, victims may be entitled to punitive damages beyond standard compensation. These cases often involve criminal proceedings, but civil claims are separate and can recover compensation for injuries regardless of criminal outcomes."
  },
  {
    slug: "ebike-accidents",
    title: "E-Bike Accident Lawyer",
    shortTitle: "E-Bike Accidents",
    description: "Injured on an electric bicycle? E-bike accidents involve unique legal considerations.",
    icon: "⚡",
    commonInjuries: ["Similar to traditional bike injuries", "Higher speed impacts", "TBI", "Broken bones"],
    averageSettlement: "$25,000 - $300,000",
    keyFacts: [
      "E-bike classification affects legal rights",
      "Higher speeds may increase injury severity",
      "Some states have specific e-bike laws",
      "Product liability claims may apply"
    ],
    content: "E-bike accidents present unique legal challenges. Electric bicycles can travel at higher speeds, and their classification varies by state. Depending on the e-bike class and state law, different traffic rules may apply. Additionally, product liability claims may be possible for defective e-bikes."
  },
  {
    slug: "pedestrian-cyclist-collisions",
    title: "Pedestrian-Cyclist Collision Lawyer",
    shortTitle: "Pedestrian Collisions",
    description: "Collided with a pedestrian while cycling? Understand liability and protect your rights.",
    icon: "🚶",
    commonInjuries: ["Varying severity", "Road rash", "Fractures", "Head injuries"],
    averageSettlement: "$10,000 - $100,000",
    keyFacts: [
      "Fault determination can be complex",
      "Shared path rules apply",
      "Insurance coverage may be limited",
      "Both parties may share liability"
    ],
    content: "Cyclist-pedestrian collisions can occur on shared paths, sidewalks, or crosswalks. Fault determination depends on right-of-way rules, which vary by location. Cyclists may be liable for injuries to pedestrians, but they may also have claims when pedestrians act negligently."
  },
  {
    slug: "child-bicycle-accidents",
    title: "Child Bicycle Accident Lawyer",
    shortTitle: "Child Cyclists",
    description: "Your child was injured cycling? Protect their rights to full compensation for injuries.",
    icon: "👧",
    commonInjuries: ["TBI", "Broken bones", "Dental injuries", "Psychological trauma", "Growth plate damage"],
    averageSettlement: "$50,000 - $1,000,000+",
    keyFacts: [
      "Longer statute of limitations for minors",
      "Growth plate injuries need special attention",
      "Future damages must be calculated",
      "Court approval required for settlements"
    ],
    content: "When children are injured in bicycle accidents, special legal considerations apply. The statute of limitations may be extended until they reach adulthood. Cases must account for future medical needs, lost earning capacity, and the impact on development. Courts must approve any settlements."
  },
  {
    slug: "wrongful-death",
    title: "Bicycle Wrongful Death Lawyer",
    shortTitle: "Wrongful Death",
    description: "Lost a loved one in a bicycle accident? Families may recover damages for their loss.",
    icon: "🕯️",
    commonInjuries: ["Fatal injuries"],
    averageSettlement: "$500,000 - $10,000,000+",
    keyFacts: [
      "Family members can file claims",
      "Recoverable damages include funeral costs",
      "Lost future income calculated",
      "Emotional damages for survivors"
    ],
    content: "When a cyclist dies due to another's negligence, surviving family members can pursue a wrongful death claim. These cases can recover funeral expenses, lost income the deceased would have earned, loss of companionship, and emotional suffering of survivors."
  }
];

export function getCaseTypeBySlug(slug: string): CaseType | undefined {
  return caseTypes.find(ct => ct.slug === slug);
}
