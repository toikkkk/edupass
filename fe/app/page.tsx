import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { FeaturesSection } from "@/components/features-section"
import { ProblemsSection } from "@/components/problems-section"
import { HowItWorksSection } from "@/components/how-it-works-section"
import { StatsCtaSection } from "@/components/stats-cta-section"

export default function Home() {
  return (
    <main className="min-h-screen bg-white scroll-smooth">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <ProblemsSection />
      <HowItWorksSection />
      <StatsCtaSection />
    </main>
  )
}
