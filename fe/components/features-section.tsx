"use client"

import { ChartBar, Target, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { motion, useInView } from "framer-motion"
import { useRef } from "react"

export function FeaturesSection() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.1
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
    hidden: { opacity: 0, y: 40 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.7, ease: [0.25, 0.46, 0.45, 0.94] }
    }
  }

  const listItemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.4 }
    }
  }

  return (
    <section className="bg-white px-4 py-24">
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
            Dua Fitur yang Kamu Butuhkan
          </h2>
          <p className="mx-auto max-w-xl text-gray-500">
            Dirancang khusus untuk siswa SMA yang ingin masuk PTN impian lewat jalur SNBP
          </p>
        </motion.div>

        {/* Feature Cards */}
        <div className="grid gap-8 md:grid-cols-2">
          {/* Card 1 - Prediksi Peluang */}
          <motion.div 
            className="group rounded-2xl border border-gray-200 bg-white p-8"
            variants={cardVariants}
            whileHover={{ 
              y: -8, 
              boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.1)",
              borderColor: "rgb(191, 219, 254)"
            }}
            transition={{ type: "spring", stiffness: 300, damping: 25 }}
          >
            <div className="mb-6 flex items-start justify-between">
              <motion.div 
                className="flex h-14 w-14 items-center justify-center rounded-xl bg-blue-50"
                whileHover={{ scale: 1.1, rotate: 5 }}
                transition={{ type: "spring", stiffness: 400, damping: 17 }}
              >
                <ChartBar className="h-7 w-7 text-blue-500" />
              </motion.div>
              <motion.span 
                className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-600"
                initial={{ scale: 0 }}
                animate={isInView ? { scale: 1 } : { scale: 0 }}
                transition={{ delay: 0.5, type: "spring", stiffness: 500 }}
              >
                Fitur 1
              </motion.span>
            </div>
            
            <h3 className="mb-3 font-serif text-xl text-gray-900">
              Prediksi Peluang Lolos SNBP
            </h3>
            
            <p className="mb-6 text-sm leading-relaxed text-gray-500">
              Masukkan nilai rapor dan pilih PTN tujuanmu. Sistem kami akan menghitung peluang kelulusanmu menggunakan Random Forest yang mempertimbangkan indeks sekolahmu.
            </p>

            <motion.ul 
              className="mb-8 space-y-3"
              variants={containerVariants}
            >
              {["Analisis 5053 program studi", "Perhitungan nilai berbobot otomatis", "Rekomendasi PTN alternatif"].map((item, i) => (
                <motion.li 
                  key={i}
                  className="flex items-center gap-3 text-sm text-gray-600"
                  variants={listItemVariants}
                  custom={i}
                >
                  <motion.div 
                    className="flex h-5 w-5 items-center justify-center rounded-full bg-green-100"
                    whileHover={{ scale: 1.2 }}
                  >
                    <Check className="h-3 w-3 text-green-600" />
                  </motion.div>
                  {item}
                </motion.li>
              ))}
            </motion.ul>

            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button variant="outline" className="rounded-full border-blue-200 text-blue-600 hover:bg-blue-50">
                Coba Prediksi
              </Button>
            </motion.div>
          </motion.div>

          {/* Card 2 - Roadmap Nilai */}
          <motion.div 
            className="group rounded-2xl border border-gray-200 bg-white p-8"
            variants={cardVariants}
            whileHover={{ 
              y: -8, 
              boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.1)",
              borderColor: "rgb(191, 219, 254)"
            }}
            transition={{ type: "spring", stiffness: 300, damping: 25 }}
          >
            <div className="mb-6 flex items-start justify-between">
              <motion.div 
                className="flex h-14 w-14 items-center justify-center rounded-xl bg-blue-50"
                whileHover={{ scale: 1.1, rotate: -5 }}
                transition={{ type: "spring", stiffness: 400, damping: 17 }}
              >
                <Target className="h-7 w-7 text-blue-500" />
              </motion.div>
              <motion.span 
                className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-600"
                initial={{ scale: 0 }}
                animate={isInView ? { scale: 1 } : { scale: 0 }}
                transition={{ delay: 0.7, type: "spring", stiffness: 500 }}
              >
                Fitur 2
              </motion.span>
            </div>
            
            <h3 className="mb-3 font-serif text-xl text-gray-900">
              Roadmap Target Nilai per Semester
            </h3>
            
            <p className="mb-6 text-sm leading-relaxed text-gray-500">
              Belum kelas 12? Tidak masalah. Masukkan nilai semester yang sudah ada dan sistem akan menghitung target nilai yang harus kamu capai tiap semester.
            </p>

            <motion.ul 
              className="mb-8 space-y-3"
              variants={containerVariants}
            >
              {["Target nilai semester 3, 4, dan 5", "Grafik proyeksi tren nilai", "Berbasis Linear Regression"].map((item, i) => (
                <motion.li 
                  key={i}
                  className="flex items-center gap-3 text-sm text-gray-600"
                  variants={listItemVariants}
                  custom={i}
                >
                  <motion.div 
                    className="flex h-5 w-5 items-center justify-center rounded-full bg-green-100"
                    whileHover={{ scale: 1.2 }}
                  >
                    <Check className="h-3 w-3 text-green-600" />
                  </motion.div>
                  {item}
                </motion.li>
              ))}
            </motion.ul>

            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button variant="outline" className="rounded-full border-blue-200 text-blue-600 hover:bg-blue-50">
                Buat Roadmap
              </Button>
            </motion.div>
          </motion.div>
        </div>
      </motion.div>
    </section>
  )
}
