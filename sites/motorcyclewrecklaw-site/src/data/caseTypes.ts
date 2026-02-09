// Case types data for motorcycle accident law pages

export interface CaseTypeData {
  name: string;
  slug: string;
  shortDescription: string;
  fullDescription: string;
  commonInjuries: string[];
  uniqueFactors: string[];
  averageSettlement: string;
  proofRequired: string[];
  icon: string;
}

export const caseTypes: CaseTypeData[] = [
  {
    name: "Cruiser Accidents",
    slug: "cruiser-accidents",
    shortDescription: "Accidents involving cruiser-style motorcycles like Harley-Davidson, Indian, and similar bikes.",
    fullDescription: "Cruiser motorcycles are among the most popular bikes on American roads, known for their laid-back riding position and powerful engines. However, their lower center of gravity and heavier weight can create unique challenges in accident scenarios. Cruiser riders often face severe injuries due to the relaxed riding position that can lead to different impact dynamics compared to sport bikes.",
    commonInjuries: ["Lower extremity fractures", "Hip injuries", "Spinal cord damage", "Road rash", "Traumatic brain injury", "Shoulder and arm injuries"],
    uniqueFactors: ["Heavy bike weight affects crash dynamics", "Lower riding position impacts visibility", "Extended forward controls change injury patterns", "Chrome and accessories can cause additional injury", "Passenger injuries common due to two-up riding"],
    averageSettlement: "$75,000 - $250,000+",
    proofRequired: ["Police report", "Witness statements", "Medical records", "Photos of bike damage", "Expert accident reconstruction"],
    icon: "🏍️"
  },
  {
    name: "Sportbike Accidents",
    slug: "sportbike-accidents",
    shortDescription: "High-performance motorcycle accidents involving speed and agility-focused bikes.",
    fullDescription: "Sportbikes are designed for speed, acceleration, and agility. Their forward-leaning riding position and high-performance capabilities make them exciting to ride but also increase certain risk factors. Accidents involving sportbikes often occur at higher speeds and can result in more severe injuries. Insurance companies frequently try to blame sportbike riders regardless of actual fault.",
    commonInjuries: ["High-speed road rash", "Multiple fractures", "Internal organ damage", "Traumatic brain injuries", "Spinal injuries", "Severe extremity injuries"],
    uniqueFactors: ["Higher average speeds increase injury severity", "Aggressive styling leads to bias against riders", "Forward riding position affects impact patterns", "Lighter weight means less crash protection", "Performance modifications may affect claims"],
    averageSettlement: "$100,000 - $500,000+",
    proofRequired: ["Speed analysis data", "Witness testimony", "Accident reconstruction", "Medical expert testimony", "Gear and helmet condition documentation"],
    icon: "🏎️"
  },
  {
    name: "Touring Accidents",
    slug: "touring-accidents",
    shortDescription: "Accidents involving large touring motorcycles designed for long-distance travel.",
    fullDescription: "Touring motorcycles like Honda Gold Wings, BMW R1250RT, and Harley-Davidson Road Glides are built for comfort on long journeys. Their large size, heavy weight, and two-up riding configuration create unique accident dynamics. Touring bike accidents often involve multiple injuries to both rider and passenger, and the substantial vehicle weight can complicate rescue and medical response.",
    commonInjuries: ["Crush injuries from bike weight", "Multiple passenger injuries", "Lower extremity trauma", "Burns from hot engine components", "Head and neck injuries", "Fatigue-related injuries"],
    uniqueFactors: ["Extreme weight (800+ lbs loaded)", "Two-up passenger considerations", "Long-distance fatigue factors", "Luggage and accessories as hazards", "Higher average age of touring riders"],
    averageSettlement: "$100,000 - $400,000+",
    proofRequired: ["Maintenance records", "Trip documentation", "Passenger statements", "Medical records for all parties", "Expert testimony on touring bike dynamics"],
    icon: "🛣️"
  },
  {
    name: "Dirt Bike Accidents",
    slug: "dirt-bike-accidents",
    shortDescription: "Off-road and dual-sport motorcycle accidents on trails, tracks, and roads.",
    fullDescription: "Dirt bikes and dual-sport motorcycles present unique legal challenges because accidents can occur on private property, public trails, or roadways. While some dirt bike accidents involve only the rider, many cases involve collisions with other vehicles, property owner negligence, or defective equipment. Understanding the specific legal issues for off-road accidents is critical.",
    commonInjuries: ["Broken bones from jumps/falls", "Concussions", "Neck and spine injuries", "Knee and ankle damage", "Facial injuries", "Internal injuries"],
    uniqueFactors: ["Location determines legal jurisdiction", "Property owner liability issues", "Equipment manufacturer liability", "Racing/competition exclusions", "Insurance coverage gaps common"],
    averageSettlement: "$50,000 - $200,000+",
    proofRequired: ["Property ownership documentation", "Equipment maintenance records", "Witness statements", "Medical records", "Photos/video of accident scene"],
    icon: "🏔️"
  },
  {
    name: "Scooter Accidents",
    slug: "scooter-accidents",
    shortDescription: "Accidents involving motor scooters and low-displacement urban transportation.",
    fullDescription: "Scooters are increasingly popular for urban commuting, but their smaller size makes them even less visible than motorcycles. Scooter riders face unique dangers including being overlooked by larger vehicles, limited acceleration for defensive maneuvers, and smaller wheels that are more vulnerable to road hazards. Many scooter accidents occur at intersections where drivers fail to yield.",
    commonInjuries: ["Leg and foot injuries", "Road rash", "Head trauma (often lower helmet use)", "Arm and wrist fractures", "Facial injuries", "Pelvic injuries"],
    uniqueFactors: ["Smaller profile increases invisibility", "Lower speed limits perception of injury severity", "Step-through design affects injury patterns", "Urban environment hazards", "Often inadequate insurance coverage"],
    averageSettlement: "$25,000 - $150,000+",
    proofRequired: ["Traffic camera footage", "Intersection witness statements", "Urban traffic pattern analysis", "Medical documentation", "Insurance policy review"],
    icon: "🛵"
  },
  {
    name: "Moped Accidents",
    slug: "moped-accidents",
    shortDescription: "Accidents involving mopeds and low-powered motorized bicycles.",
    fullDescription: "Mopeds occupy a legal gray area in many states, sometimes classified as motorcycles and other times as motorized bicycles. This classification affects licensing, insurance, and legal liability. Moped accidents often involve riders with less training and experience, and the vehicles' low speed and small size create significant vulnerability in traffic.",
    commonInjuries: ["Lower extremity injuries", "Head trauma", "Road rash", "Facial injuries", "Spinal injuries", "Soft tissue damage"],
    uniqueFactors: ["Variable state classifications", "Often no helmet requirement", "Minimal rider training required", "Speed differential with traffic", "Insurance coverage complications"],
    averageSettlement: "$20,000 - $100,000+",
    proofRequired: ["State classification documentation", "Licensing requirements proof", "Insurance policy analysis", "Witness statements", "Medical records"],
    icon: "🚲"
  },
  {
    name: "Trike Accidents",
    slug: "trike-accidents",
    shortDescription: "Accidents involving three-wheeled motorcycles and trikes.",
    fullDescription: "Three-wheeled motorcycles (trikes) are popular among riders who want stability or have physical limitations that prevent traditional motorcycle riding. However, trikes handle differently than two-wheeled motorcycles, particularly in turns and emergency maneuvers. Trike accidents often involve unique dynamics that require specialized accident reconstruction expertise.",
    commonInjuries: ["Ejection injuries", "Crush injuries", "Rollover-related trauma", "Head and neck injuries", "Multiple fractures", "Spinal cord damage"],
    uniqueFactors: ["Different handling dynamics than motorcycles", "Rollover risk in tight turns", "Heavier weight affects stopping distance", "Often ridden by older adults", "Conversion kit liability issues"],
    averageSettlement: "$75,000 - $300,000+",
    proofRequired: ["Trike-specific accident reconstruction", "Handling characteristic analysis", "Medical records", "Manufacturer specifications", "Witness testimony"],
    icon: "🔱"
  },
  {
    name: "Sidecar Accidents",
    slug: "sidecar-accidents",
    shortDescription: "Accidents involving motorcycles with attached sidecars.",
    fullDescription: "Sidecar motorcycles present unique handling characteristics that differ significantly from standard motorcycles. The asymmetric weight distribution affects braking, turning, and stability. Sidecar accidents often involve the sidecar passenger, creating additional liability considerations. These cases require attorneys who understand the specialized dynamics of sidecar operation.",
    commonInjuries: ["Sidecar passenger ejection injuries", "Impact injuries from sidecar structure", "Driver crush injuries", "Head trauma", "Multiple fractures", "Internal injuries"],
    uniqueFactors: ["Asymmetric handling characteristics", "Passenger has no control", "Increased width affects lane positioning", "Specialized operator skill required", "Limited manufacturer options for claims"],
    averageSettlement: "$50,000 - $250,000+",
    proofRequired: ["Sidecar attachment documentation", "Operator experience records", "Passenger statements", "Specialized accident reconstruction", "Medical records for all parties"],
    icon: "🏎️"
  },
  {
    name: "Passenger Injuries",
    slug: "passenger-injuries",
    shortDescription: "Claims for motorcycle passengers injured in accidents.",
    fullDescription: "Motorcycle passengers face unique challenges when injured in accidents. Unlike drivers, passengers have no control over the vehicle and cannot take evasive action. Passengers may have claims against the motorcycle operator, other drivers, or both. Understanding the complex liability issues in passenger injury cases is essential for maximum compensation.",
    commonInjuries: ["Ejection injuries", "Burns from exhaust/engine", "Impact with driver", "Road rash", "Lower extremity trauma", "Head and neck injuries"],
    uniqueFactors: ["No control over vehicle operation", "May have claims against multiple parties", "Relationship with driver complicates cases", "Often inadequate insurance coverage", "Passenger assumption of risk arguments"],
    averageSettlement: "$50,000 - $300,000+",
    proofRequired: ["Driver's insurance policy", "Multiple party liability analysis", "Passenger's own insurance", "Medical records", "Relationship documentation"],
    icon: "👥"
  },
  {
    name: "Hit-and-Run Accidents",
    slug: "hit-and-run",
    shortDescription: "Motorcycle accidents where the at-fault driver fled the scene.",
    fullDescription: "Hit-and-run accidents are devastating for motorcyclists. When a driver flees the scene, victims must navigate complex insurance claims and potentially work with law enforcement to identify the responsible party. Uninsured motorist coverage becomes critical in these cases, and experienced attorneys can help maximize recovery even when the at-fault driver is never found.",
    commonInjuries: ["Any injury type possible", "Delayed treatment injuries", "Psychological trauma", "Injuries worsened by delayed response", "Long-term disability"],
    uniqueFactors: ["At-fault driver may never be found", "Uninsured motorist coverage essential", "Police investigation required", "Witness identification critical", "Time-sensitive evidence collection"],
    averageSettlement: "$30,000 - $200,000+ (depends on UM coverage)",
    proofRequired: ["Police report", "Witness statements", "Traffic/security camera footage", "UM policy documentation", "Medical records"],
    icon: "🚗💨"
  },
  {
    name: "Uninsured Motorist Claims",
    slug: "uninsured-motorist",
    shortDescription: "Accidents caused by drivers without adequate insurance coverage.",
    fullDescription: "When a motorcyclist is hit by an uninsured or underinsured driver, their own insurance becomes the primary source of compensation. Navigating uninsured motorist (UM) and underinsured motorist (UIM) claims requires understanding policy language, coverage limits, and the claims process with your own insurance company—who may not have your best interests at heart.",
    commonInjuries: ["All injury types possible", "Financial stress from coverage gaps", "Treatment delays due to insurance uncertainty", "Long-term care concerns"],
    uniqueFactors: ["Own insurance becomes adversarial", "Coverage stacking possibilities", "Policy interpretation disputes", "Bad faith insurance practices", "Multiple policy coordination"],
    averageSettlement: "Limited by policy coverage",
    proofRequired: ["All applicable insurance policies", "At-fault driver's insurance status", "Medical records and bills", "Lost wage documentation", "Future care needs assessment"],
    icon: "📋"
  },
  {
    name: "Drunk Driver Accidents",
    slug: "drunk-driver",
    shortDescription: "Motorcycle accidents caused by intoxicated drivers.",
    fullDescription: "When a drunk driver causes a motorcycle accident, victims may be entitled to both compensatory and punitive damages. DUI/DWI crashes often result in severe injuries due to the impaired driver's inability to react appropriately. Criminal proceedings against the drunk driver can support civil claims, and establishments that over-served alcohol may share liability.",
    commonInjuries: ["Severe trauma from high-impact crashes", "Traumatic brain injury", "Spinal cord damage", "Multiple fractures", "Internal organ damage", "Wrongful death"],
    uniqueFactors: ["Punitive damages available", "Criminal case provides evidence", "Dram shop liability possible", "Higher settlement potential", "Clear liability usually established"],
    averageSettlement: "$100,000 - $1,000,000+",
    proofRequired: ["Police DUI report", "Blood alcohol test results", "Criminal court records", "Bar/restaurant records", "Medical records", "Expert testimony"],
    icon: "🍺"
  },
  {
    name: "Distracted Driver Accidents",
    slug: "distracted-driver",
    shortDescription: "Accidents caused by drivers distracted by phones, GPS, or other factors.",
    fullDescription: "Distracted driving has become an epidemic, and motorcyclists are particularly vulnerable because they're already less visible to attentive drivers. Cell phone records, witness testimony, and accident reconstruction can prove distraction. Distracted driver accidents often result in severe injuries because the driver made no attempt to brake or take evasive action.",
    commonInjuries: ["High-impact trauma", "Rear-end collision injuries", "Intersection impact injuries", "Ejection injuries", "Road rash", "Head trauma"],
    uniqueFactors: ["Cell phone records as evidence", "No evasive action taken", "Social media use increasingly common", "In-vehicle technology distractions", "Corporate liability for employee distraction"],
    averageSettlement: "$75,000 - $500,000+",
    proofRequired: ["Cell phone records subpoena", "Witness statements", "Accident reconstruction", "Police investigation notes", "Medical records", "Expert testimony"],
    icon: "📱"
  },
  {
    name: "Commercial Vehicle Accidents",
    slug: "commercial-vehicle",
    shortDescription: "Motorcycle accidents involving trucks, buses, and commercial vehicles.",
    fullDescription: "Accidents between motorcycles and commercial vehicles—semi-trucks, delivery vans, buses—are often catastrophic due to the massive size and weight differential. Commercial vehicle operators and their employers are held to higher standards, and multiple parties may be liable including drivers, trucking companies, cargo loaders, and maintenance providers.",
    commonInjuries: ["Catastrophic injuries", "Wrongful death", "Crush injuries", "Burns", "Traumatic amputations", "Severe internal injuries"],
    uniqueFactors: ["Multiple liable parties", "Federal trucking regulations apply", "Higher insurance coverage available", "Electronic logging device evidence", "Cargo and maintenance liability"],
    averageSettlement: "$150,000 - $2,000,000+",
    proofRequired: ["Trucking company records", "Driver logs and qualifications", "Maintenance records", "Black box data", "FMCSA compliance records", "Expert testimony"],
    icon: "🚛"
  }
];

// Helper functions
export function getCaseTypeBySlug(slug: string): CaseTypeData | undefined {
  return caseTypes.find(ct => ct.slug === slug);
}

export function getAllCaseTypeSlugs(): string[] {
  return caseTypes.map(ct => ct.slug);
}
