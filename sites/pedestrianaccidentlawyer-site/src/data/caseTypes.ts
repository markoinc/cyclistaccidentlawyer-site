// Case types data for pedestrian accident law pages

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
    name: "Crosswalk Accidents",
    slug: "crosswalk-accidents",
    shortDescription: "Pedestrians struck while legally crossing at marked or unmarked crosswalks.",
    fullDescription: "Crosswalk accidents occur when vehicles fail to yield to pedestrians who have the legal right-of-way. In most states, every intersection is considered a crosswalk, whether marked or not. Drivers have a legal duty to stop for pedestrians in crosswalks, and failure to do so is negligence. These cases often have clear liability since the pedestrian was crossing legally.",
    commonInjuries: ["Traumatic brain injury", "Spinal cord damage", "Broken legs and pelvis", "Internal bleeding", "Road rash", "Wrongful death"],
    uniqueFactors: ["Clear right-of-way establishes liability", "Traffic cameras often capture accidents", "Witness availability at intersections", "Driver distraction common cause", "Speed at intersection affects severity"],
    averageSettlement: "$100,000 - $500,000+",
    proofRequired: ["Police report", "Traffic camera footage", "Witness statements", "Crosswalk documentation", "Signal timing records"],
    icon: "🚶"
  },
  {
    name: "Hit-and-Run Accidents",
    slug: "hit-and-run",
    shortDescription: "Pedestrians struck by drivers who fled the scene without stopping.",
    fullDescription: "Hit-and-run pedestrian accidents are devastating because victims may not know who hit them, complicating the claims process. These accidents often occur at night or in areas with few witnesses. Even if the driver is never found, victims may recover compensation through their own uninsured motorist coverage or crime victim compensation funds. Law enforcement investigation and surveillance footage are crucial.",
    commonInjuries: ["Severe trauma from impact", "Delayed medical treatment injuries", "Traumatic brain injury", "Spinal injuries", "Compound fractures", "Psychological trauma"],
    uniqueFactors: ["Driver may never be found", "Uninsured motorist coverage essential", "Police investigation critical", "Surveillance footage key evidence", "Crime victim compensation available", "Criminal charges if driver found"],
    averageSettlement: "$50,000 - $300,000+ (varies by UM coverage)",
    proofRequired: ["Police hit-and-run report", "Surveillance footage", "Witness descriptions", "Vehicle debris analysis", "UM policy documentation"],
    icon: "🚗💨"
  },
  {
    name: "Intersection Accidents",
    slug: "intersection-accidents",
    shortDescription: "Pedestrians struck at intersections while crossing with or without signals.",
    fullDescription: "Intersection accidents account for the majority of pedestrian crashes. These occur when drivers run red lights, fail to yield on right turns, or ignore pedestrians in crosswalks. Signal timing, driver distraction, and failure to check for pedestrians before turning are common causes. Modern traffic cameras at intersections often capture these accidents, providing crucial evidence.",
    commonInjuries: ["Leg and hip fractures", "Head trauma", "Spinal injuries", "Internal organ damage", "Compound fractures", "Facial injuries"],
    uniqueFactors: ["Right-turn-on-red accidents common", "Signal timing affects liability", "Multiple witnesses often present", "Traffic cameras capture events", "Driver visibility issues may be defense"],
    averageSettlement: "$75,000 - $400,000+",
    proofRequired: ["Traffic signal records", "Red light camera footage", "Witness statements", "Police accident report", "Intersection design analysis"],
    icon: "🚦"
  },
  {
    name: "Parking Lot Accidents",
    slug: "parking-lot-accidents",
    shortDescription: "Pedestrians struck in shopping center, store, or commercial parking lots.",
    fullDescription: "Parking lot pedestrian accidents occur in shopping centers, grocery stores, malls, and commercial areas where pedestrians and vehicles mix closely. Drivers backing out of spaces, speeding through lots, and distracted driving are common causes. Property owners may share liability if the lot design is unsafe or lacks proper pedestrian paths and crossings.",
    commonInjuries: ["Leg and ankle injuries", "Back injuries", "Head trauma", "Hip fractures", "Soft tissue injuries", "Emotional trauma"],
    uniqueFactors: ["Property owner may share liability", "Lot design affects safety", "Lower speeds but less visibility", "Backing vehicles common cause", "Surveillance cameras often present"],
    averageSettlement: "$25,000 - $200,000+",
    proofRequired: ["Parking lot surveillance video", "Property owner records", "Lot design documentation", "Witness statements", "Prior incident history"],
    icon: "🅿️"
  },
  {
    name: "Sidewalk Accidents",
    slug: "sidewalk-accidents",
    shortDescription: "Pedestrians struck on sidewalks by vehicles leaving the roadway.",
    fullDescription: "Sidewalk accidents occur when vehicles jump the curb and strike pedestrians who are walking safely on the sidewalk. These accidents often result from DUI, distracted driving, medical emergencies, or loss of vehicle control. Liability is typically clear since pedestrians on sidewalks have every expectation of safety from vehicle traffic.",
    commonInjuries: ["Catastrophic injuries", "Traumatic brain injury", "Spinal cord damage", "Crush injuries", "Multiple fractures", "Wrongful death"],
    uniqueFactors: ["Clear liability - pedestrian on sidewalk", "Often involves DUI or distraction", "May involve building or barrier strikes", "Multiple victims possible", "High severity due to surprise"],
    averageSettlement: "$150,000 - $1,000,000+",
    proofRequired: ["Police report", "Driver toxicology results", "Witness statements", "Vehicle damage analysis", "Road and sidewalk conditions"],
    icon: "🛤️"
  },
  {
    name: "School Zone Accidents",
    slug: "school-zone-accidents",
    shortDescription: "Children and adults struck in school zones during school hours.",
    fullDescription: "School zone accidents involve special circumstances due to reduced speed limits, crossing guards, and the vulnerability of child victims. Drivers must exercise extreme caution in school zones, and penalties for violations are enhanced. Schools and municipalities may share liability if crossings, signage, or crossing guard programs are inadequate.",
    commonInjuries: ["Child-specific trauma patterns", "Traumatic brain injury", "Growth plate injuries", "Psychological trauma", "Long-term developmental impacts", "Wrongful death"],
    uniqueFactors: ["Enhanced driver duties in school zones", "Child victim considerations", "School/municipality potential liability", "Crossing guard testimony", "Special damages for child victims"],
    averageSettlement: "$100,000 - $750,000+",
    proofRequired: ["School zone signage documentation", "Speed limit verification", "Crossing guard statements", "School policies", "Child medical/psychological records"],
    icon: "🏫"
  },
  {
    name: "Driveway Accidents",
    slug: "driveway-accidents",
    shortDescription: "Pedestrians struck by vehicles entering or exiting driveways.",
    fullDescription: "Driveway accidents often involve vehicles backing out and striking pedestrians on sidewalks or in streets. Children and elderly pedestrians are particularly vulnerable. Drivers have a duty to ensure the path is clear before backing, and many modern vehicles have backup cameras specifically to prevent these accidents.",
    commonInjuries: ["Leg and hip injuries", "Head trauma", "Back injuries", "Child injuries", "Crush injuries", "Psychological trauma"],
    uniqueFactors: ["Backup camera requirements on newer vehicles", "Residential vs commercial driveways", "Child victims common", "Homeowner insurance may apply", "Visibility obstructions"],
    averageSettlement: "$50,000 - $300,000+",
    proofRequired: ["Vehicle backup system records", "Witness statements", "Property owner information", "Driveway sight line analysis", "Medical records"],
    icon: "🏠"
  },
  {
    name: "Bus Stop Accidents",
    slug: "bus-stop-accidents",
    shortDescription: "Pedestrians struck while waiting at or approaching bus stops.",
    fullDescription: "Bus stop accidents involve pedestrians struck while waiting for public transit, crossing to reach stops, or being struck by the bus itself. Transit authorities may share liability for unsafe stop placement or bus driver negligence. These accidents often occur during rush hours when pedestrians are hurrying to catch buses.",
    commonInjuries: ["Multiple trauma from bus collisions", "Crowd crush injuries", "Head trauma", "Leg and hip fractures", "Internal injuries", "Wrongful death"],
    uniqueFactors: ["Transit authority potential liability", "Bus driver training records", "Stop placement safety analysis", "Rush hour timing", "Multiple victim scenarios"],
    averageSettlement: "$75,000 - $500,000+",
    proofRequired: ["Transit authority records", "Bus driver logs", "Stop safety assessment", "Witness statements", "Bus camera footage"],
    icon: "🚌"
  },
  {
    name: "Distracted Driver Accidents",
    slug: "distracted-driver",
    shortDescription: "Pedestrians struck by drivers using phones, eating, or otherwise distracted.",
    fullDescription: "Distracted driving is one of the leading causes of pedestrian accidents. Drivers using cell phones, texting, eating, or engaged with infotainment systems fail to see pedestrians. Cell phone records can prove distraction, and these cases may support punitive damages due to the driver's conscious disregard for safety.",
    commonInjuries: ["Severe impact trauma", "Traumatic brain injury", "Spinal injuries", "Multiple fractures", "Internal bleeding", "Wrongful death"],
    uniqueFactors: ["Cell phone records as evidence", "No evasive action taken by driver", "Punitive damages possible", "Employer liability if work-related", "Insurance policy stacking"],
    averageSettlement: "$100,000 - $750,000+",
    proofRequired: ["Cell phone records subpoena", "Police investigation of distraction", "Witness statements", "Accident reconstruction", "Driver admission if any"],
    icon: "📱"
  },
  {
    name: "Drunk Driver Accidents",
    slug: "drunk-driver",
    shortDescription: "Pedestrians struck by drivers under the influence of alcohol or drugs.",
    fullDescription: "DUI pedestrian accidents often result in severe injuries or death because impaired drivers cannot react appropriately. Criminal charges against the driver can support civil claims. Punitive damages are commonly awarded, and dram shop liability may apply against bars or restaurants that over-served the driver.",
    commonInjuries: ["Catastrophic injuries", "Traumatic brain injury", "Spinal cord damage", "Internal organ damage", "Multiple fractures", "Wrongful death"],
    uniqueFactors: ["Punitive damages typically awarded", "Criminal case provides evidence", "Dram shop liability possible", "Higher insurance limits often available", "Clear liability established"],
    averageSettlement: "$150,000 - $2,000,000+",
    proofRequired: ["Police DUI report", "Blood alcohol test results", "Criminal court records", "Bar/restaurant records if applicable", "Toxicology expert testimony"],
    icon: "🍺"
  },
  {
    name: "Commercial Vehicle Accidents",
    slug: "commercial-vehicle",
    shortDescription: "Pedestrians struck by trucks, delivery vehicles, or commercial vehicles.",
    fullDescription: "Pedestrians struck by commercial vehicles—semi-trucks, delivery vans, buses—face catastrophic injuries due to vehicle size. Multiple parties may be liable including drivers, companies, and cargo loaders. Federal trucking regulations may apply, and commercial vehicles typically have higher insurance coverage limits.",
    commonInjuries: ["Catastrophic crush injuries", "Traumatic brain injury", "Spinal cord damage", "Traumatic amputations", "Internal organ failure", "Wrongful death"],
    uniqueFactors: ["Multiple liable parties", "Federal trucking regulations", "Higher insurance limits", "Electronic logging device evidence", "Company training records relevant"],
    averageSettlement: "$200,000 - $3,000,000+",
    proofRequired: ["Company safety records", "Driver qualification files", "Electronic logging data", "Maintenance records", "FMCSA compliance records"],
    icon: "🚛"
  },
  {
    name: "Construction Zone Accidents",
    slug: "construction-zone",
    shortDescription: "Pedestrians struck in work zones or areas with altered pedestrian paths.",
    fullDescription: "Construction zone pedestrian accidents occur when work sites force pedestrians into unsafe areas, inadequate barriers fail to protect walkways, or construction vehicles strike pedestrians. Construction companies, property owners, and general contractors may share liability for failing to maintain safe pedestrian routes.",
    commonInjuries: ["Construction equipment trauma", "Trip and fall injuries", "Vehicle strike injuries", "Multiple fractures", "Head trauma", "Wrongful death"],
    uniqueFactors: ["Multiple contractors potentially liable", "OSHA violations may establish negligence", "Work zone design evidence", "Temporary signage adequacy", "Pedestrian detour safety"],
    averageSettlement: "$75,000 - $500,000+",
    proofRequired: ["Work zone permits", "Safety plans", "OSHA records", "Contractor agreements", "Site safety inspection records"],
    icon: "🚧"
  },
  {
    name: "Rideshare Accidents",
    slug: "rideshare-accidents",
    shortDescription: "Pedestrians struck by Uber, Lyft, or other rideshare vehicles.",
    fullDescription: "Rideshare pedestrian accidents involve Uber, Lyft, and similar services. These cases can be complex because driver insurance coverage depends on whether the app was on, a ride was accepted, or a passenger was present. Rideshare companies have substantial insurance policies for serious accidents.",
    commonInjuries: ["Severe impact trauma", "Head injuries", "Leg and hip fractures", "Internal injuries", "Spinal damage", "Wrongful death"],
    uniqueFactors: ["Insurance coverage depends on app status", "Rideshare company insurance available", "Driver employment status issues", "App data can establish liability", "Multiple insurance policies may apply"],
    averageSettlement: "$75,000 - $500,000+",
    proofRequired: ["Rideshare app status at time of accident", "Driver insurance information", "Company insurance policy", "Trip data if available", "Police report"],
    icon: "🚕"
  },
  {
    name: "Elderly Pedestrian Accidents",
    slug: "elderly-pedestrian",
    shortDescription: "Seniors struck while walking, often facing unique challenges and injuries.",
    fullDescription: "Elderly pedestrians face unique dangers due to slower walking speeds, reduced mobility, and age-related vulnerabilities. Injuries are often more severe due to fragile bones and pre-existing conditions. Signal timing that doesn't account for slower crossing speeds may contribute to liability.",
    commonInjuries: ["Hip fractures", "Head trauma", "Spinal injuries", "Internal bleeding", "Complications from pre-existing conditions", "Wrongful death"],
    uniqueFactors: ["Age-related vulnerabilities", "Pre-existing conditions complicate damages", "Signal timing may be inadequate", "Assisted living facility liability possible", "Life expectancy calculations affect damages"],
    averageSettlement: "$75,000 - $500,000+",
    proofRequired: ["Medical history", "Signal timing analysis", "Crossing speed studies", "Witness statements", "Life care planning if needed"],
    icon: "👴"
  },
  {
    name: "Child Pedestrian Accidents",
    slug: "child-pedestrian",
    shortDescription: "Children struck while walking, playing, or crossing streets.",
    fullDescription: "Child pedestrian accidents are particularly tragic and involve special legal considerations. Drivers have heightened duties around children, who are less predictable and may dart into streets. Damages include long-term effects on development, education, and future earning capacity.",
    commonInjuries: ["Growth plate injuries", "Traumatic brain injury", "Long-term developmental impacts", "Psychological trauma", "Facial injuries", "Wrongful death"],
    uniqueFactors: ["Drivers must anticipate child behavior", "Statutory protections for children", "Parental claims for emotional distress", "Future earnings calculations complex", "Educational impact damages"],
    averageSettlement: "$100,000 - $1,000,000+",
    proofRequired: ["Pediatric medical specialists", "Child development experts", "Educational impact assessment", "Future care planning", "Family impact documentation"],
    icon: "👶"
  }
];

// Helper functions
export function getCaseTypeBySlug(slug: string): CaseTypeData | undefined {
  return caseTypes.find(ct => ct.slug === slug);
}

export function getAllCaseTypeSlugs(): string[] {
  return caseTypes.map(ct => ct.slug);
}
