$.jsonrpc.defaultUrl = '/timing/rpc/';
$.jsonrpc.namespace = 'timing';

//base rpc calling function
rpc_call = function (method, options) {
  $.jsonrpc({
    method : method,
    params : options.params
  }, {
    success : function(result) {
      if(options.success) options.success(result);
    },
    error : function(error) {
      if (window.console) {
        console.info('code:', error.code);
        console.info('message:', error.message);
        console.dir(error.data);
      }
      if (options.error) options.error(error);
      else if(error.message.length){
          console.info(error.message);
      }
    }
  },
  options.async);
};

//async rpc call
rpc = function (method, params, success_callback, error_callback) {
  return rpc_call(method, {
    params: params,
    success: success_callback || null,
    error: error_callback || null
  });
};

//sync rpc call
rpc_sync = function (method, params) {
  var result = undefined;
  params = params || [];
  function callback(data) {
    result = data;
  }
  rpc_call(method, {'success': callback, 'async': false, params: params});
  return result;
};