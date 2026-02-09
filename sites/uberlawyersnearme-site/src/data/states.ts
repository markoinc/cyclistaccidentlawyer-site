// State data for rideshare accident law pages
export interface StateData {
  name: string;
  slug: string;
  abbreviation: string;
  capital: string;
  majorCities: string[];
  statuteOfLimitations: string;
  faultSystem: string;
  minAutoInsurance: string;
  rideshareRegulations: string;
  tncInsuranceRequirements: string;
  uberCoverage: {
    offline: string;
    appOnWaiting: string;
    enRouteAndTrip: string;
  };
  lyftCoverage: {
    offline: string;
    appOnWaiting: string;
    enRouteAndTrip: string;
  };
  uniqueRideshareFactors: string[];
  majorAirports: string[];
  rideshareAccidentHotspots: string[];
  annualRideshareTrips: string;
  averageSettlement: string;
}

export const states: StateData[] = [
  {
    name: "Alabama",
    slug: "alabama",
    abbreviation: "AL",
    capital: "Montgomery",
    majorCities: ["Birmingham", "Huntsville", "Mobile", "Montgomery"],
    statuteOfLimitations: "2 years",
    faultSystem: "Contributory negligence (pure)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation passed 2018. Requires commercial insurance and background checks for drivers.",
    tncInsuranceRequirements: "Must maintain $1M liability during trips. Period 1 requires state minimums or TNC coverage.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Contributory negligence can bar ANY recovery if you're 1% at fault", "Growing rideshare market in Birmingham", "Limited public transit increases rideshare demand", "College towns drive weekend rideshare usage"],
    majorAirports: ["Birmingham-Shuttlesworth (BHM)", "Huntsville International (HSV)"],
    rideshareAccidentHotspots: ["I-65 corridor", "Birmingham downtown entertainment district", "US-280 corridor", "UAB campus area"],
    annualRideshareTrips: "8+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Alaska",
    slug: "alaska",
    abbreviation: "AK",
    capital: "Juneau",
    majorCities: ["Anchorage", "Fairbanks", "Juneau", "Sitka"],
    statuteOfLimitations: "2 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$50,000/$100,000/$25,000",
    rideshareRegulations: "TNC regulations adopted. Limited rideshare availability due to population density.",
    tncInsuranceRequirements: "Standard TNC insurance requirements apply. Higher state minimum requirements than most states.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Limited rideshare availability in remote areas", "Extreme weather conditions affect driving safety", "Tourism drives seasonal rideshare demand", "Higher insurance minimums than other states"],
    majorAirports: ["Ted Stevens Anchorage (ANC)", "Fairbanks International (FAI)"],
    rideshareAccidentHotspots: ["Anchorage downtown", "Airport routes", "Seward Highway", "Northern Lights Boulevard"],
    annualRideshareTrips: "2+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Arizona",
    slug: "arizona",
    abbreviation: "AZ",
    capital: "Phoenix",
    majorCities: ["Phoenix", "Tucson", "Mesa", "Scottsdale", "Chandler", "Tempe"],
    statuteOfLimitations: "2 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$15,000",
    rideshareRegulations: "Comprehensive TNC legislation since 2015. First state to allow autonomous rideshare testing.",
    tncInsuranceRequirements: "Three-tiered insurance system. $1M coverage during active trips required.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Waymo autonomous rideshare operations in Phoenix", "Major rideshare market - Phoenix #5 nationally", "Extreme heat affects driver fatigue", "Spring training and events create surge periods", "Phoenix Sky Harbor major airport hub"],
    majorAirports: ["Phoenix Sky Harbor (PHX)", "Tucson International (TUS)", "Phoenix-Mesa Gateway (AZA)"],
    rideshareAccidentHotspots: ["Sky Harbor airport routes", "Scottsdale entertainment district", "ASU Tempe campus", "I-10 corridor", "Mill Avenue"],
    annualRideshareTrips: "75+ million",
    averageSettlement: "$55,000 - $500,000"
  },
  {
    name: "Arkansas",
    slug: "arkansas",
    abbreviation: "AR",
    capital: "Little Rock",
    majorCities: ["Little Rock", "Fort Smith", "Fayetteville", "Springdale", "Bentonville"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (49%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation enacted 2015. State preempts local rideshare regulations.",
    tncInsuranceRequirements: "Standard three-tiered insurance. Contingent coverage during Period 1.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Walmart headquarters drives NW Arkansas rideshare demand", "University of Arkansas events create surge", "Growing tech sector in Bentonville", "Limited public transit increases rideshare reliance"],
    majorAirports: ["Bill and Hillary Clinton National (LIT)", "Northwest Arkansas Regional (XNA)"],
    rideshareAccidentHotspots: ["River Market District Little Rock", "Dickson Street Fayetteville", "Walmart campus area", "I-40 corridor"],
    annualRideshareTrips: "6+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "California",
    slug: "california",
    abbreviation: "CA",
    capital: "Sacramento",
    majorCities: ["Los Angeles", "San Francisco", "San Diego", "San Jose", "Oakland", "Sacramento"],
    statuteOfLimitations: "2 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$15,000/$30,000/$5,000",
    rideshareRegulations: "Most comprehensive TNC regulations nationally. CPUC oversight. AB5 gig worker law (Prop 22 exempts rideshare).",
    tncInsuranceRequirements: "Pioneered the three-period insurance model adopted nationwide. Strict commercial requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $30,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $30,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Uber and Lyft headquartered here", "Largest rideshare market in the US", "Prop 22 classifies drivers as independent contractors", "Autonomous vehicle testing active", "High volume of rideshare accident litigation"],
    majorAirports: ["LAX", "SFO", "SAN", "OAK", "SJC", "ONT", "BUR", "LGB", "SNA"],
    rideshareAccidentHotspots: ["LAX airport routes", "Hollywood & West Hollywood", "San Francisco Financial District", "Silicon Valley", "San Diego Gaslamp Quarter"],
    annualRideshareTrips: "500+ million",
    averageSettlement: "$75,000 - $750,000"
  },
  {
    name: "Colorado",
    slug: "colorado",
    abbreviation: "CO",
    capital: "Denver",
    majorCities: ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Boulder"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$15,000",
    rideshareRegulations: "Early TNC adopter. Comprehensive regulations since 2014. PUC oversight.",
    tncInsuranceRequirements: "Standard three-tier system. Strong consumer protections.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Heavy ski resort rideshare traffic", "DIA is major rideshare hub", "High altitude affects driver fatigue", "Marijuana tourism increases rideshare demand", "Severe weather conditions in mountains"],
    majorAirports: ["Denver International (DEN)", "Colorado Springs (COS)"],
    rideshareAccidentHotspots: ["DEN airport routes", "LoDo Denver entertainment district", "I-25 corridor", "I-70 mountain corridor", "Pearl Street Boulder"],
    annualRideshareTrips: "50+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "Connecticut",
    slug: "connecticut",
    abbreviation: "CT",
    capital: "Hartford",
    majorCities: ["Bridgeport", "New Haven", "Hartford", "Stamford", "Waterbury"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation enacted 2017. DMV oversight and licensing required.",
    tncInsuranceRequirements: "Follows standard TNC insurance model with state-specific requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["NYC commuter corridor increases rideshare use", "Yale University drives New Haven demand", "Casino destinations (Mohegan Sun, Foxwoods)", "Dense traffic in Gold Coast region"],
    majorAirports: ["Bradley International (BDL)", "Tweed New Haven (HVN)"],
    rideshareAccidentHotspots: ["I-95 corridor", "Hartford downtown", "New Haven around Yale", "Stamford transit hub", "Casino routes"],
    annualRideshareTrips: "20+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Delaware",
    slug: "delaware",
    abbreviation: "DE",
    capital: "Dover",
    majorCities: ["Wilmington", "Dover", "Newark", "Middletown"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$10,000",
    rideshareRegulations: "TNC regulations enacted. Required permits and insurance verification.",
    tncInsuranceRequirements: "Standard three-tier insurance system with Delaware-specific compliance.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Philadelphia metro rideshare extends into Delaware", "Beach tourism in Rehoboth drives seasonal demand", "Tax-free shopping attracts rideshare trips", "University of Delaware campus activity"],
    majorAirports: ["Wilmington Airport (ILG)", "Most use Philadelphia (PHL)"],
    rideshareAccidentHotspots: ["I-95 corridor", "Wilmington downtown", "Rehoboth Beach area", "UD campus area"],
    annualRideshareTrips: "5+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "District of Columbia",
    slug: "district-of-columbia",
    abbreviation: "DC",
    capital: "Washington",
    majorCities: ["Washington"],
    statuteOfLimitations: "3 years",
    faultSystem: "Contributory negligence (pure)",
    minAutoInsurance: "$25,000/$50,000/$10,000",
    rideshareRegulations: "Comprehensive TNC legislation. DC Taxicab Commission oversight. Strict licensing requirements.",
    tncInsuranceRequirements: "Enhanced insurance requirements. All TNCs must be licensed in DC.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["CONTRIBUTORY NEGLIGENCE - Any fault bars recovery", "Extremely high rideshare volume in small area", "Federal government commuters", "Tourist destination creates constant demand", "Multiple airports serve the area"],
    majorAirports: ["Reagan National (DCA)", "Dulles (IAD)", "BWI (nearby)"],
    rideshareAccidentHotspots: ["DCA airport routes", "Capitol Hill area", "Georgetown", "Dupont Circle", "Adams Morgan nightlife"],
    annualRideshareTrips: "40+ million",
    averageSettlement: "$60,000 - $500,000"
  },
  {
    name: "Florida",
    slug: "florida",
    abbreviation: "FL",
    capital: "Tallahassee",
    majorCities: ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale", "St. Petersburg"],
    statuteOfLimitations: "2 years",
    faultSystem: "Pure comparative fault (modified 2023)",
    minAutoInsurance: "$10,000 PIP, $10,000 PDL (no BI required)",
    rideshareRegulations: "Comprehensive TNC Act since 2017. State preempts local regulations. Required permits and insurance.",
    tncInsuranceRequirements: "Strong TNC insurance requirements. Higher than state minimums during all periods.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["#2 rideshare market nationally", "Massive tourism drives demand", "No-fault PIP system complicates claims", "Multiple major airports", "2023 tort reform changed comparative fault to modified (51%)"],
    majorAirports: ["Miami (MIA)", "Orlando (MCO)", "Fort Lauderdale (FLL)", "Tampa (TPA)", "Jacksonville (JAX)"],
    rideshareAccidentHotspots: ["South Beach Miami", "Disney/Universal area Orlando", "Tampa Ybor City", "Fort Lauderdale beach strip", "Airport routes statewide"],
    annualRideshareTrips: "200+ million",
    averageSettlement: "$50,000 - $500,000"
  },
  {
    name: "Georgia",
    slug: "georgia",
    abbreviation: "GA",
    capital: "Atlanta",
    majorCities: ["Atlanta", "Augusta", "Columbus", "Savannah", "Marietta"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC Act passed 2015. Georgia PSC oversight. Statewide regulations preempt local rules.",
    tncInsuranceRequirements: "Standard three-period model. Strong commercial insurance requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Atlanta is major rideshare hub - #6 nationally", "Hartsfield-Jackson busiest airport globally", "Heavy convention traffic", "Limited public transit increases rideshare reliance", "Major film industry creates production-related rideshare demand"],
    majorAirports: ["Hartsfield-Jackson Atlanta (ATL)", "Savannah/Hilton Head (SAV)"],
    rideshareAccidentHotspots: ["ATL airport routes", "Buckhead entertainment district", "Downtown Atlanta", "Midtown", "Georgia Dome/Mercedes-Benz Stadium area"],
    annualRideshareTrips: "100+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "Hawaii",
    slug: "hawaii",
    abbreviation: "HI",
    capital: "Honolulu",
    majorCities: ["Honolulu", "Pearl City", "Hilo", "Kailua"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$20,000/$40,000/$10,000 (PIP required)",
    rideshareRegulations: "TNC legislation enacted. PUC oversight. Island-specific considerations.",
    tncInsuranceRequirements: "Standard TNC insurance plus Hawaii's no-fault PIP requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Heavy tourism creates massive rideshare demand", "Island geography limits driving options", "Airport transfers are huge portion of rides", "PIP no-fault affects injury claims", "Multiple islands have separate rideshare markets"],
    majorAirports: ["Daniel K. Inouye/Honolulu (HNL)", "Maui (OGG)", "Kona (KOA)", "Lihue (LIH)"],
    rideshareAccidentHotspots: ["Waikiki Beach area", "HNL airport routes", "H-1 Freeway", "Kalakaua Avenue", "Resort corridors on all islands"],
    annualRideshareTrips: "25+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Idaho",
    slug: "idaho",
    abbreviation: "ID",
    capital: "Boise",
    majorCities: ["Boise", "Meridian", "Nampa", "Idaho Falls", "Coeur d'Alene"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$15,000",
    rideshareRegulations: "TNC legislation enacted 2015. Basic state requirements.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Growing tech sector in Boise drives rideshare demand", "Sun Valley tourism creates seasonal surge", "Limited rideshare in rural areas", "BSU campus generates significant rideshare traffic"],
    majorAirports: ["Boise Airport (BOI)", "Idaho Falls Regional (IDA)"],
    rideshareAccidentHotspots: ["Downtown Boise", "BOI airport routes", "Eagle Road corridor", "BSU campus area"],
    annualRideshareTrips: "5+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Illinois",
    slug: "illinois",
    abbreviation: "IL",
    capital: "Springfield",
    majorCities: ["Chicago", "Aurora", "Naperville", "Rockford", "Springfield"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$20,000",
    rideshareRegulations: "Comprehensive TNC regulations. Chicago has additional local requirements. ICC oversight.",
    tncInsuranceRequirements: "Enhanced requirements in Chicago. Standard model statewide.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Chicago is #3 rideshare market nationally", "Two major airports create massive rideshare demand", "Heavy convention traffic at McCormick Place", "Extreme winter weather affects driving safety", "Dense urban traffic patterns"],
    majorAirports: ["O'Hare (ORD)", "Midway (MDW)"],
    rideshareAccidentHotspots: ["O'Hare airport routes", "Magnificent Mile", "Wrigleyville", "Loop area", "Navy Pier vicinity"],
    annualRideshareTrips: "125+ million",
    averageSettlement: "$60,000 - $500,000"
  },
  {
    name: "Indiana",
    slug: "indiana",
    abbreviation: "IN",
    capital: "Indianapolis",
    majorCities: ["Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Carmel"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. State preemption of local rideshare laws.",
    tncInsuranceRequirements: "Standard three-period model. IURC oversight.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Indianapolis 500 creates massive surge demand", "Convention center drives rideshare traffic", "Notre Dame games increase South Bend rideshare", "Growing tech hub status"],
    majorAirports: ["Indianapolis (IND)", "Fort Wayne (FWA)"],
    rideshareAccidentHotspots: ["IND airport routes", "Downtown Indianapolis", "Broad Ripple", "IU campus Bloomington", "Notre Dame area"],
    annualRideshareTrips: "20+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Iowa",
    slug: "iowa",
    abbreviation: "IA",
    capital: "Des Moines",
    majorCities: ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$20,000/$40,000/$15,000",
    rideshareRegulations: "TNC legislation 2016. DOT oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["University of Iowa drives Iowa City demand", "State fair creates seasonal surge", "Insurance industry hub in Des Moines", "Winter weather affects driving safety"],
    majorAirports: ["Des Moines (DSM)", "Cedar Rapids (CID)"],
    rideshareAccidentHotspots: ["DSM airport", "Downtown Des Moines", "Iowa City downtown", "Ped Mall area"],
    annualRideshareTrips: "8+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Kansas",
    slug: "kansas",
    abbreviation: "KS",
    capital: "Topeka",
    majorCities: ["Wichita", "Overland Park", "Kansas City", "Olathe", "Topeka"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. KCC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["KC metro area (shared with Missouri) is main market", "KU and K-State games drive rideshare demand", "Limited rideshare in rural areas", "Aviation industry in Wichita"],
    majorAirports: ["Wichita Eisenhower (ICT)", "Kansas City (MCI - technically Missouri but serves Kansas)"],
    rideshareAccidentHotspots: ["Power and Light District KC", "Wichita downtown", "Lawrence downtown", "KU campus area"],
    annualRideshareTrips: "10+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Kentucky",
    slug: "kentucky",
    abbreviation: "KY",
    capital: "Frankfort",
    majorCities: ["Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington"],
    statuteOfLimitations: "1 year",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$25,000 (PIP required)",
    rideshareRegulations: "TNC legislation 2015. Choice no-fault state.",
    tncInsuranceRequirements: "Standard model plus Kentucky's no-fault PIP requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["ONLY 1 YEAR to file lawsuit - shortest in nation", "Kentucky Derby creates massive rideshare surge", "Bourbon tourism drives rideshare demand", "UK basketball generates Lexington traffic"],
    majorAirports: ["Louisville (SDF)", "Cincinnati/Northern Kentucky (CVG)"],
    rideshareAccidentHotspots: ["Fourth Street Live Louisville", "Churchill Downs area", "Downtown Lexington", "UK campus", "Bourbon Trail routes"],
    annualRideshareTrips: "15+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Louisiana",
    slug: "louisiana",
    abbreviation: "LA",
    capital: "Baton Rouge",
    majorCities: ["New Orleans", "Baton Rouge", "Shreveport", "Lafayette", "Lake Charles"],
    statuteOfLimitations: "1 year",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$15,000/$30,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. LPSC oversight.",
    tncInsuranceRequirements: "Standard three-period model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["ONLY 1 YEAR statute of limitations", "Mardi Gras/festivals create extreme surge demand", "French Quarter pedestrian/rideshare conflicts", "Heavy tourism in New Orleans", "Flood zones affect driving conditions"],
    majorAirports: ["New Orleans (MSY)", "Baton Rouge (BTR)"],
    rideshareAccidentHotspots: ["French Quarter", "Bourbon Street vicinity", "MSY airport routes", "Magazine Street", "CBD New Orleans"],
    annualRideshareTrips: "25+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Maine",
    slug: "maine",
    abbreviation: "ME",
    capital: "Augusta",
    majorCities: ["Portland", "Lewiston", "Bangor", "South Portland", "Auburn"],
    statuteOfLimitations: "6 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$50,000/$100,000/$25,000",
    rideshareRegulations: "TNC legislation enacted. PUC oversight.",
    tncInsuranceRequirements: "Standard model. Higher state minimums than many states.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["6-year statute of limitations - longest in nation", "Tourism creates summer surge in Portland", "Limited rideshare in rural areas", "Winter weather affects driving safety"],
    majorAirports: ["Portland (PWM)", "Bangor (BGR)"],
    rideshareAccidentHotspots: ["Old Port Portland", "PWM airport routes", "Bar Harbor seasonal", "Bangor downtown"],
    annualRideshareTrips: "5+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Maryland",
    slug: "maryland",
    abbreviation: "MD",
    capital: "Annapolis",
    majorCities: ["Baltimore", "Columbia", "Germantown", "Silver Spring", "Waldorf"],
    statuteOfLimitations: "3 years",
    faultSystem: "Contributory negligence (pure)",
    minAutoInsurance: "$30,000/$60,000/$15,000",
    rideshareRegulations: "Comprehensive TNC legislation. PSC oversight. Additional Baltimore regulations.",
    tncInsuranceRequirements: "Standard three-period model with Maryland-specific requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["CONTRIBUTORY NEGLIGENCE - Any fault bars recovery", "DC metro area extends into Maryland", "BWI Airport is major rideshare hub", "Heavy commuter rideshare traffic", "Ravens/Orioles games create surge"],
    majorAirports: ["Baltimore-Washington (BWI)", "Also serves DCA/IAD"],
    rideshareAccidentHotspots: ["BWI airport routes", "Inner Harbor Baltimore", "Fells Point", "I-95/I-495 corridor", "Bethesda/Silver Spring area"],
    annualRideshareTrips: "40+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "Massachusetts",
    slug: "massachusetts",
    abbreviation: "MA",
    capital: "Boston",
    majorCities: ["Boston", "Worcester", "Springfield", "Cambridge", "Lowell"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$20,000/$40,000/$5,000 (PIP required)",
    rideshareRegulations: "Comprehensive TNC law 2016. DPU oversight. Per-ride assessment fund.",
    tncInsuranceRequirements: "Standard model plus state's no-fault PIP requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Major rideshare market - #7 nationally", "Dense college population drives demand", "Confusing road layout increases accident risk", "Per-ride fee funds transportation improvements", "Logan Airport is major rideshare hub"],
    majorAirports: ["Boston Logan (BOS)", "Worcester Regional (ORH)"],
    rideshareAccidentHotspots: ["Logan Airport routes", "Fenway area", "Harvard/MIT areas", "Seaport District", "Back Bay"],
    annualRideshareTrips: "60+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "Michigan",
    slug: "michigan",
    abbreviation: "MI",
    capital: "Lansing",
    majorCities: ["Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%) - No-fault for auto",
    minAutoInsurance: "$50,000/$100,000 (Unlimited PIP optional, $250k min)",
    rideshareRegulations: "TNC legislation 2016. LARA oversight.",
    tncInsuranceRequirements: "Complex due to Michigan's no-fault system. Highest PIP in nation.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Complex no-fault insurance system", "Detroit is #10 rideshare market", "Auto industry hub creates unique traffic patterns", "University of Michigan generates Ann Arbor demand", "Winter weather severely affects driving"],
    majorAirports: ["Detroit Metro (DTW)", "Grand Rapids (GRR)", "Flint (FNT)"],
    rideshareAccidentHotspots: ["DTW airport routes", "Downtown Detroit", "Greektown/entertainment district", "Ann Arbor downtown", "Big House events"],
    annualRideshareTrips: "50+ million",
    averageSettlement: "$60,000 - $500,000"
  },
  {
    name: "Minnesota",
    slug: "minnesota",
    abbreviation: "MN",
    capital: "St. Paul",
    majorCities: ["Minneapolis", "St. Paul", "Rochester", "Duluth", "Bloomington"],
    statuteOfLimitations: "6 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$30,000/$60,000/$10,000 (PIP required)",
    rideshareRegulations: "TNC legislation 2015. State preempts local regulations.",
    tncInsuranceRequirements: "Standard model plus Minnesota's no-fault PIP requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["6-year statute of limitations", "MSP Airport is major hub", "Mall of America generates significant traffic", "Extreme winter weather", "Strong no-fault PIP benefits"],
    majorAirports: ["Minneapolis-St. Paul (MSP)", "Rochester (RST)"],
    rideshareAccidentHotspots: ["MSP airport routes", "Downtown Minneapolis", "Mall of America", "Nicollet Mall", "Northeast Minneapolis"],
    annualRideshareTrips: "30+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Mississippi",
    slug: "mississippi",
    abbreviation: "MS",
    capital: "Jackson",
    majorCities: ["Jackson", "Gulfport", "Southaven", "Biloxi", "Hattiesburg"],
    statuteOfLimitations: "3 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2016. PSC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Gulf Coast casinos drive rideshare demand", "Limited rideshare in rural areas", "Ole Miss/MSU games create surge", "Lower rideshare penetration than other states"],
    majorAirports: ["Jackson-Medgar Wiley Evers (JAN)", "Gulfport-Biloxi (GPT)"],
    rideshareAccidentHotspots: ["Biloxi casino strip", "Jackson downtown", "Oxford Square area", "Gulfport beach routes"],
    annualRideshareTrips: "5+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Missouri",
    slug: "missouri",
    abbreviation: "MO",
    capital: "Jefferson City",
    majorCities: ["Kansas City", "St. Louis", "Springfield", "Columbia", "Independence"],
    statuteOfLimitations: "5 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2017. State preempts local regulations.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["5-year statute of limitations", "Two major metro areas (KC and STL)", "Cardinals/Chiefs/Royals games drive demand", "MU campus creates Columbia demand", "Gateway Arch tourism"],
    majorAirports: ["St. Louis Lambert (STL)", "Kansas City (MCI)"],
    rideshareAccidentHotspots: ["Power and Light KC", "Downtown St. Louis", "Ballpark Village area", "Soulard neighborhood", "Columbia downtown"],
    annualRideshareTrips: "30+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Montana",
    slug: "montana",
    abbreviation: "MT",
    capital: "Helena",
    majorCities: ["Billings", "Missoula", "Great Falls", "Bozeman", "Helena"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$20,000",
    rideshareRegulations: "TNC legislation 2015. PSC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Very limited rideshare availability outside major cities", "Ski resort tourism drives seasonal demand", "Yellowstone/Glacier tourism", "Long driving distances", "Wildlife collision risk"],
    majorAirports: ["Billings (BIL)", "Bozeman (BZN)", "Missoula (MSO)"],
    rideshareAccidentHotspots: ["Downtown Bozeman", "Big Sky routes", "Missoula downtown", "Airport routes"],
    annualRideshareTrips: "2+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Nebraska",
    slug: "nebraska",
    abbreviation: "NE",
    capital: "Lincoln",
    majorCities: ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney"],
    statuteOfLimitations: "4 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. PSC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Nebraska football creates Lincoln surge", "College World Series drives Omaha demand", "Limited rideshare outside metro areas", "Warren Buffett annual meeting creates surge"],
    majorAirports: ["Omaha Eppley (OMA)", "Lincoln (LNK)"],
    rideshareAccidentHotspots: ["Old Market Omaha", "Haymarket Lincoln", "Memorial Stadium area", "TD Ameritrade Park vicinity"],
    annualRideshareTrips: "8+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Nevada",
    slug: "nevada",
    abbreviation: "NV",
    capital: "Carson City",
    majorCities: ["Las Vegas", "Henderson", "Reno", "North Las Vegas", "Sparks"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$20,000",
    rideshareRegulations: "Comprehensive TNC legislation 2015. Nevada TU Authority oversight.",
    tncInsuranceRequirements: "Standard three-period model. Enhanced airport requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Las Vegas is #4 rideshare market nationally", "24/7 Strip activity creates constant demand", "Massive convention traffic", "Alcohol-related rides extremely common", "Airport to Strip route is one of busiest in nation"],
    majorAirports: ["Harry Reid International/Las Vegas (LAS)", "Reno-Tahoe (RNO)"],
    rideshareAccidentHotspots: ["Las Vegas Strip", "LAS airport routes", "Fremont Street area", "Convention center routes", "Pool party venues"],
    annualRideshareTrips: "100+ million",
    averageSettlement: "$55,000 - $500,000"
  },
  {
    name: "New Hampshire",
    slug: "new-hampshire",
    abbreviation: "NH",
    capital: "Concord",
    majorCities: ["Manchester", "Nashua", "Concord", "Dover", "Rochester"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "No mandatory insurance (financial responsibility required)",
    rideshareRegulations: "TNC legislation 2016. PUC oversight.",
    tncInsuranceRequirements: "Standard model - TNCs provide insurance since state doesn't mandate it.",
    uberCoverage: {
      offline: "Driver's personal insurance only (if any)",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only (if any)",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Only state without mandatory auto insurance", "Boston commuter demand extends here", "Ski resort tourism creates seasonal surge", "Tax-free shopping attracts cross-border traffic"],
    majorAirports: ["Manchester-Boston Regional (MHT)"],
    rideshareAccidentHotspots: ["Downtown Manchester", "Nashua commercial areas", "MHT airport routes", "Ski resort routes"],
    annualRideshareTrips: "5+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "New Jersey",
    slug: "new-jersey",
    abbreviation: "NJ",
    capital: "Trenton",
    majorCities: ["Newark", "Jersey City", "Paterson", "Elizabeth", "Trenton"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (varies by policy)",
    minAutoInsurance: "$15,000/$30,000/$5,000 (PIP required)",
    rideshareRegulations: "Comprehensive TNC legislation 2017. MVC oversight.",
    tncInsuranceRequirements: "Standard model plus NJ's complex no-fault requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["NYC metro extends here - massive rideshare market", "Newark Airport is major hub", "Complex no-fault/verbal threshold system", "Dense traffic patterns", "Shore points create summer surge"],
    majorAirports: ["Newark Liberty (EWR)", "Atlantic City (ACY)"],
    rideshareAccidentHotspots: ["EWR airport routes", "Hoboken/Jersey City", "Atlantic City casinos", "Route 1 corridor", "Shore points in summer"],
    annualRideshareTrips: "50+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "New Mexico",
    slug: "new-mexico",
    abbreviation: "NM",
    capital: "Santa Fe",
    majorCities: ["Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell"],
    statuteOfLimitations: "3 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$10,000",
    rideshareRegulations: "TNC legislation 2016. PRC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["High DWI rates increase rideshare demand", "Tourism in Santa Fe", "UNM campus creates Albuquerque demand", "Limited rideshare in rural areas"],
    majorAirports: ["Albuquerque (ABQ)", "Santa Fe (SAF)"],
    rideshareAccidentHotspots: ["Downtown Albuquerque", "Santa Fe Plaza area", "ABQ airport routes", "UNM campus area"],
    annualRideshareTrips: "8+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "New York",
    slug: "new-york",
    abbreviation: "NY",
    capital: "Albany",
    majorCities: ["New York City", "Buffalo", "Rochester", "Yonkers", "Syracuse"],
    statuteOfLimitations: "3 years",
    faultSystem: "Pure comparative fault (No-fault for auto)",
    minAutoInsurance: "$25,000/$50,000/$10,000 (PIP required)",
    rideshareRegulations: "Most comprehensive regulations. TLC oversight in NYC. State DMV elsewhere.",
    tncInsuranceRequirements: "Enhanced requirements. NYC has additional TLC licensing. Black car fund.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$75,000/$150,000 liability (NYC higher), $25,000 property",
      enRouteAndTrip: "$1,250,000+ liability in NYC, $1,000,000 elsewhere"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$75,000/$150,000 liability (NYC higher), $25,000 property",
      enRouteAndTrip: "$1,250,000+ liability in NYC, $1,000,000 elsewhere"
    },
    uniqueRideshareFactors: ["NYC is #1 rideshare market in the nation", "TLC licensing required in NYC", "Complex no-fault system", "Higher insurance requirements in NYC", "Congestion pricing coming"],
    majorAirports: ["JFK", "LaGuardia (LGA)", "Newark (EWR)", "Buffalo (BUF)"],
    rideshareAccidentHotspots: ["All of Manhattan", "Airport routes", "Brooklyn nightlife areas", "Times Square vicinity", "LGA/JFK pickup zones"],
    annualRideshareTrips: "300+ million",
    averageSettlement: "$75,000 - $750,000"
  },
  {
    name: "North Carolina",
    slug: "north-carolina",
    abbreviation: "NC",
    capital: "Raleigh",
    majorCities: ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem"],
    statuteOfLimitations: "3 years",
    faultSystem: "Contributory negligence (pure)",
    minAutoInsurance: "$30,000/$60,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. DMV oversight.",
    tncInsuranceRequirements: "Standard three-period model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["CONTRIBUTORY NEGLIGENCE - Any fault bars recovery", "Charlotte is major banking hub", "Research Triangle drives demand", "ACC/college sports create surge", "Growing tech industry"],
    majorAirports: ["Charlotte Douglas (CLT)", "Raleigh-Durham (RDU)"],
    rideshareAccidentHotspots: ["Uptown Charlotte", "CLT airport routes", "Durham downtown", "Chapel Hill/UNC area", "Bank of America Stadium vicinity"],
    annualRideshareTrips: "50+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "North Dakota",
    slug: "north-dakota",
    abbreviation: "ND",
    capital: "Bismarck",
    majorCities: ["Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo"],
    statuteOfLimitations: "6 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$25,000 (PIP required)",
    rideshareRegulations: "TNC legislation 2015. PSC oversight.",
    tncInsuranceRequirements: "Standard model plus North Dakota's no-fault requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["6-year statute of limitations", "Oil industry drives rideshare in western ND", "NDSU games create Fargo demand", "Extreme winter weather", "Limited rideshare in most areas"],
    majorAirports: ["Fargo (FAR)", "Bismarck (BIS)"],
    rideshareAccidentHotspots: ["Downtown Fargo", "NDSU area", "Bismarck downtown", "Oil field routes in west"],
    annualRideshareTrips: "2+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Ohio",
    slug: "ohio",
    abbreviation: "OH",
    capital: "Columbus",
    majorCities: ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. PUCO oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Three major metro areas with significant rideshare", "OSU games create massive Columbus surge", "Cleveland sports/Rock Hall traffic", "Cincinnati Ohio River events"],
    majorAirports: ["Cleveland Hopkins (CLE)", "John Glenn Columbus (CMH)", "Cincinnati (CVG - technically KY)"],
    rideshareAccidentHotspots: ["OSU campus area", "Short North Columbus", "Warehouse District Cleveland", "Over-the-Rhine Cincinnati", "Airport routes"],
    annualRideshareTrips: "45+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Oklahoma",
    slug: "oklahoma",
    abbreviation: "OK",
    capital: "Oklahoma City",
    majorCities: ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Edmond"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. Corporation Commission oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["OU and OSU games drive rideshare demand", "Oil industry creates business travel", "Tornado weather affects driving safety", "Growing entertainment districts"],
    majorAirports: ["Will Rogers World OKC (OKC)", "Tulsa (TUL)"],
    rideshareAccidentHotspots: ["Bricktown OKC", "Downtown Tulsa", "OU campus Norman", "Memorial Road corridor"],
    annualRideshareTrips: "15+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Oregon",
    slug: "oregon",
    abbreviation: "OR",
    capital: "Salem",
    majorCities: ["Portland", "Eugene", "Salem", "Gresham", "Hillsboro"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$20,000 (PIP required)",
    rideshareRegulations: "Comprehensive TNC regulations 2015. Transportation Commission oversight.",
    tncInsuranceRequirements: "Standard model plus Oregon's PIP requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Strong rideshare market in Portland", "Ducks/Beavers games drive Eugene demand", "Rainy weather affects driving safety", "No sales tax attracts cross-border trips", "Craft beer/wine tourism"],
    majorAirports: ["Portland (PDX)", "Eugene (EUG)"],
    rideshareAccidentHotspots: ["Downtown Portland", "Pearl District", "PDX airport routes", "Eugene downtown", "Hawthorne/Division Street"],
    annualRideshareTrips: "25+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Pennsylvania",
    slug: "pennsylvania",
    abbreviation: "PA",
    capital: "Harrisburg",
    majorCities: ["Philadelphia", "Pittsburgh", "Allentown", "Reading", "Erie"],
    statuteOfLimitations: "2 years",
    faultSystem: "Choice - Full tort or Limited tort",
    minAutoInsurance: "$15,000/$30,000/$5,000",
    rideshareRegulations: "Comprehensive TNC legislation 2016. PUC oversight.",
    tncInsuranceRequirements: "Standard model. Choice of tort options affects claims.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Philadelphia is #8 rideshare market", "Two major metro areas", "Choice tort system complicates claims", "Penn State weekends create surge", "Heavy tourism in Philadelphia"],
    majorAirports: ["Philadelphia (PHL)", "Pittsburgh (PIT)"],
    rideshareAccidentHotspots: ["Center City Philadelphia", "South Street area", "PHL airport routes", "Strip District Pittsburgh", "State College area"],
    annualRideshareTrips: "70+ million",
    averageSettlement: "$50,000 - $450,000"
  },
  {
    name: "Rhode Island",
    slug: "rhode-island",
    abbreviation: "RI",
    capital: "Providence",
    majorCities: ["Providence", "Warwick", "Cranston", "Pawtucket", "East Providence"],
    statuteOfLimitations: "3 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2016. DMV oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Smallest state - concentrated rideshare market", "College hill (Brown, RISD) drives demand", "Newport tourism creates summer surge", "Boston proximity affects rideshare patterns"],
    majorAirports: ["T.F. Green/Providence (PVD)"],
    rideshareAccidentHotspots: ["Downtown Providence", "PVD airport routes", "College Hill", "Federal Hill", "Newport in summer"],
    annualRideshareTrips: "8+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "South Carolina",
    slug: "south-carolina",
    abbreviation: "SC",
    capital: "Columbia",
    majorCities: ["Charleston", "Columbia", "North Charleston", "Mount Pleasant", "Greenville"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2015. PSC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Charleston tourism drives significant demand", "Myrtle Beach seasonal surge", "College towns (Clemson, USC) create demand", "Growing Greenville tech scene"],
    majorAirports: ["Charleston (CHS)", "Myrtle Beach (MYR)", "Greenville-Spartanburg (GSP)"],
    rideshareAccidentHotspots: ["Downtown Charleston", "King Street area", "Myrtle Beach strip", "Five Points Columbia", "Greenville downtown"],
    annualRideshareTrips: "20+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "South Dakota",
    slug: "south-dakota",
    abbreviation: "SD",
    capital: "Pierre",
    majorCities: ["Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (slight/gross)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2016. PUC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Sturgis Rally creates massive August surge", "Mount Rushmore tourism", "Limited rideshare outside Sioux Falls/Rapid City", "Extreme weather conditions"],
    majorAirports: ["Sioux Falls (FSD)", "Rapid City (RAP)"],
    rideshareAccidentHotspots: ["Downtown Sioux Falls", "Sturgis during rally", "Mount Rushmore routes", "Rapid City downtown"],
    annualRideshareTrips: "2+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Tennessee",
    slug: "tennessee",
    abbreviation: "TN",
    capital: "Nashville",
    majorCities: ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville"],
    statuteOfLimitations: "1 year",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$15,000",
    rideshareRegulations: "TNC legislation 2015. State preempts local regulations.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["ONLY 1 YEAR statute of limitations", "Nashville is one of fastest growing rideshare markets", "Broadway/honky tonk district extremely busy", "Memphis Beale Street tourism", "Music tourism drives constant demand"],
    majorAirports: ["Nashville (BNA)", "Memphis (MEM)"],
    rideshareAccidentHotspots: ["Broadway Nashville", "BNA airport routes", "Beale Street Memphis", "Downtown Knoxville", "The Gulch Nashville"],
    annualRideshareTrips: "40+ million",
    averageSettlement: "$50,000 - $400,000"
  },
  {
    name: "Texas",
    slug: "texas",
    abbreviation: "TX",
    capital: "Austin",
    majorCities: ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$30,000/$60,000/$25,000",
    rideshareRegulations: "Comprehensive TNC legislation 2017. State preempts local regulations after Austin fight.",
    tncInsuranceRequirements: "Standard three-period model. Enhanced requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Multiple top-10 rideshare markets (Houston, Dallas, Austin, San Antonio)", "DFW and IAH among busiest airports", "SXSW creates Austin surge", "Oil industry drives business travel", "Long driving distances"],
    majorAirports: ["DFW", "Houston IAH", "Houston Hobby (HOU)", "Austin (AUS)", "San Antonio (SAT)"],
    rideshareAccidentHotspots: ["6th Street Austin", "Deep Ellum Dallas", "Downtown Houston", "River Walk San Antonio", "All major airport routes"],
    annualRideshareTrips: "200+ million",
    averageSettlement: "$60,000 - $550,000"
  },
  {
    name: "Utah",
    slug: "utah",
    abbreviation: "UT",
    capital: "Salt Lake City",
    majorCities: ["Salt Lake City", "West Valley City", "Provo", "West Jordan", "Orem"],
    statuteOfLimitations: "4 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$65,000/$15,000 (PIP required)",
    rideshareRegulations: "TNC legislation 2015. PSC oversight.",
    tncInsuranceRequirements: "Standard model plus Utah's no-fault PIP requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Ski resort traffic drives demand", "SLC Airport is major hub", "BYU/Utah games create surge", "Tech industry growth (Silicon Slopes)", "4-year statute of limitations"],
    majorAirports: ["Salt Lake City (SLC)"],
    rideshareAccidentHotspots: ["Downtown SLC", "SLC airport routes", "Park City ski areas", "Provo/BYU area", "I-15 corridor"],
    annualRideshareTrips: "20+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Vermont",
    slug: "vermont",
    abbreviation: "VT",
    capital: "Montpelier",
    majorCities: ["Burlington", "South Burlington", "Rutland", "Essex Junction", "Bennington"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$10,000",
    rideshareRegulations: "TNC legislation 2017. DMV oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Ski resort tourism drives demand", "Limited rideshare outside Burlington", "Fall foliage tourism creates surge", "UVM creates Burlington demand"],
    majorAirports: ["Burlington (BTV)"],
    rideshareAccidentHotspots: ["Downtown Burlington", "Church Street", "Stowe/ski area routes", "BTV airport"],
    annualRideshareTrips: "2+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Virginia",
    slug: "virginia",
    abbreviation: "VA",
    capital: "Richmond",
    majorCities: ["Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Arlington", "Alexandria"],
    statuteOfLimitations: "2 years",
    faultSystem: "Contributory negligence (pure)",
    minAutoInsurance: "$30,000/$60,000/$20,000",
    rideshareRegulations: "Comprehensive TNC legislation 2015. DMV oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["CONTRIBUTORY NEGLIGENCE - Any fault bars recovery", "DC metro extends into NoVA - major rideshare market", "Multiple airports serve Northern Virginia", "Military bases create demand", "Virginia Beach tourism"],
    majorAirports: ["Dulles (IAD)", "Reagan National (DCA)", "Richmond (RIC)", "Norfolk (ORF)"],
    rideshareAccidentHotspots: ["Dulles airport routes", "Tysons Corner", "Arlington/Pentagon City", "Virginia Beach oceanfront", "Richmond downtown"],
    annualRideshareTrips: "50+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "Washington",
    slug: "washington",
    abbreviation: "WA",
    capital: "Olympia",
    majorCities: ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue"],
    statuteOfLimitations: "3 years",
    faultSystem: "Pure comparative fault",
    minAutoInsurance: "$25,000/$50,000/$10,000 (PIP optional)",
    rideshareRegulations: "Comprehensive TNC legislation. UTC oversight. Seattle has additional requirements.",
    tncInsuranceRequirements: "Standard model. Enhanced Seattle requirements.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Seattle is #9 rideshare market", "Tech industry drives high rideshare demand", "Sea-Tac is major hub", "Rainy weather affects driving safety", "Amazon HQ creates concentrated demand"],
    majorAirports: ["Seattle-Tacoma (SEA)", "Spokane (GEG)"],
    rideshareAccidentHotspots: ["Capitol Hill Seattle", "Downtown Seattle", "SEA airport routes", "SLU/Amazon campus", "Bellevue downtown"],
    annualRideshareTrips: "60+ million",
    averageSettlement: "$55,000 - $450,000"
  },
  {
    name: "West Virginia",
    slug: "west-virginia",
    abbreviation: "WV",
    capital: "Charleston",
    majorCities: ["Charleston", "Huntington", "Morgantown", "Parkersburg", "Wheeling"],
    statuteOfLimitations: "2 years",
    faultSystem: "Modified comparative fault (50%)",
    minAutoInsurance: "$25,000/$50,000/$25,000",
    rideshareRegulations: "TNC legislation 2016. PSC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Limited rideshare availability outside major cities", "WVU creates Morgantown demand", "Mountain roads create driving challenges", "Casino tourism in some areas"],
    majorAirports: ["Yeager/Charleston (CRW)", "Morgantown (MGW)"],
    rideshareAccidentHotspots: ["Downtown Charleston", "Morgantown downtown", "High Street area", "Casino routes"],
    annualRideshareTrips: "3+ million",
    averageSettlement: "$40,000 - $300,000"
  },
  {
    name: "Wisconsin",
    slug: "wisconsin",
    abbreviation: "WI",
    capital: "Madison",
    majorCities: ["Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine"],
    statuteOfLimitations: "3 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$10,000",
    rideshareRegulations: "TNC legislation 2015. DOT oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Packers games create Green Bay surge", "UW-Madison drives student demand", "Summerfest creates Milwaukee surge", "Harsh winter weather affects driving"],
    majorAirports: ["Milwaukee Mitchell (MKE)", "Madison (MSN)"],
    rideshareAccidentHotspots: ["Downtown Milwaukee", "Third Ward", "State Street Madison", "Lambeau Field area", "MKE airport routes"],
    annualRideshareTrips: "20+ million",
    averageSettlement: "$45,000 - $350,000"
  },
  {
    name: "Wyoming",
    slug: "wyoming",
    abbreviation: "WY",
    capital: "Cheyenne",
    majorCities: ["Cheyenne", "Casper", "Laramie", "Gillette", "Rock Springs"],
    statuteOfLimitations: "4 years",
    faultSystem: "Modified comparative fault (51%)",
    minAutoInsurance: "$25,000/$50,000/$20,000",
    rideshareRegulations: "TNC legislation 2017. PSC oversight.",
    tncInsuranceRequirements: "Standard three-period insurance model.",
    uberCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    lyftCoverage: {
      offline: "Driver's personal insurance only",
      appOnWaiting: "$50,000/$100,000 liability, $25,000 property",
      enRouteAndTrip: "$1,000,000 liability, $1,000,000 UM/UIM"
    },
    uniqueRideshareFactors: ["Very limited rideshare availability", "Yellowstone/Grand Teton tourism", "Long driving distances", "Wildlife collision risk", "Extreme weather conditions"],
    majorAirports: ["Jackson Hole (JAC)", "Casper (CPR)", "Cheyenne (CYS)"],
    rideshareAccidentHotspots: ["Jackson Hole area", "Cheyenne downtown", "Yellowstone gateway routes"],
    annualRideshareTrips: "1+ million",
    averageSettlement: "$40,000 - $300,000"
  }
];

export function getStateBySlug(slug: string): StateData | undefined {
  return states.find(state => state.slug === slug);
}
