"use client"

import { useEffect, useState, useRef } from "react"

interface UseCountUpOptions {
  end: number
  duration?: number
  startOnMount?: boolean
}

export function useCountUp({ end, duration = 2000, startOnMount = false }: UseCountUpOptions) {
  const [count, setCount] = useState(0)
  const [hasStarted, setHasStarted] = useState(false)
  const countRef = useRef(0)
  const frameRef = useRef<number>()

  const startCounting = () => {
    if (hasStarted) return
    setHasStarted(true)
    
    const startTime = performance.now()
    
    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      
      // Easing function for smooth animation
      const easeOutQuart = 1 - Math.pow(1 - progress, 4)
      const currentCount = Math.floor(easeOutQuart * end)
      
      if (currentCount !== countRef.current) {
        countRef.current = currentCount
        setCount(currentCount)
      }
      
      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate)
      } else {
        setCount(end)
      }
    }
    
    frameRef.current = requestAnimationFrame(animate)
  }

  useEffect(() => {
    if (startOnMount) {
      startCounting()
    }
    
    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current)
      }
    }
  }, [startOnMount])

  return { count, startCounting, hasStarted }
}
