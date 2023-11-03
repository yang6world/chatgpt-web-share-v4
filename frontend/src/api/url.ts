enum ApiUrl {
  Register = '/auth/register',
  Login = '/auth/login',
  Logout = '/auth/logout',
  UserMe = '/user/me',

  Conversation = '/conv',
  AllConversation = '/conv/all',
  UserList = '/user',

  ChatPlugin = '/chat/openai-plugin',
  AllChatPlugins = '/chat/openai-plugins/all',
  InstalledChatPlugins = '/chat/openai-plugins/installed',

  ServerStatus = '/status/common',

  SystemInfo = '/system/info',
  SystemRequestStatistics = '/system/stats/request',
  SystemAskStatistics = '/system/stats/ask',
  ServerLogs = '/system/logs/server',
  SystemActionSyncOpenaiWebConversations = '/system/action/sync-openai-web-conv',

  SystemConfig = '/system/config',
  SystemCredentials = '/system/credentials',

  FilesLocalUpload = '/files/local/upload',
  FilesLocalDownload = '/files/local/download',
  FilesOpenaiWebUploadStart = '/files/openai-web/upload-start',
  FilesOpenaiWebUploadComplete = '/files/openai-web/upload-complete',
  FilesLocalUploadToOpenaiWeb = '/files/local/upload-to-openai-web',
}

export default ApiUrl;
