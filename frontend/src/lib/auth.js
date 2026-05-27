const AUTH_KEY = 'brainpath_auth'

export const getCurrentUser = () => {
  if (typeof window === 'undefined') return null

  const rawUser = window.localStorage.getItem(AUTH_KEY)
  if (!rawUser) return null

  try {
    return JSON.parse(rawUser)
  } catch {
    window.localStorage.removeItem(AUTH_KEY)
    return null
  }
}

export const loginUser = (email) => {
  const role = email.trim().toLowerCase() === 'admin@brainpath.dev' ? 'admin' : 'user'
  const user = {
    email,
    role,
    name: role === 'admin' ? 'Admin' : 'User',
  }

  window.localStorage.setItem(AUTH_KEY, JSON.stringify(user))
  return user
}

export const logoutUser = () => {
  if (typeof window === 'undefined') return
  window.localStorage.removeItem(AUTH_KEY)
}

export const isAuthenticated = () => Boolean(getCurrentUser())

export const hasRole = (role) => getCurrentUser()?.role === role
