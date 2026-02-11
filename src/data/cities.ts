// Extract all cities from states data for city-specific pages
import { states } from './states';
import type { City } from './states';

export type { City };

// Get all cities across all states
export const cities: City[] = states.flatMap(state => state.cities);

// Get a city by slug
export function getCityBySlug(citySlug: string): City | undefined {
  return cities.find(c => c.slug === citySlug);
}

// Get cities by state
export function getCitiesByState(stateSlug: string): City[] {
  const state = states.find(s => s.slug === stateSlug);
  return state?.cities || [];
}

// Get top cities by population
export function getTopCities(limit: number = 50): City[] {
  return [...cities]
    .filter(c => c.population)
    .sort((a, b) => (b.population || 0) - (a.population || 0))
    .slice(0, limit);
}

// Get cities with highest bike scores
export function getBikeFriendlyCities(limit: number = 20): City[] {
  return [...cities]
    .filter(c => c.bikeScore && c.bikeScore > 50)
    .sort((a, b) => (b.bikeScore || 0) - (a.bikeScore || 0))
    .slice(0, limit);
}
