"use client"

import { Clock } from "lucide-react"
import { motion } from "framer-motion"

export function UniversityCard() {
  return (
    <motion.div 
      className="w-52 rounded-2xl bg-white p-4 shadow-xl transition-shadow duration-300"
      whileHover={{ 
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.2)",
        transition: { duration: 0.3 }
      }}
    >
      <motion.div 
        className="mb-3 flex items-center gap-3"
        whileHover={{ x: 3, transition: { duration: 0.2 } }}
      >
        <motion.div 
          className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-100"
          whileHover={{ 
            rotate: 15, 
            scale: 1.1,
            transition: { type: "spring", stiffness: 400 }
          }}
        >
          <Clock className="h-5 w-5 text-gray-600" />
        </motion.div>
        <span className="font-medium text-gray-900">Pengingat</span>
      </motion.div>
      
      <div className="space-y-2">
        <motion.div 
          className="rounded-lg bg-yellow-50 p-3 transition-colors duration-200"
          whileHover={{ 
            scale: 1.03, 
            backgroundColor: "#fef3c7",
            transition: { type: "spring", stiffness: 400, damping: 15 }
          }}
        >
          <p className="text-sm font-medium text-gray-900">SNBP 2025</p>
          <p className="text-xs text-gray-500">Pendaftaran dimulai</p>
        </motion.div>
        
        <motion.div 
          className="flex items-center gap-2 px-1 text-xs text-gray-500"
          whileHover={{ x: 3, transition: { duration: 0.2 } }}
        >
          <motion.div 
            className="h-2 w-2 rounded-full bg-blue-500"
            whileHover={{ 
              scale: 1.5,
              transition: { type: "spring", stiffness: 400 }
            }}
          />
          <span>13:00 - 13:45</span>
        </motion.div>
      </div>
    </motion.div>
  )
}
