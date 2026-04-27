"use client"

import { Button } from "@/components/ui/button"
import { PredictionCard } from "@/components/prediction-card"
import { TargetCard } from "@/components/target-card"
import { UniversityCard } from "@/components/university-card"
import { NoteCard } from "@/components/note-card"
import { InfiniteGrid } from "@/components/ui/the-infinite-grid"
import { motion } from "framer-motion"

export function HeroSection() {
  return (
    <div className="px-4 pb-8 pt-4">
      {/* Bordered Container with Paper Background */}
      <div className="relative mx-auto min-h-[calc(100vh-120px)] overflow-hidden rounded-3xl border border-gray-200">
        {/* Infinite Grid Background */}
        <InfiniteGrid className="absolute inset-0" showGlows={false}>
          <div className="h-full w-full bg-gradient-to-b from-gray-50/90 to-gray-100/80" />
        </InfiniteGrid>

        {/* Paper texture lines */}
        <svg
          className="pointer-events-none absolute inset-0 h-full w-full opacity-30"
          preserveAspectRatio="none"
          viewBox="0 0 1440 900"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M-100 300 Q 400 150, 800 280 T 1600 220"
            stroke="#d1d5db"
            strokeWidth="1.5"
            fill="none"
          />
          <path
            d="M-100 450 Q 350 280, 750 400 T 1550 350"
            stroke="#d1d5db"
            strokeWidth="1.5"
            fill="none"
          />
          <path
            d="M-100 600 Q 450 420, 850 550 T 1650 500"
            stroke="#d1d5db"
            strokeWidth="1.5"
            fill="none"
          />
          <path
            d="M-100 750 Q 380 580, 780 700 T 1580 650"
            stroke="#d1d5db"
            strokeWidth="1.5"
            fill="none"
          />
        </svg>

        <div className="relative flex min-h-[calc(100vh-120px)] items-center justify-center px-4 py-16">
          {/* Floating Cards - Top Left (Sticky Note) */}
          <motion.div 
            className="absolute left-8 top-20 hidden -rotate-6 lg:block xl:left-20"
            whileHover={{ 
              scale: 1.08, 
              rotate: 0,
              y: -8,
              transition: { type: "spring", stiffness: 400, damping: 15 }
            }}
            whileTap={{ scale: 0.98 }}
          >
            <NoteCard />
          </motion.div>

          {/* Floating Cards - Bottom Left (Prediction/Tasks) */}
          <motion.div 
            className="absolute bottom-20 left-8 hidden rotate-3 lg:block xl:left-12"
            whileHover={{ 
              scale: 1.08, 
              rotate: 0,
              y: -8,
              transition: { type: "spring", stiffness: 400, damping: 15 }
            }}
            whileTap={{ scale: 0.98 }}
          >
            <PredictionCard />
          </motion.div>

          {/* Floating Cards - Top Right (University/Reminders) */}
          <motion.div 
            className="absolute right-8 top-16 hidden rotate-6 lg:block xl:right-16"
            whileHover={{ 
              scale: 1.08, 
              rotate: 0,
              y: -8,
              transition: { type: "spring", stiffness: 400, damping: 15 }
            }}
            whileTap={{ scale: 0.98 }}
          >
            <UniversityCard />
          </motion.div>

          {/* Floating Cards - Bottom Right (Integrations/Target) */}
          <motion.div 
            className="absolute bottom-16 right-8 hidden -rotate-3 lg:block xl:right-20"
            whileHover={{ 
              scale: 1.08, 
              rotate: 0,
              y: -8,
              transition: { type: "spring", stiffness: 400, damping: 15 }
            }}
            whileTap={{ scale: 0.98 }}
          >
            <TargetCard />
          </motion.div>

          {/* Center Content */}
          <div className="z-10 flex max-w-2xl flex-col items-center text-center">
            {/* Logo Icon */}
            <motion.div 
              className="mb-8 flex h-14 w-14 items-center justify-center rounded-xl bg-white shadow-lg"
              whileHover={{ 
                scale: 1.1, 
                rotate: 5,
                transition: { type: "spring", stiffness: 400, damping: 10 }
              }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="grid grid-cols-2 gap-1.5">
                <div className="h-3 w-3 rounded-full bg-cyan-400" />
                <div className="h-3 w-3 rounded-full bg-gray-800" />
                <div className="h-3 w-3 rounded-full bg-gray-800" />
                <div className="h-3 w-3 rounded-full bg-gray-800" />
              </div>
            </motion.div>

            {/* Headline */}
            <h1 className="mb-4 text-balance font-serif text-4xl tracking-tight text-gray-900 md:text-5xl lg:text-[56px] lg:leading-tight">
              Ketahui, rencanakan, dan raih
              <br />
              <span className="text-blue-400">PTN impianmu</span>
            </h1>

            {/* Subheadline */}
            <p className="mb-8 max-w-md text-pretty text-base text-gray-500">
              Prediksi peluangmu masuk PTN favorit dengan Machine Learning yang akurat.
            </p>

            {/* CTA Button */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              <Button
                size="lg"
                className="rounded-full bg-blue-500 px-8 py-6 text-sm font-medium text-white shadow-sm hover:bg-blue-600"
              >
                Cek Peluang Gratis
              </Button>
            </motion.div>
          </div>
        </div>

        {/* Mobile Cards */}
        <div className="grid grid-cols-1 gap-6 px-4 pb-8 sm:grid-cols-2 lg:hidden">
          <PredictionCard />
          <TargetCard />
        </div>
      </div>
    </div>
  )
}
