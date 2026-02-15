import { useState } from "react";
import { Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const scrollTo = (id: string) => {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
};

const navLinks = [
  { id: "features", label: "Features" },
  { id: "how-it-works", label: "How It Works" },
  { id: "gestures", label: "Gestures" },
  { id: "tech-stack", label: "Tech Stack" },
  { id: "download", label: "Download" },
];

const Header = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border">
      <div className="container mx-auto flex items-center justify-between h-16 px-4">
        <button onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })} className="font-display text-lg font-bold text-primary text-glow">
          GesturePlay
        </button>

        <nav className="hidden md:flex items-center gap-8">
          {navLinks.map((l) => (
            <button
              key={l.id}
              onClick={() => scrollTo(l.id)}
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
            >
              {l.label}
            </button>
          ))}
        </nav>

        <button
          onClick={() => scrollTo("download")}
          className="hidden md:inline-flex h-9 px-5 items-center rounded-md bg-primary text-primary-foreground font-semibold text-sm hover:bg-primary/90 transition-colors box-glow"
        >
          Download
        </button>

        <button
          className="md:hidden text-foreground"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-background/95 backdrop-blur-xl border-b border-border overflow-hidden"
          >
            <nav className="flex flex-col gap-1 p-4">
              {navLinks.map((l) => (
                <button
                  key={l.id}
                  onClick={() => { scrollTo(l.id); setMobileOpen(false); }}
                  className="py-3 px-4 rounded-md text-muted-foreground hover:text-primary hover:bg-secondary transition-colors text-left"
                >
                  {l.label}
                </button>
              ))}
              <button
                onClick={() => { scrollTo("download"); setMobileOpen(false); }}
                className="mt-2 h-10 flex items-center justify-center rounded-md bg-primary text-primary-foreground font-semibold text-sm"
              >
                Download
              </button>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

export default Header;
