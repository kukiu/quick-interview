(function () {
  // Config
  const PARTICLE_COUNT = 160;
  const EDGE_POINT_COUNT = 32;

  // DOM
  const canvas = document.getElementById("particles-canvas");
  const svg = document.getElementById("diag-svg");
  const diagPathEl = document.getElementById("diag-path");
  const diagGlow = document.getElementById("diag-glow");
  const diagEdge = document.getElementById("diag-edge");
  let ctx = canvas.getContext("2d");
  let particles = [];
  let edgePoints = [];
  let mouse = { x: window.innerWidth/2, y: window.innerHeight/2 };

  // Utility
  function resize() {
    const dpr = window.devicePixelRatio || 1;
    const w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    const h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    initEdgePoints();
  }

  function rand(min, max) {
    return Math.random() * (max - min) + min;
  }

  // Particles
  function initParticles() {
    particles = [];
    const w = window.innerWidth;
    const h = window.innerHeight;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        z: Math.random() * 1.8 + 0.2,
        r: Math.random() * 1.2 + 0.6,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
      });
    }
  }

  // Edge / diagonal
  function initEdgePoints() {
    edgePoints = [];
    for (let i = 0; i < EDGE_POINT_COUNT; i++) {
      edgePoints.push({
        t: i / (EDGE_POINT_COUNT - 1),
        offset: (Math.random() - 0.5) * 28,
      });
    }
  }

  // Build path string for SVG path
  function buildEdgePathString() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const dx = w;
    const dy = h;
    const len = Math.hypot(dx, dy);
    const nx = -dy / len;
    const ny = dx / len;
    let str = "";
    for (let i = 0; i < edgePoints.length; i++) {
      const p = edgePoints[i];
      const t = p.t;
      const cx = t * w;
      const cy = t * h;
      const o = p.offset || 0;
      const px = cx + nx * o;
      const py = cy + ny * o;
      if (i === 0) str += `M ${px.toFixed(2)} ${py.toFixed(2)}`;
      else str += ` L ${px.toFixed(2)} ${py.toFixed(2)}`;
    }
    str += ` L ${w} ${h} L ${w} 0 Z`;
    return str;
  }

  // Particle drawing
  function drawParticles(dt) {
    const w = window.innerWidth;
    const h = window.innerHeight;
    ctx.clearRect(0, 0, w, h);
    const now = Date.now();
    const wind = Math.sin(now / 3500) * 0.3;
    for (let p of particles) {
      const depthScale = 1 / (p.z + 0.4);
      p.vx += (Math.sin((p.y + now / 60) / 130) * 0.001 + wind * 0.01);
      p.vy += (Math.cos((p.x + now / 90) / 100) * 0.001 - 0.002);
      p.x += p.vx * depthScale * dt * 60;
      p.y += p.vy * depthScale * dt * 60;
      if (p.x < -40) p.x = w + 40;
      if (p.x > w + 40) p.x = -40;
      if (p.y < -40) p.y = h + 40;
      if (p.y > h + 40) p.y = -40;
      const radius = Math.max(0.6, p.r * depthScale * 1.6);
      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 6);
      grad.addColorStop(0, "rgba(255,255,255,0.9)");
      grad.addColorStop(0.25, "rgba(255,255,255,0.55)");
      grad.addColorStop(1, "rgba(255,255,255,0)");
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius * 6, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Edge animation
  function stepEdge(elapsed) {
    const w = window.innerWidth, h = window.innerHeight;
    const mx = mouse.x, my = mouse.y;
    for (let i = 0; i < edgePoints.length; i++) {
      const p = edgePoints[i];
      const wave = Math.sin(elapsed * 2 + i * 0.7) * (12 + Math.sin(i*1.1) * 6);
      const tx = p.t * w;
      const ty = p.t * h;
      const dist = Math.hypot(tx - mx, ty - my);
      const influence = Math.max(0, 1 - dist / 420);
      const push = influence * 48;
      p.offset = wave + Math.sin(i*1.3 + elapsed*1.2) * 6 + push;
    }
    const pathStr = buildEdgePathString();
    diagPathEl.setAttribute("d", pathStr);
    diagGlow.setAttribute("d", pathStr);
    diagEdge.setAttribute("d", pathStr);
  }

  // Main loop
  let lastTs = performance.now();
  function loop(ts) {
    const dt = Math.min(40, ts - lastTs) / 1000;
    lastTs = ts;
    drawParticles(dt);
    stepEdge(ts / 1000);
    requestAnimationFrame(loop);
  }

  // Mouse
  function onMove(e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  }
  

  // Floating thoughts
  const thoughts = [
    "Pain of discipline or Pain of regret?",
    "Believe in yourself and your abilities.",
    "Be so good they can't ignore you.",
    "Never give up!",
    "Coding is fun!",
    "Work smart not hard.",
    "Design by Shaurya.",
    "What's the meaning of life?",
    "If there is no struggle, there is no progress.",
    "Don't stop until you're proud.",
  ];

  function createFloatingThought() {
  const thoughtContainer = document.getElementById("floatingThoughts");
  if (!thoughtContainer) return;

  const thoughtText = thoughts[Math.floor(Math.random() * thoughts.length)];
  const thoughtElement = document.createElement("div");
  thoughtElement.className = "floating-thought";
  thoughtElement.textContent = thoughtText;

  const leftPosition = Math.random() * 100;
  thoughtElement.style.left = `${leftPosition}%`;

  const animationDuration = 6 + Math.random() * 6;
  thoughtElement.style.animationDuration = `${animationDuration}s`;

  const delay = Math.random() * 5;
  thoughtElement.style.animationDelay = `${delay}s`;

  thoughtContainer.appendChild(thoughtElement);

  setTimeout(() => {
    thoughtElement.remove();
  }, animationDuration * 1000);
}


  // Init function
  function init() {
    resize();
    initParticles();
    initEdgePoints();
    const pathStr = buildEdgePathString();
    diagPathEl.setAttribute("d", pathStr);
    diagGlow.setAttribute("d", pathStr);
    diagEdge.setAttribute("d", pathStr);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("resize", () => {
      resize();
      initParticles();
    });
    requestAnimationFrame(loop);

    // Start floating thoughts
    setInterval(createFloatingThought, 2000);
  }

  // Add popup error logic
    const popupErrorMessage = document.getElementById("popupErrorMessage");
    if (popupErrorMessage) {
      const alertDanger = document.querySelector(".alert.alert-danger");
      if (alertDanger && alertDanger.textContent.trim() !== "") {
        popupErrorMessage.textContent = alertDanger.textContent.trim();
        popupErrorMessage.style.display = "block";

        // Hide the popup after 5 seconds
        setTimeout(function() {
          popupErrorMessage.style.display = "none";
        }, 5000);
      }
    }

  // Kick off
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
