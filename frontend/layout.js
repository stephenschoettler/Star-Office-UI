// Star Office UI - Layout and Layer Configuration
// All coordinates,depthUnified resource path management here
// Avoid magic numbers, reduce error risk

// Core rules:
// - Transparent resources (like desks) forced .png, opacity prioritized .webp
// - Level: Low → sofa(10) → starWorking(900) → desk(1000) → flower(1100)

const LAYOUT = {
  // === Game canvas ===
  game: {
    width: 1280,
    height: 720
  },

  // === Coordinates of each area ===
  areas: {
    door:        { x: 640, y: 550 },
    writing:     { x: 320, y: 360 },
    researching: { x: 320, y: 360 },
    error:       { x: 1066, y: 180 },
    breakroom:   { x: 640, y: 360 }
  },

  // === Decorations and Furniture: Coordinates + Origin + depth ===
  furniture: {
    // Sofa
    sofa: {
      x: 670,
      y: 144,
      origin: { x: 0, y: 0 },
      depth: 10
    },

    // New desk (transparent PNG Force)
    desk: {
      x: 218,
      y: 417,
      origin: { x: 0.5, y: 0.5 },
      depth: 1000
    },

    // Desk flowerpot
    flower: {
      x: 310,
      y: 405,
      origin: { x: 0.5, y: 0.5 },
      depth: 1100
    },

    // Star Working at the desk (at desk Below)
    starWorking: {
      x: 217,
      y: 333,
      origin: { x: 0.5, y: 0.5 },
      depth: 900,
      scale: 1.32
    },

    // Plants
    plants: [
      { x: 565, y: 178, depth: 5 },
      { x: 230, y: 185, depth: 5 },
      { x: 977, y: 496, depth: 5 }
    ],

    // Poster
    poster: {
      x: 252,
      y: 66,
      depth: 4
    },

    // Coffee Machine
    coffeeMachine: {
      x: 659,
      y: 397,
      origin: { x: 0.5, y: 0.5 },
      depth: 99
    },

    // Server zone
    serverroom: {
      x: 1021,
      y: 142,
      origin: { x: 0.5, y: 0.5 },
      depth: 2
    },

    // Error bug
    errorBug: {
      x: 1007,
      y: 221,
      origin: { x: 0.5, y: 0.5 },
      depth: 50,
      scale: 0.9,
      pingPong: { leftX: 1007, rightX: 1111, speed: 0.6 }
    },

    // Sync Animation
    syncAnim: {
      x: 1157,
      y: 592,
      origin: { x: 0.5, y: 0.5 },
      depth: 40
    },

    // Kitten
    cat: {
      x: 94,
      y: 557,
      origin: { x: 0.5, y: 0.5 },
      depth: 2000
    }
  },

  // === Sign ===
  plaque: {
    x: 640,
    y: 720 - 36,
    width: 420,
    height: 44
  },

  // === Resource loading rules: which are mandatory PNG(Transparent resource) ===
  forcePng: {
    desk_v2: true // New desk must be transparent, enforced PNG
  },

  // === Total resource count (for loading progress bar) ===
  totalAssets: 15
};
