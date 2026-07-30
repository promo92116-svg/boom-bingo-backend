from pathlib import Path

files = []

# BottomNav.tsx
path = Path('src/components/BottomNav.tsx')
text = path.read_text(encoding='utf-8')
old1 = '''  useEffect(() => setMounted(true), []);

  if (!mounted) return null;

  const accentHex = {
    classic: "#7c5cfc",
    violet: "#7c5cfc",
    navy: "#1e293b",
    green: "#22c55e",
    orange: "#f97316",
    purple: "#a855f7",
  }[appTheme] ?? "#7c5cfc";

  const inactiveHex = "#9ca3af";

  return (
    <div className="bottom-nav">
'''
new1 = '''  useEffect(() => setMounted(true), []);

  if (!mounted) return null;

  return (
    <div className="bottom-nav">
'''
if old1 not in text:
    raise SystemExit('BottomNav.tsx missing expected chunk 1')
text = text.replace(old1, new1)
old2 = '''          <button
            type="button"
            key={tab.id}
            onClick={() => navigate({ to: tab.path })}
            className={`nav-tab ${isActive ? "active" : ""}`}
            aria-label={tab.label}
            style={
              isActive
                ? {
                    backgroundColor: accentHex,
                    color: "#ffffff",
                  }
                : {
                    color: inactiveHex,
                  }
            }
          >
            <Icon className="nav-icon" />
          </button>
'''
new2 = '''          <button
            type="button"
            key={tab.id}
            onClick={() => navigate({ to: tab.path })}
            className={`nav-tab ${isActive ? "active" : ""}`}
            aria-label={tab.label}
            aria-current={isActive ? "page" : undefined}
          >
            <Icon className="nav-icon" />
          </button>
'''
if old2 not in text:
    raise SystemExit('BottomNav.tsx missing expected chunk 2')
text = text.replace(old2, new2)
path.write_text(text, encoding='utf-8')
print('patched BottomNav.tsx')

# index.tsx
path = Path('src/routes/index.tsx')
text = path.read_text(encoding='utf-8')
old3 = '''  return (
    <MainLayout>
      <TopBar />
      <div className="screen">
        {showRegistrationBonus ? (
'''
new3 = '''  return (
    <MainLayout>
      <TopBar />
      <div className="home-balance-strip">
        <div className="balance-strip-column">
          <span className="balance-strip-label">Main</span>
          <span className="balance-strip-value">{showBalance ? f"{main:.2f} ETB" : "•••• ETB"}</span>
        </div>
        <div className="balance-strip-column">
          <span className="balance-strip-label">Bonus</span>
          <span className="balance-strip-value">{showBalance ? f"{bonus:.2f} ETB" : "•••• ETB"}</span>
        </div>
      </div>
      <div className="screen">
        {showRegistrationBonus ? (
'''
if old3 not in text:
    raise SystemExit('index.tsx missing expected chunk')
text = text.replace(old3, new3)
path.write_text(text, encoding='utf-8')
print('patched index.tsx')

# globals.css
path = Path('src/styles/globals.css')
text = path.read_text(encoding='utf-8')
old4 = '''.nav-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 8px 4px;
  border-radius: 100px;
  transition: all 0.2s ease;
  cursor: pointer;
  color: var(--text-dim);
}

.nav-tab.active {
  background: linear-gradient(135deg, var(--accent), var(--gold));
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  color: #ffffff;
  padding: 8px 16px;
}

.nav-icon {
  width: 22px;
  height: 22px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.nav-tab.active .nav-icon {
  stroke-width: 2.4;
}
'''
new4 = '''.nav-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 8px 4px;
  border-radius: 100px;
  transition: all 0.2s ease;
  cursor: pointer;
  color: var(--text-dim);
}

.nav-tab.active {
  background: linear-gradient(135deg, var(--accent), var(--accent-l));
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.14);
  color: #ffffff;
  padding: 8px 16px;
}

.nav-icon {
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.nav-tab.active .nav-icon {
  stroke-width: 2.4;
}
'''
if old4 not in text:
    raise SystemExit('globals.css missing expected nav chunk')
text = text.replace(old4, new4)
old5 = '''.header-pill {
  position: relative;
  width: 100%;
  max-width: 480px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  margin: 0 auto 8px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(247, 245, 255, 0.92));
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid var(--border);
  border-radius: 0 0 16px 16px;
  box-shadow: var(--shadow-lg);
  box-sizing: border-box;
}
'''
new5 = old5 + '''
.logo-placeholder {
  background: var(--bg2);
  border: 1px solid var(--border);
}

.logo-placeholder-label {
  font-size: 10px;
  line-height: 1;
  color: var(--text-dim);
  font-weight: 700;
}
'''
if old5 not in text:
    raise SystemExit('globals.css missing expected header chunk')
text = text.replace(old5, new5)
old6 = '''  .header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}
'''
new6 = '''  .header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.home-balance-strip {
  width: 100%;
  max-width: 480px;
  margin: 0 auto 12px;
  padding: 10px 12px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--shadow-sm);
}

.balance-strip-column {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.balance-strip-label {
  font-size: 10px;
  color: var(--text-dim);
}

.balance-strip-value {
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
}
'''
if old6 not in text:
    raise SystemExit('globals.css missing expected header-left chunk')
text = text.replace(old6, new6)
path.write_text(text, encoding='utf-8')
print('patched globals.css')
