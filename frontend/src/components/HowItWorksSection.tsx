import { motion } from "framer-motion";
import { Rocket, Monitor, Hand, Play } from "lucide-react";

const steps = [
  { icon: Rocket, title: "Launch the App", desc: "Run the application on your computer." },
  { icon: Monitor, title: "Open Your Game", desc: "Start Hill Climb Racing or any arrow-key game." },
  { icon: Hand, title: "Show Your Hand", desc: "Position your hand in front of your webcam." },
  { icon: Play, title: "Play!", desc: "Open palm to accelerate, closed fist to brake." },
];

const HowItWorksSection = () => (
  <section id="how-it-works" className="py-24 md:py-32 bg-secondary/30">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
          How It <span className="text-primary">Works</span>
        </h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Get started in just four simple steps.
        </p>
      </motion.div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 max-w-5xl mx-auto">
        {steps.map((s, i) => (
          <motion.div
            key={s.title}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.15, duration: 0.5 }}
            className="text-center"
          >
            <div className="relative mx-auto w-20 h-20 rounded-full bg-card border border-border flex items-center justify-center mb-6">
              <s.icon className="w-8 h-8 text-primary" />
              <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-accent text-accent-foreground font-display text-xs font-bold flex items-center justify-center">
                {i + 1}
              </span>
            </div>
            <h3 className="font-display text-base font-semibold mb-2">{s.title}</h3>
            <p className="text-sm text-muted-foreground">{s.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default HowItWorksSection;
