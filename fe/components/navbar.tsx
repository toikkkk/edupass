"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"

export function Navbar() {
  return (
    <header className="w-full bg-white dark:bg-gray-950">
      <div className="mx-auto flex h-16 max-w-[1400px] items-center justify-between px-6">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5">
          <div className="grid grid-cols-2 gap-1">
            <div className="h-2.5 w-2.5 rounded-full bg-gray-900 dark:bg-gray-100" />
            <div className="h-2.5 w-2.5 rounded-full bg-gray-900 dark:bg-gray-100" />
            <div className="h-2.5 w-2.5 rounded-full bg-gray-900 dark:bg-gray-100" />
            <div className="h-2.5 w-2.5 rounded-full bg-gray-900 dark:bg-gray-100" />
          </div>
          <span className="text-base font-semibold tracking-tight text-gray-900 dark:text-gray-100">
            EduPass
          </span>
        </Link>

        {/* Navigation Links - Center */}
        <nav className="hidden items-center gap-8 md:flex">
          <Link
            href="#"
            className="text-sm text-gray-600 transition-colors hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            Fitur
          </Link>
          <Link
            href="#"
            className="text-sm text-gray-600 transition-colors hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            Universitas
          </Link>
          <Link
            href="#"
            className="text-sm text-gray-600 transition-colors hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            Cara Kerja
          </Link>
          <Link
            href="#"
            className="text-sm text-gray-600 transition-colors hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            Harga
          </Link>
        </nav>

        {/* Auth Buttons & Theme Toggle */}
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Link
            href="#"
            className="text-sm text-gray-600 transition-colors hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            Masuk
          </Link>
          <Button className="rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-gray-200">
            Coba Gratis
          </Button>
        </div>
      </div>
    </header>
  )
}
