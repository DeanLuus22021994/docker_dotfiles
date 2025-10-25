import { Service } from '../../types/cluster'
import { ServiceCard } from './ServiceCard'
import { Loader2 } from 'lucide-react'

interface ServiceGridProps {
  services: Service[]
  isLoading: boolean
}

export const ServiceGrid = ({ services, isLoading }: ServiceGridProps) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary-500" />
      </div>
    )
  }

  return (
    <section className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Services
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {services.map((service) => (
          <ServiceCard key={service.id} service={service} />
        ))}
      </div>
    </section>
  )
}
