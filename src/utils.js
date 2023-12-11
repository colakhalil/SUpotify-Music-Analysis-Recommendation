import globalVar from './global';

export const updateGlobalUser = (email, username = '') => {
  globalVar.mail = email;
  if (username) {
    globalVar.username = username;
  }
  console.log(globalVar.username);
  console.log(globalVar.mail);
};
