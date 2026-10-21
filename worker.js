// Workers (static assets): mọi request đi qua đăng nhập trước
import { handle } from './auth.js';
export default { fetch: (req, env) => handle(req, env, () => env.ASSETS.fetch(req)) };
