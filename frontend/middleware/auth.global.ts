import { useAuth } from '~/composables/useAuth';
import { useLocalePath } from '#imports';

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isAuthenticated, fetchUser, user, hasPermission } = useAuth();
  const localePath = useLocalePath();

  // Define public route names (accessible by everyone)
  const publicRouteNames = ['index', 'announcements'];

  // Define guest-only route names (accessible only by unauthenticated users)
  const guestOnlyRouteNames = ['login', 'register', 'forgot-password', 'reset-password'];

  // Check if the route is public or guest-only
  const isPublicRoute = publicRouteNames.some(name => to.name?.toString().startsWith(name));
  const isGuestOnlyRoute = guestOnlyRouteNames.some(name => to.name?.toString().startsWith(name));

  // If user object doesn't exist, try to fetch it.
  if (!user.value) {
    await fetchUser();
  }

  // If the user is authenticated
  if (isAuthenticated.value) {
    // If they are trying to access a guest-only route (like login), redirect them to the homepage.
    if (isGuestOnlyRoute) {
      return navigateTo(localePath('/'));
    }

    // Check for route-specific permissions defined in page metadata
    const requiredPermission = to.meta.permission as string;

    // If a permission is required but the user doesn't have it, redirect.
    if (requiredPermission && !hasPermission(requiredPermission)) {
      return navigateTo(localePath('/')); // Redirect to a safe page like home/dashboard
    }

  } else { // If the user is not authenticated
    // And if the route is not public AND not guest-only, redirect them to the login page.
    if (!isPublicRoute && !isGuestOnlyRoute) {
      return navigateTo(localePath('/login'));
    }
  }

  // If none of the above conditions are met, allow navigation.
});