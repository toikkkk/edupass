"use client"

import { Button } from "@/components/ui/button"
import { Building2, BookOpen, School } from "lucide-react"
import { motion, useInView } from "framer-motion"
import { useRef, useEffect, useState } from "react"

function CountUpNumber({ end, suffix = "" }: { end: number; suffix?: string }) {
  const [count, setCount] = useState(0)
  const ref = useRef<HTMLSpanElement>(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })
  const hasAnimated = useRef(false)

  useEffect(() => {
    if (isInView && !hasAnimated.current) {
      hasAnimated.current = true
      const duration = 2000
      const startTime = performance.now()
      
      const animate = (currentTime: number) => {
        const elapsed = currentTime - startTime
        const progress = Math.min(elapsed / duration, 1)
        const easeOutQuart = 1 - Math.pow(1 - progress, 4)
        const currentCount = Math.floor(easeOutQuart * end)
        
        setCount(currentCount)
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          setCount(end)
        }
      }
      
      requestAnimationFrame(animate)
    }
  }, [isInView, end])

  return (
    <span ref={ref}>
      {count.toLocaleString()}{suffix}
    </span>
  )
}

export function StatsCtaSection() {
  const stats = [
    {
      icon: Building2,
      value: 146,
      suffix: "",
      label: "PTN"
    },
    {
      icon: BookOpen,
      value: 5053,
      suffix: "",
      label: "Program Studi"
    },
    {
      icon: School,
      value: 1000,
      suffix: "+",
      label: "Sekolah"
    }
  ]

  const containerRef = useRef(null)
  const isInView = useInView(containerRef, { once: true, margin: "-100px" })

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94]
      }
    }
  }

  return (
    <section className="bg-[#0F172A] px-4 py-24">
      <motion.div 
        ref={containerRef}
        className="mx-auto max-w-4xl text-center"
        variants={containerVariants}
        initial="hidden"
        animate={isInView ? "visible" : "hidden"}
      >
        {/* Stats */}
        <motion.div className="mb-16 flex flex-wrap items-center justify-center gap-12 md:gap-24">
          {stats.map((stat, index) => (
            <motion.div 
              key={index} 
              className="flex flex-col items-center"
              variants={itemVariants}
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <motion.div 
                className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-500/10"
                whileHover={{ 
                  backgroundColor: "rgba(59, 130, 246, 0.2)",
                  rotate: [0, -10, 10, 0]
                }}
                transition={{ duration: 0.4 }}
              >
                <stat.icon className="h-6 w-6 text-blue-400" />
              </motion.div>
              <span className="font-serif text-3xl text-white md:text-4xl">
                <CountUpNumber end={stat.value} suffix={stat.suffix} />
              </span>
              <span className="text-sm text-gray-400">
                {stat.label}
              </span>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div 
          className="mx-auto max-w-2xl"
          variants={itemVariants}
        >
          <motion.h2 
            className="mb-4 font-serif text-2xl text-white md:text-3xl"
            variants={itemVariants}
          >
            Siap Meraih PTN Impianmu?
          </motion.h2>
          <motion.p 
            className="mb-8 text-gray-400"
            variants={itemVariants}
          >
            Bergabung dengan ribuan siswa yang sudah menggunakan EduPass untuk merencanakan strategi SNBP mereka.
          </motion.p>
          <motion.div 
            className="flex flex-wrap items-center justify-center gap-4"
            variants={itemVariants}
          >
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
              <Button
                size="lg"
                className="rounded-full bg-blue-500 px-8 text-white hover:bg-blue-600"
              >
                Mulai Sekarang
              </Button>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}>
              <Button
                size="lg"
                variant="outline"
                className="rounded-full border-gray-700 text-gray-300 hover:bg-gray-800 hover:text-white"
              >
                Pelajari Lebih Lanjut
              </Button>
            </motion.div>
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  )
}
