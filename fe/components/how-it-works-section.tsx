"use client"

import { UserPlus, FileInput, LineChart } from "lucide-react"
import { motion, useInView } from "framer-motion"
import { useRef } from "react"

export function HowItWorksSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  const steps = [
    {
      number: "01",
      icon: UserPlus,
      title: "Daftar & Lengkapi Profil",
      description: "Buat akun dan masukkan informasi sekolah serta kelas kamu saat ini."
    },
    {
      number: "02",
      icon: FileInput,
      title: "Input Nilai & Pilih PTN",
      description: "Masukkan nilai rapor semester yang sudah ada dan pilih PTN serta prodi yang kamu inginkan."
    },
    {
      number: "03",
      icon: LineChart,
      title: "Dapatkan Hasil & Strategi",
      description: "Lihat persentase peluang lolos, rekomendasi alternatif, dan roadmap target nilai per semester."
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.25,
        delayChildren: 0.2
      }
    }
  }

  const headerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  }

  const stepVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }
    }
  }

  const lineVariants = {
    hidden: { scaleX: 0 },
    visible: {
      scaleX: 1,
      transition: { duration: 1, delay: 0.5, ease: "easeOut" }
    }
  }

  return (
    <section className="bg-[#F8FAFC] px-4 py-24">
      <motion.div 
        ref={ref}
        className="mx-auto max-w-6xl"
        variants={containerVariants}
        initial="hidden"
        animate={isInView ? "visible" : "hidden"}
      >
        {/* Section Header */}
        <motion.div className="mb-16 text-center" variants={headerVariants}>
          <h2 className="mb-4 font-serif text-3xl tracking-tight text-gray-900 md:text-4xl">
            Cara Kerja EduPass
          </h2>
          <p className="mx-auto max-w-xl text-gray-500">
            Tiga langkah sederhana menuju strategi SNBP yang lebih cerdas
          </p>
        </motion.div>

        {/* Steps */}
        <div className="relative">
          {/* Animated Dotted Line Connector */}
          <motion.div 
            className="absolute left-1/2 top-16 hidden h-0.5 w-[60%] -translate-x-1/2 origin-left border-t-2 border-dashed border-blue-300 md:block"
            variants={lineVariants}
          />

          <div className="grid gap-12 md:grid-cols-3 md:gap-8">
            {steps.map((step, index) => (
              <motion.div 
                key={index} 
                className="relative flex flex-col items-center text-center"
                variants={stepVariants}
              >
                {/* Number Badge */}
                <motion.div 
                  className="relative mb-6"
                  whileHover={{ scale: 1.1 }}
                  transition={{ type: "spring", stiffness: 400, damping: 17 }}
                >
                  <motion.div 
                    className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-500 text-sm font-semibold text-white shadow-lg"
                    initial={{ scale: 0, rotate: -180 }}
                    animate={isInView ? { scale: 1, rotate: 0 } : { scale: 0, rotate: -180 }}
                    transition={{ 
                      delay: 0.3 + index * 0.2, 
                      type: "spring", 
                      stiffness: 200,
                      damping: 15
                    }}
                  >
                    {step.number}
                  </motion.div>
                </motion.div>

                {/* Icon */}
                <motion.div 
                  className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white shadow-md"
                  whileHover={{ 
                    y: -5, 
                    boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                  }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <motion.div
                    animate={isInView ? {
                      y: [0, -3, 0]
                    } : {}}
                    transition={{
                      delay: 1 + index * 0.3,
                      duration: 2,
                      repeat: Infinity,
                      repeatType: "reverse",
                      ease: "easeInOut"
                    }}
                  >
                    <step.icon className="h-8 w-8 text-blue-500" />
                  </motion.div>
                </motion.div>

                {/* Content */}
                <h3 className="mb-2 font-serif text-lg text-gray-900">
                  {step.title}
                </h3>
                
                <p className="max-w-xs text-sm leading-relaxed text-gray-500">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </section>
  )
}
