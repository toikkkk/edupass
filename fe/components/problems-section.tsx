"use client"

import { AlertTriangle } from "lucide-react"
import { motion, useInView } from "framer-motion"
import { useRef } from "react"

export function ProblemsSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  const problems = [
    {
      title: "Tidak Tahu Passing Grade",
      description: "Siswa tidak mengetahui berapa nilai minimum yang dibutuhkan untuk masuk prodi impian di PTN tertentu."
    },
    {
      title: "Mengabaikan Bobot Sekolah",
      description: "Nilai 90 dari sekolah berbeda memiliki bobot berbeda. Banyak siswa tidak menyadari faktor indeks sekolah dalam SNBP."
    },
    {
      title: "Tidak Ada Target Per Semester",
      description: "Siswa kelas 10-11 tidak memiliki target nilai yang jelas untuk dicapai agar kompetitif saat mendaftar SNBP."
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
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

  const cardVariants = {
    hidden: { opacity: 0, y: 30, scale: 0.95 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }
    }
  }

  return (
    <section className="bg-[#0F172A] px-4 py-24">
      <motion.div 
        ref={ref}
        className="mx-auto max-w-6xl"
        variants={containerVariants}
        initial="hidden"
        animate={isInView ? "visible" : "hidden"}
      >
        {/* Section Header */}
        <motion.div className="mb-16 text-center" variants={headerVariants}>
          <h2 className="mb-4 font-serif text-3xl tracking-tight text-white md:text-4xl">
            Masalah yang Sering Dihadapi Siswa SNBP
          </h2>
          <p className="mx-auto max-w-xl text-gray-400">
            Banyak siswa gagal bukan karena nilainya kurang, tapi karena kurang informasi
          </p>
        </motion.div>

        {/* Problem Cards */}
        <div className="grid gap-6 md:grid-cols-3">
          {problems.map((problem, index) => (
            <motion.div
              key={index}
              className="rounded-2xl bg-[#1E293B] p-8"
              variants={cardVariants}
              whileHover={{ 
                y: -8, 
                scale: 1.02,
                boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.3)"
              }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
              <motion.div 
                className="mb-6 flex h-12 w-12 items-center justify-center rounded-xl bg-red-500/10"
                whileHover={{ 
                  scale: 1.1,
                  backgroundColor: "rgba(239, 68, 68, 0.2)"
                }}
                animate={isInView ? {
                  rotate: [0, -5, 5, -5, 0],
                } : {}}
                transition={{ 
                  rotate: { delay: 0.5 + index * 0.2, duration: 0.5 }
                }}
              >
                <AlertTriangle className="h-6 w-6 text-red-400" />
              </motion.div>
              
              <h3 className="mb-3 font-serif text-lg text-white">
                {problem.title}
              </h3>
              
              <p className="text-sm leading-relaxed text-gray-400">
                {problem.description}
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  )
}
