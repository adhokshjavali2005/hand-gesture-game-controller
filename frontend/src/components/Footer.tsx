const Footer = () => (
  <footer className="border-t border-border py-8">
    <div className="container mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
      <p>Made with ❤️ · Hand Gesture Game Controller © 2026</p>
      <div className="flex gap-6">
        <a href="https://github.com/adhokshjavali2005/hand-gesture-game-controller#readme" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">Documentation</a>
        <a href="https://github.com/adhokshjavali2005/hand-gesture-game-controller/issues" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">Report a Bug</a>
      </div>
    </div>
  </footer>
);

export default Footer;
