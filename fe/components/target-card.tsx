"use client"

import { motion } from "framer-motion"

export function TargetCard() {
  return (
    <motion.div 
      className="w-52 rounded-2xl bg-white p-4 shadow-xl transition-shadow duration-300"
      whileHover={{ 
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.2)",
        transition: { duration: 0.3 }
      }}
    >
      <p className="mb-3 text-sm font-medium text-gray-900">100+ Universitas</p>
      
      <div className="flex flex-wrap gap-2">
        {/* Gmail-style icon */}
        <motion.div 
          className="flex h-11 w-11 items-center justify-center rounded-xl bg-white shadow-md ring-1 ring-gray-100"
          whileHover={{ 
            scale: 1.15, 
            y: -4,
            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.15)",
            transition: { type: "spring", stiffness: 400, damping: 15 }
          }}
          whileTap={{ scale: 0.95 }}
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6">
            <path fill="#EA4335" d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/>
          </svg>
        </motion.div>
        
        {/* Slack-style icon */}
        <motion.div 
          className="flex h-11 w-11 items-center justify-center rounded-xl bg-white shadow-md ring-1 ring-gray-100"
          whileHover={{ 
            scale: 1.15, 
            y: -4,
            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.15)",
            transition: { type: "spring", stiffness: 400, damping: 15 }
          }}
          whileTap={{ scale: 0.95 }}
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6">
            <path fill="#E01E5A" d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z"/>
          </svg>
        </motion.div>
        
        {/* Calendar icon */}
        <motion.div 
          className="flex h-11 w-11 items-center justify-center rounded-xl bg-white shadow-md ring-1 ring-gray-100"
          whileHover={{ 
            scale: 1.15, 
            y: -4,
            boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.15)",
            transition: { type: "spring", stiffness: 400, damping: 15 }
          }}
          whileTap={{ scale: 0.95 }}
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6">
            <path fill="#4285F4" d="M19.5 3h-3V1.5h-1.5V3h-6V1.5H7.5V3h-3A1.5 1.5 0 0 0 3 4.5v15A1.5 1.5 0 0 0 4.5 21h15a1.5 1.5 0 0 0 1.5-1.5v-15A1.5 1.5 0 0 0 19.5 3zm0 16.5h-15V9h15v10.5z"/>
            <text x="12" y="16" textAnchor="middle" fill="#4285F4" fontSize="8" fontWeight="bold">31</text>
          </svg>
        </motion.div>
      </div>
    </motion.div>
  )
}
