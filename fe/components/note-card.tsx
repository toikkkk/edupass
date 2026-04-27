"use client"

import { Check } from "lucide-react"
import { motion } from "framer-motion"

export function NoteCard() {
  return (
    <div className="relative">
      {/* Yellow sticky note */}
      <motion.div 
        className="w-44 rounded-sm bg-yellow-200 p-4 shadow-lg transition-shadow duration-300"
        whileHover={{ 
          boxShadow: "0 20px 40px -10px rgba(0, 0, 0, 0.25)",
          rotate: 2,
          transition: { type: "spring", stiffness: 300, damping: 15 }
        }}
      >
        {/* Pin */}
        <motion.div 
          className="absolute -top-2 left-1/2 h-4 w-4 -translate-x-1/2 rounded-full bg-red-400 shadow-sm"
          whileHover={{ 
            scale: 1.3,
            transition: { type: "spring", stiffness: 400 }
          }}
        />
        <p className="text-sm italic leading-relaxed text-gray-700">
          Pantau nilai rapormu,
          <br />
          capai target semester,
          <br />
          dan raih PTN impian
          <br />
          dengan lebih mudah.
        </p>
      </motion.div>
      
      {/* Blue checkbox icon */}
      <motion.div 
        className="absolute -bottom-4 -left-4 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-400 shadow-lg"
        whileHover={{ 
          scale: 1.15, 
          rotate: 10,
          boxShadow: "0 15px 30px -5px rgba(59, 130, 246, 0.4)",
          transition: { type: "spring", stiffness: 400, damping: 15 }
        }}
        whileTap={{ scale: 0.95 }}
      >
        <Check className="h-6 w-6 text-white" strokeWidth={3} />
      </motion.div>
    </div>
  )
}
