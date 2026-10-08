$file = "C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\auth\authSlice.js"
$content = Get-Content $file -Raw
$content = $content -replace "clearError\(state\) \{`r`n      state\.error = null;`r`n    \},", "clearError(state) {`r`n      state.error = null;`r`n    },`r`n    updateUser(state, action) {`r`n      state.user = { ...state.user, ...action.payload };`r`n      localStorage.setItem(`"auth`", JSON.stringify({ access: state.access, refresh: state.refresh, user: state.user }));`r`n    },"
$content = $content -replace "export const \{ logout, clearError \} = authSlice\.actions;", "export const { logout, clearError, updateUser } = authSlice.actions;"
Set-Content $file $content -Encoding utf8
