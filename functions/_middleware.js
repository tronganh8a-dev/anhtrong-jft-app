// Pages Functions: dùng chung logic đăng nhập trong ../auth.js
import { handle } from '../auth.js';
export const onRequest = ({ request, env, next }) => handle(request, env, () => next());
