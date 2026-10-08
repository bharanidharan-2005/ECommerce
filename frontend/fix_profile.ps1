$file = "C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"
$content = Get-Content $file -Raw
$content = $content -replace "import \{ loginSuccess \} from `"`.\./features/auth/authSlice`";", "import { updateUser } from `"../features/auth/authSlice`";"
$content = $content -replace "dispatch\(loginSuccess\(\{ user: data, token: localStorage\.getItem\(`"accessToken`"\) \}\)\);", "dispatch(updateUser(data));"
Set-Content $file $content -Encoding utf8
