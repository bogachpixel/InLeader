export const getTelegramId = (): number => {
  const tg = (window as any).Telegram?.WebApp;
  const user = tg?.initDataUnsafe?.user;
  if (user && user.id) {
    return user.id;
  }
  // Для локальной разработки или теста в браузере (замени на реальный ID админа)
  return 5925660014; 
};

export function useTelegram() {
  const tg = (window as any).Telegram?.WebApp;

  const user = tg?.initDataUnsafe?.user;
  
  // Для локальной разработки, если tg.initDataUnsafe пустой
  const userId = getTelegramId();
  const username = user?.username || "guest";

  const onClose = () => {
    tg?.close();
  };

  const onExpand = () => {
    tg?.expand();
  };

  const ready = () => {
    tg?.ready();
  };

  return {
    tg,
    user,
    userId,
    username,
    onClose,
    onExpand,
    ready,
  };
}
