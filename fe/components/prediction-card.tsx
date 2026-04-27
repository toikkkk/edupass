"use client"

import { motion } from "framer-motion"

export function PredictionCard() {
  return (
    <motion.div 
      className="w-56 rounded-2xl bg-white p-4 shadow-xl transition-shadow duration-300"
      whileHover={{ 
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.2)",
        transition: { duration: 0.3 }
      }}
    >
      <p className="mb-3 text-sm font-medium text-gray-900">{"Today's tasks"}</p>
      
      <div className="space-y-3">
        {/* Task 1 */}
        <motion.div 
          className="flex items-center gap-3"
          whileHover={{ x: 4, transition: { duration: 0.2 } }}
        >
          <motion.div 
            className="flex h-6 w-6 shrink-0 items-center justify-center rounded bg-red-100 text-xs font-semibold text-red-600"
            whileHover={{ scale: 1.15, transition: { type: "spring", stiffness: 400 } }}
          >
            S
          </motion.div>
          <div className="flex-1">
            <p className="text-xs font-medium text-gray-800">Target Nilai Raport</p>
            <div className="mt-1 flex items-center gap-2">
              <span className="text-[10px] text-gray-400">Sem 10</span>
              <div className="h-1 flex-1 overflow-hidden rounded-full bg-gray-100">
                <div className="h-full w-[60%] rounded-full bg-blue-400" />
              </div>
              <span className="text-[10px] text-gray-500">60%</span>
            </div>
          </div>
        </motion.div>
        
        {/* Task 2 */}
        <motion.div 
          className="flex items-center gap-3"
          whileHover={{ x: 4, transition: { duration: 0.2 } }}
        >
          <motion.div 
            className="flex h-6 w-6 shrink-0 items-center justify-center rounded bg-blue-100 text-xs font-semibold text-blue-600"
            whileHover={{ scale: 1.15, transition: { type: "spring", stiffness: 400 } }}
          >
            D
          </motion.div>
          <div className="flex-1">
            <p className="text-xs font-medium text-gray-800">Design PPT #4</p>
            <div className="mt-1 flex items-center gap-2">
              <span className="text-[10px] text-gray-400">Sem 18</span>
              <div className="h-1 flex-1 overflow-hidden rounded-full bg-gray-100">
                <div className="h-full w-full rounded-full bg-red-400" />
              </div>
              <span className="text-[10px] text-gray-500">112%</span>
            </div>
          </div>
        </motion.div>
      </div>
      
      {/* Avatar group */}
      <div className="mt-3 flex items-center">
        <div className="flex -space-x-2">
          <motion.div 
            className="h-6 w-6 rounded-full border-2 border-white bg-amber-200"
            whileHover={{ scale: 1.25, zIndex: 10, transition: { type: "spring", stiffness: 400 } }}
          />
          <motion.div 
            className="h-6 w-6 rounded-full border-2 border-white bg-blue-200"
            whileHover={{ scale: 1.25, zIndex: 10, transition: { type: "spring", stiffness: 400 } }}
          />
        </div>
      </div>
    </motion.div>
  )
}
