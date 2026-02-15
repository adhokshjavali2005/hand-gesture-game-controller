import { motion } from "framer-motion";
import { Hand, Grip, Circle } from "lucide-react";

const gestures = [
  {
    icon: Hand,
    gesture: "Open Palm",
    action: "ACCELERATE",
    color: "text-primary",
    bgColor: "bg-primary/10",
    borderColor: "border-primary/30",
  },
  {
    icon: Grip,
    gesture: "Closed Fist",
    action: "BRAKE",
    color: "text-accent",
    bgColor: "bg-accent/10",
    borderColor: "border-accent/30",
  },
  {
    icon: Circle,
    gesture: "No Hand",
    action: "IDLE",
    color: "text-muted-foreground",
    bgColor: "bg-muted",
    borderColor: "border-border",
  },
];

const GestureControlsSection = () => (
  <section id="gestures" className="py-24 md:py-32">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
          Gesture <span className="text-primary">Controls</span>
        </h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Simple, intuitive hand gestures to control your game.
        </p>
      </motion.div>

      <div className="flex flex-col md:flex-row gap-8 justify-center items-stretch max-w-4xl mx-auto">
        {gestures.map((g, i) => (
          <motion.div
            key={g.gesture}
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.15, duration: 0.5 }}
            className={`flex-1 rounded-2xl bg-card border ${g.borderColor} p-8 text-center hover:scale-105 transition-transform duration-300`}
          >
            <div className={`w-24 h-24 mx-auto rounded-full ${g.bgColor} flex items-center justify-center mb-6`}>
              <g.icon className={`w-12 h-12 ${g.color}`} />
            </div>
            <h3 className="font-display text-lg font-bold mb-1">{g.gesture}</h3>
            <div className="flex items-center justify-center gap-2 mt-3">
              <span className="text-xs text-muted-foreground">→</span>
              <span className={`font-display text-sm font-bold tracking-wider ${g.color}`}>
                {g.action}
              </span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default GestureControlsSection;
