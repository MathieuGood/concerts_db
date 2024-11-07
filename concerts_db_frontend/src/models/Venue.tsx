export interface Venue {
    id: number
    name: string
    address_id: number
    address?: {
        country: string
        id: number
        city: string
    }
}
