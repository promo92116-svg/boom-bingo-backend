from pathlib import Path

# Patch TopBar imports and state
path = Path('src/components/TopBar.tsx')
text = path.read_text(encoding='utf-8')
old_import = 'import { useEffect, useState } from "react";\nimport { useUIStore, uiStore } from "@/store/uiStore";\nimport { updateUserPreferences } from "@/lib/api/user.functions";\nimport { getPlayerKey } from "@/lib/player";\nimport { EyeIcon, EyeSlashIcon, SpeakerIcon, SpeakerMutedIcon } from "./Icons";\n'
new_import = 'import { useEffect, useState } from "react";\nimport { useStore } from "@/lib/store";\nimport { useUIStore, uiStore } from "@/store/uiStore";\nimport { updateUserPreferences } from "@/lib/api/user.functions";\nimport { getPlayerKey } from "@/lib/player";\nimport { EyeIcon, EyeSlashIcon, SpeakerIcon, SpeakerMutedIcon } from "./Icons";\n'
if old_import not in text:
    raise SystemExit('TopBar import block mismatch')
text = text.replace(old_import, new_import)

old_state = '  const sound = useUIStore((s) => s.soundOn);\n  const hideBalance = useUIStore((s) => s.hideBalance);\n  const language = useUIStore((s) => s.language);\n  const [isLanguageMenuOpen, setIsLanguageMenuOpen] = useState(false);\n'
new_state = '  const sound = useUIStore((s) => s.soundOn);\n  const hideBalance = useUIStore((s) => s.hideBalance);\n  const language = useUIStore((s) => s.language);\n  const main = useStore((s) => s.main);\n  const bonus = useStore((s) => s.bonus);\n  const [isLanguageMenuOpen, setIsLanguageMenuOpen] = useState(false);\n'
if old_state not in text:
    raise SystemExit('TopBar state block mismatch')
text = text.replace(old_state, new_state)

old_balance = '        </div>\n      </div>\n\n      <div className="header-right">\n'
new_balance = '        </div>\n\n        <div className="header-balance-chips">\n          <div className="chip">\n            <span className="chip-icon">💳</span>\n            <span className="amount">{hideBalance ? "••••" : main.toFixed(2)}</span>\n            <span className="chip-currency">ETB</span>\n          </div>\n          <div className="chip">\n            <span className="chip-icon">🎁</span>\n            <span className="amount">{hideBalance ? "••••" : bonus.toFixed(2)}</span>\n            <span className="chip-currency">ETB</span>\n          </div>\n        </div>\n\n      </div>\n\n      <div className="header-right">\n'
if old_balance not in text:
    raise SystemExit('TopBar balance insertion point mismatch')
text = text.replace(old_balance, new_balance)
path.write_text(text, encoding='utf-8')
print('patched TopBar')

# Remove standalone home balance strip from index route
path = Path('src/routes/index.tsx')
text = path.read_text(encoding='utf-8')
old_strip = '      <TopBar />\n      <div className="home-balance-strip">\n        <div className="balance-strip-column">\n          <span className="balance-strip-label">Main</span>\n          <span className="balance-strip-value">{showBalance ? `${main.toFixed(2)} ETB` : \'•••• ETB\'}</span>\n        </div>\n        <div className="balance-strip-column">\n          <span className="balance-strip-label">Bonus</span>\n          <span className="balance-strip-value">{showBalance ? `${bonus.toFixed(2)} ETB` : \'•••• ETB\'}</span>\n        </div>\n      </div>\n      <div className="screen">\n'
new_strip = '      <TopBar />\n      <div className="screen">\n'
if old_strip in text:
    text = text.replace(old_strip, new_strip)
else:
    text = text.replace('      <TopBar />\n      <div className="home-balance-strip">', '      <TopBar />\n      <div className="screen">')
path.write_text(text, encoding='utf-8')
print('patched index route')
