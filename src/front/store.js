export const initialStore=()=>{
  return{
    message: null,
    todos: [
      {
        id: 1,
        title: "Make the bed",
        background: null,
      },
      {
        id: 2,
        title: "Do my homework",
        background: null,
      }
    ],
    token: sessionStorage.getItem("token") || null, // Recupera el token si existe
    isAuthenticated: !!sessionStorage.getItem("token"), 
    user: null // para guardar datos de usuario
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
    case 'set_hello':
      return {
        ...store,
        message: action.payload
      };
      
    case 'add_task':

      const { id,  color } = action.payload

      return {
        ...store,
        todos: store.todos.map((todo) => (todo.id === id ? { ...todo, background: color } : todo))
      };

      case 'login_success':
        return {
          ...store,
          token: action.payload.token,
          isAuthenticated: true,
          user: action.payload.user
        };
  
      case 'logout':
        return {
          ...store,
          token: null,
          isAuthenticated: false,
          user: null
        };
  
      default:
        throw Error('Unknown action.');
  }    
}

// FETCH 

export const actions = (getStore, setStore) => ({
  login: async (email, password) => {
    try {
      const resp = await fetch("https://literate-lamp-7v7wxwp7v9w9hrrgx-3001.app.github.dev/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      if (!resp.ok) throw new Error("Error en login");

      const data = await resp.json();

      sessionStorage.setItem("token", data.access_token);

      setStore({
        token: data.access_token,
        isAuthenticated: true,
        user: { email: data.email }
      });

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  },

  signup: async (name, email, password) => {
    try {
      const resp = await fetch("https://literate-lamp-7v7wxwp7v9w9hrrgx-3001.app.github.dev/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
      });

      if (!resp.ok) throw new Error("Error en signup");

      const data = await resp.json();

      sessionStorage.setItem("token", data.access_token);

      setStore({
        token: data.access_token,
        isAuthenticated: true,
        user: { email: data.email }
      });

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  },

  logout: () => {
    sessionStorage.removeItem("token");
    setStore({
      token: null,
      isAuthenticated: false,
      user: null
    });
  }
});
