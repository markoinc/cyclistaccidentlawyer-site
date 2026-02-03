function tE(Q) {
  return Q && Q.__esModule && Object.prototype.hasOwnProperty.call(Q, "default") ? Q.default : Q;
}
var Jv = { exports: {} }, bp = {};
var G2;
function DT() {
  if (G2) return bp;
  G2 = 1;
  var Q = /* @__PURE__ */ Symbol.for("react.transitional.element"), te = /* @__PURE__ */ Symbol.for("react.fragment");
  function Be(U, Re, Se) {
    var mt = null;
    if (Se !== void 0 && (mt = "" + Se), Re.key !== void 0 && (mt = "" + Re.key), "key" in Re) {
      Se = {};
      for (var le in Re)
        le !== "key" && (Se[le] = Re[le]);
    } else Se = Re;
    return Re = Se.ref, {
      $$typeof: Q,
      type: U,
      key: mt,
      ref: Re !== void 0 ? Re : null,
      props: Se
    };
  }
  return bp.Fragment = te, bp.jsx = Be, bp.jsxs = Be, bp;
}
var Ep = {}, Kv = { exports: {} }, $e = {};
var X2;
function RT() {
  if (X2) return $e;
  X2 = 1;
  var Q = /* @__PURE__ */ Symbol.for("react.transitional.element"), te = /* @__PURE__ */ Symbol.for("react.portal"), Be = /* @__PURE__ */ Symbol.for("react.fragment"), U = /* @__PURE__ */ Symbol.for("react.strict_mode"), Re = /* @__PURE__ */ Symbol.for("react.profiler"), Se = /* @__PURE__ */ Symbol.for("react.consumer"), mt = /* @__PURE__ */ Symbol.for("react.context"), le = /* @__PURE__ */ Symbol.for("react.forward_ref"), ne = /* @__PURE__ */ Symbol.for("react.suspense"), W = /* @__PURE__ */ Symbol.for("react.memo"), Ne = /* @__PURE__ */ Symbol.for("react.lazy"), w = /* @__PURE__ */ Symbol.for("react.activity"), x = Symbol.iterator;
  function ce(S) {
    return S === null || typeof S != "object" ? null : (S = x && S[x] || S["@@iterator"], typeof S == "function" ? S : null);
  }
  var Ge = {
    isMounted: function() {
      return !1;
    },
    enqueueForceUpdate: function() {
    },
    enqueueReplaceState: function() {
    },
    enqueueSetState: function() {
    }
  }, it = Object.assign, ut = {};
  function Ze(S, H, I) {
    this.props = S, this.context = H, this.refs = ut, this.updater = I || Ge;
  }
  Ze.prototype.isReactComponent = {}, Ze.prototype.setState = function(S, H) {
    if (typeof S != "object" && typeof S != "function" && S != null)
      throw Error(
        "takes an object of state variables to update or a function which returns an object of state variables."
      );
    this.updater.enqueueSetState(this, S, H, "setState");
  }, Ze.prototype.forceUpdate = function(S) {
    this.updater.enqueueForceUpdate(this, S, "forceUpdate");
  };
  function qt() {
  }
  qt.prototype = Ze.prototype;
  function Ot(S, H, I) {
    this.props = S, this.context = H, this.refs = ut, this.updater = I || Ge;
  }
  var Ct = Ot.prototype = new qt();
  Ct.constructor = Ot, it(Ct, Ze.prototype), Ct.isPureReactComponent = !0;
  var wt = Array.isArray;
  function Gt() {
  }
  var Ae = { H: null, A: null, T: null, S: null }, Je = Object.prototype.hasOwnProperty;
  function Me(S, H, I) {
    var F = I.ref;
    return {
      $$typeof: Q,
      type: S,
      key: H,
      ref: F !== void 0 ? F : null,
      props: I
    };
  }
  function se(S, H) {
    return Me(S.type, H, S.props);
  }
  function Yt(S) {
    return typeof S == "object" && S !== null && S.$$typeof === Q;
  }
  function pe(S) {
    var H = { "=": "=0", ":": "=2" };
    return "$" + S.replace(/[=:]/g, function(I) {
      return H[I];
    });
  }
  var Xe = /\/+/g;
  function Kt(S, H) {
    return typeof S == "object" && S !== null && S.key != null ? pe("" + S.key) : H.toString(36);
  }
  function Xt(S) {
    switch (S.status) {
      case "fulfilled":
        return S.value;
      case "rejected":
        throw S.reason;
      default:
        switch (typeof S.status == "string" ? S.then(Gt, Gt) : (S.status = "pending", S.then(
          function(H) {
            S.status === "pending" && (S.status = "fulfilled", S.value = H);
          },
          function(H) {
            S.status === "pending" && (S.status = "rejected", S.reason = H);
          }
        )), S.status) {
          case "fulfilled":
            return S.value;
          case "rejected":
            throw S.reason;
        }
    }
    throw S;
  }
  function R(S, H, I, F, be) {
    var Le = typeof S;
    (Le === "undefined" || Le === "boolean") && (S = null);
    var Oe = !1;
    if (S === null) Oe = !0;
    else
      switch (Le) {
        case "bigint":
        case "string":
        case "number":
          Oe = !0;
          break;
        case "object":
          switch (S.$$typeof) {
            case Q:
            case te:
              Oe = !0;
              break;
            case Ne:
              return Oe = S._init, R(
                Oe(S._payload),
                H,
                I,
                F,
                be
              );
          }
      }
    if (Oe)
      return be = be(S), Oe = F === "" ? "." + Kt(S, 0) : F, wt(be) ? (I = "", Oe != null && (I = Oe.replace(Xe, "$&/") + "/"), R(be, H, I, "", function(wa) {
        return wa;
      })) : be != null && (Yt(be) && (be = se(
        be,
        I + (be.key == null || S && S.key === be.key ? "" : ("" + be.key).replace(
          Xe,
          "$&/"
        ) + "/") + Oe
      )), H.push(be)), 1;
    Oe = 0;
    var $t = F === "" ? "." : F + ":";
    if (wt(S))
      for (var gt = 0; gt < S.length; gt++)
        F = S[gt], Le = $t + Kt(F, gt), Oe += R(
          F,
          H,
          I,
          Le,
          be
        );
    else if (gt = ce(S), typeof gt == "function")
      for (S = gt.call(S), gt = 0; !(F = S.next()).done; )
        F = F.value, Le = $t + Kt(F, gt++), Oe += R(
          F,
          H,
          I,
          Le,
          be
        );
    else if (Le === "object") {
      if (typeof S.then == "function")
        return R(
          Xt(S),
          H,
          I,
          F,
          be
        );
      throw H = String(S), Error(
        "Objects are not valid as a React child (found: " + (H === "[object Object]" ? "object with keys {" + Object.keys(S).join(", ") + "}" : H) + "). If you meant to render a collection of children, use an array instead."
      );
    }
    return Oe;
  }
  function Z(S, H, I) {
    if (S == null) return S;
    var F = [], be = 0;
    return R(S, F, "", "", function(Le) {
      return H.call(I, Le, be++);
    }), F;
  }
  function ee(S) {
    if (S._status === -1) {
      var H = S._result;
      H = H(), H.then(
        function(I) {
          (S._status === 0 || S._status === -1) && (S._status = 1, S._result = I);
        },
        function(I) {
          (S._status === 0 || S._status === -1) && (S._status = 2, S._result = I);
        }
      ), S._status === -1 && (S._status = 0, S._result = H);
    }
    if (S._status === 1) return S._result.default;
    throw S._result;
  }
  var ge = typeof reportError == "function" ? reportError : function(S) {
    if (typeof window == "object" && typeof window.ErrorEvent == "function") {
      var H = new window.ErrorEvent("error", {
        bubbles: !0,
        cancelable: !0,
        message: typeof S == "object" && S !== null && typeof S.message == "string" ? String(S.message) : String(S),
        error: S
      });
      if (!window.dispatchEvent(H)) return;
    } else if (typeof process == "object" && typeof process.emit == "function") {
      process.emit("uncaughtException", S);
      return;
    }
    console.error(S);
  }, De = {
    map: Z,
    forEach: function(S, H, I) {
      Z(
        S,
        function() {
          H.apply(this, arguments);
        },
        I
      );
    },
    count: function(S) {
      var H = 0;
      return Z(S, function() {
        H++;
      }), H;
    },
    toArray: function(S) {
      return Z(S, function(H) {
        return H;
      }) || [];
    },
    only: function(S) {
      if (!Yt(S))
        throw Error(
          "React.Children.only expected to receive a single React element child."
        );
      return S;
    }
  };
  return $e.Activity = w, $e.Children = De, $e.Component = Ze, $e.Fragment = Be, $e.Profiler = Re, $e.PureComponent = Ot, $e.StrictMode = U, $e.Suspense = ne, $e.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = Ae, $e.__COMPILER_RUNTIME = {
    __proto__: null,
    c: function(S) {
      return Ae.H.useMemoCache(S);
    }
  }, $e.cache = function(S) {
    return function() {
      return S.apply(null, arguments);
    };
  }, $e.cacheSignal = function() {
    return null;
  }, $e.cloneElement = function(S, H, I) {
    if (S == null)
      throw Error(
        "The argument must be a React element, but you passed " + S + "."
      );
    var F = it({}, S.props), be = S.key;
    if (H != null)
      for (Le in H.key !== void 0 && (be = "" + H.key), H)
        !Je.call(H, Le) || Le === "key" || Le === "__self" || Le === "__source" || Le === "ref" && H.ref === void 0 || (F[Le] = H[Le]);
    var Le = arguments.length - 2;
    if (Le === 1) F.children = I;
    else if (1 < Le) {
      for (var Oe = Array(Le), $t = 0; $t < Le; $t++)
        Oe[$t] = arguments[$t + 2];
      F.children = Oe;
    }
    return Me(S.type, be, F);
  }, $e.createContext = function(S) {
    return S = {
      $$typeof: mt,
      _currentValue: S,
      _currentValue2: S,
      _threadCount: 0,
      Provider: null,
      Consumer: null
    }, S.Provider = S, S.Consumer = {
      $$typeof: Se,
      _context: S
    }, S;
  }, $e.createElement = function(S, H, I) {
    var F, be = {}, Le = null;
    if (H != null)
      for (F in H.key !== void 0 && (Le = "" + H.key), H)
        Je.call(H, F) && F !== "key" && F !== "__self" && F !== "__source" && (be[F] = H[F]);
    var Oe = arguments.length - 2;
    if (Oe === 1) be.children = I;
    else if (1 < Oe) {
      for (var $t = Array(Oe), gt = 0; gt < Oe; gt++)
        $t[gt] = arguments[gt + 2];
      be.children = $t;
    }
    if (S && S.defaultProps)
      for (F in Oe = S.defaultProps, Oe)
        be[F] === void 0 && (be[F] = Oe[F]);
    return Me(S, Le, be);
  }, $e.createRef = function() {
    return { current: null };
  }, $e.forwardRef = function(S) {
    return { $$typeof: le, render: S };
  }, $e.isValidElement = Yt, $e.lazy = function(S) {
    return {
      $$typeof: Ne,
      _payload: { _status: -1, _result: S },
      _init: ee
    };
  }, $e.memo = function(S, H) {
    return {
      $$typeof: W,
      type: S,
      compare: H === void 0 ? null : H
    };
  }, $e.startTransition = function(S) {
    var H = Ae.T, I = {};
    Ae.T = I;
    try {
      var F = S(), be = Ae.S;
      be !== null && be(I, F), typeof F == "object" && F !== null && typeof F.then == "function" && F.then(Gt, ge);
    } catch (Le) {
      ge(Le);
    } finally {
      H !== null && I.types !== null && (H.types = I.types), Ae.T = H;
    }
  }, $e.unstable_useCacheRefresh = function() {
    return Ae.H.useCacheRefresh();
  }, $e.use = function(S) {
    return Ae.H.use(S);
  }, $e.useActionState = function(S, H, I) {
    return Ae.H.useActionState(S, H, I);
  }, $e.useCallback = function(S, H) {
    return Ae.H.useCallback(S, H);
  }, $e.useContext = function(S) {
    return Ae.H.useContext(S);
  }, $e.useDebugValue = function() {
  }, $e.useDeferredValue = function(S, H) {
    return Ae.H.useDeferredValue(S, H);
  }, $e.useEffect = function(S, H) {
    return Ae.H.useEffect(S, H);
  }, $e.useEffectEvent = function(S) {
    return Ae.H.useEffectEvent(S);
  }, $e.useId = function() {
    return Ae.H.useId();
  }, $e.useImperativeHandle = function(S, H, I) {
    return Ae.H.useImperativeHandle(S, H, I);
  }, $e.useInsertionEffect = function(S, H) {
    return Ae.H.useInsertionEffect(S, H);
  }, $e.useLayoutEffect = function(S, H) {
    return Ae.H.useLayoutEffect(S, H);
  }, $e.useMemo = function(S, H) {
    return Ae.H.useMemo(S, H);
  }, $e.useOptimistic = function(S, H) {
    return Ae.H.useOptimistic(S, H);
  }, $e.useReducer = function(S, H, I) {
    return Ae.H.useReducer(S, H, I);
  }, $e.useRef = function(S) {
    return Ae.H.useRef(S);
  }, $e.useState = function(S) {
    return Ae.H.useState(S);
  }, $e.useSyncExternalStore = function(S, H, I) {
    return Ae.H.useSyncExternalStore(
      S,
      H,
      I
    );
  }, $e.useTransition = function() {
    return Ae.H.useTransition();
  }, $e.version = "19.2.4", $e;
}
var Op = { exports: {} };
Op.exports;
var L2;
function _T() {
  return L2 || (L2 = 1, (function(Q, te) {
    process.env.NODE_ENV !== "production" && (function() {
      function Be(g, M) {
        Object.defineProperty(Se.prototype, g, {
          get: function() {
            console.warn(
              "%s(...) is deprecated in plain JavaScript React classes. %s",
              M[0],
              M[1]
            );
          }
        });
      }
      function U(g) {
        return g === null || typeof g != "object" ? null : (g = _c && g[_c] || g["@@iterator"], typeof g == "function" ? g : null);
      }
      function Re(g, M) {
        g = (g = g.constructor) && (g.displayName || g.name) || "ReactClass";
        var P = g + "." + M;
        Mc[P] || (console.error(
          "Can't call %s on a component that is not yet mounted. This is a no-op, but it might indicate a bug in your application. Instead, assign to `this.state` directly or define a `state = {};` class property with the desired state in the %s component.",
          M,
          g
        ), Mc[P] = !0);
      }
      function Se(g, M, P) {
        this.props = g, this.context = M, this.refs = vt, this.updater = P || Ga;
      }
      function mt() {
      }
      function le(g, M, P) {
        this.props = g, this.context = M, this.refs = vt, this.updater = P || Ga;
      }
      function ne() {
      }
      function W(g) {
        return "" + g;
      }
      function Ne(g) {
        try {
          W(g);
          var M = !1;
        } catch {
          M = !0;
        }
        if (M) {
          M = console;
          var P = M.error, ae = typeof Symbol == "function" && Symbol.toStringTag && g[Symbol.toStringTag] || g.constructor.name || "Object";
          return P.call(
            M,
            "The provided key is an unsupported type %s. This value must be coerced to a string before using it here.",
            ae
          ), W(g);
        }
      }
      function w(g) {
        if (g == null) return null;
        if (typeof g == "function")
          return g.$$typeof === hs ? null : g.displayName || g.name || null;
        if (typeof g == "string") return g;
        switch (g) {
          case S:
            return "Fragment";
          case I:
            return "Profiler";
          case H:
            return "StrictMode";
          case Oe:
            return "Suspense";
          case $t:
            return "SuspenseList";
          case oe:
            return "Activity";
        }
        if (typeof g == "object")
          switch (typeof g.tag == "number" && console.error(
            "Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."
          ), g.$$typeof) {
            case De:
              return "Portal";
            case be:
              return g.displayName || "Context";
            case F:
              return (g._context.displayName || "Context") + ".Consumer";
            case Le:
              var M = g.render;
              return g = g.displayName, g || (g = M.displayName || M.name || "", g = g !== "" ? "ForwardRef(" + g + ")" : "ForwardRef"), g;
            case gt:
              return M = g.displayName || null, M !== null ? M : w(g.type) || "Memo";
            case wa:
              M = g._payload, g = g._init;
              try {
                return w(g(M));
              } catch {
              }
          }
        return null;
      }
      function x(g) {
        if (g === S) return "<>";
        if (typeof g == "object" && g !== null && g.$$typeof === wa)
          return "<...>";
        try {
          var M = w(g);
          return M ? "<" + M + ">" : "<...>";
        } catch {
          return "<...>";
        }
      }
      function ce() {
        var g = de.A;
        return g === null ? null : g.getOwner();
      }
      function Ge() {
        return Error("react-stack-top-frame");
      }
      function it(g) {
        if (Cc.call(g, "key")) {
          var M = Object.getOwnPropertyDescriptor(g, "key").get;
          if (M && M.isReactWarning) return !1;
        }
        return g.key !== void 0;
      }
      function ut(g, M) {
        function P() {
          bi || (bi = !0, console.error(
            "%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)",
            M
          ));
        }
        P.isReactWarning = !0, Object.defineProperty(g, "key", {
          get: P,
          configurable: !0
        });
      }
      function Ze() {
        var g = w(this.type);
        return td[g] || (td[g] = !0, console.error(
          "Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release."
        )), g = this.props.ref, g !== void 0 ? g : null;
      }
      function qt(g, M, P, ae, he, Ce) {
        var me = P.ref;
        return g = {
          $$typeof: ge,
          type: g,
          key: M,
          props: P,
          _owner: ae
        }, (me !== void 0 ? me : null) !== null ? Object.defineProperty(g, "ref", {
          enumerable: !1,
          get: Ze
        }) : Object.defineProperty(g, "ref", { enumerable: !1, value: null }), g._store = {}, Object.defineProperty(g._store, "validated", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: 0
        }), Object.defineProperty(g, "_debugInfo", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: null
        }), Object.defineProperty(g, "_debugStack", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: he
        }), Object.defineProperty(g, "_debugTask", {
          configurable: !1,
          enumerable: !1,
          writable: !0,
          value: Ce
        }), Object.freeze && (Object.freeze(g.props), Object.freeze(g)), g;
      }
      function Ot(g, M) {
        return M = qt(
          g.type,
          M,
          g.props,
          g._owner,
          g._debugStack,
          g._debugTask
        ), g._store && (M._store.validated = g._store.validated), M;
      }
      function Ct(g) {
        wt(g) ? g._store && (g._store.validated = 1) : typeof g == "object" && g !== null && g.$$typeof === wa && (g._payload.status === "fulfilled" ? wt(g._payload.value) && g._payload.value._store && (g._payload.value._store.validated = 1) : g._store && (g._store.validated = 1));
      }
      function wt(g) {
        return typeof g == "object" && g !== null && g.$$typeof === ge;
      }
      function Gt(g) {
        var M = { "=": "=0", ":": "=2" };
        return "$" + g.replace(/[=:]/g, function(P) {
          return M[P];
        });
      }
      function Ae(g, M) {
        return typeof g == "object" && g !== null && g.key != null ? (Ne(g.key), Gt("" + g.key)) : M.toString(36);
      }
      function Je(g) {
        switch (g.status) {
          case "fulfilled":
            return g.value;
          case "rejected":
            throw g.reason;
          default:
            switch (typeof g.status == "string" ? g.then(ne, ne) : (g.status = "pending", g.then(
              function(M) {
                g.status === "pending" && (g.status = "fulfilled", g.value = M);
              },
              function(M) {
                g.status === "pending" && (g.status = "rejected", g.reason = M);
              }
            )), g.status) {
              case "fulfilled":
                return g.value;
              case "rejected":
                throw g.reason;
            }
        }
        throw g;
      }
      function Me(g, M, P, ae, he) {
        var Ce = typeof g;
        (Ce === "undefined" || Ce === "boolean") && (g = null);
        var me = !1;
        if (g === null) me = !0;
        else
          switch (Ce) {
            case "bigint":
            case "string":
            case "number":
              me = !0;
              break;
            case "object":
              switch (g.$$typeof) {
                case ge:
                case De:
                  me = !0;
                  break;
                case wa:
                  return me = g._init, Me(
                    me(g._payload),
                    M,
                    P,
                    ae,
                    he
                  );
              }
          }
        if (me) {
          me = g, he = he(me);
          var lt = ae === "" ? "." + Ae(me, 0) : ae;
          return Si(he) ? (P = "", lt != null && (P = lt.replace(ld, "$&/") + "/"), Me(he, M, P, "", function(la) {
            return la;
          })) : he != null && (wt(he) && (he.key != null && (me && me.key === he.key || Ne(he.key)), P = Ot(
            he,
            P + (he.key == null || me && me.key === he.key ? "" : ("" + he.key).replace(
              ld,
              "$&/"
            ) + "/") + lt
          ), ae !== "" && me != null && wt(me) && me.key == null && me._store && !me._store.validated && (P._store.validated = 2), he = P), M.push(he)), 1;
        }
        if (me = 0, lt = ae === "" ? "." : ae + ":", Si(g))
          for (var Qe = 0; Qe < g.length; Qe++)
            ae = g[Qe], Ce = lt + Ae(ae, Qe), me += Me(
              ae,
              M,
              P,
              Ce,
              he
            );
        else if (Qe = U(g), typeof Qe == "function")
          for (Qe === g.entries && (Un || console.warn(
            "Using Maps as children is not supported. Use an array of keyed ReactElements instead."
          ), Un = !0), g = Qe.call(g), Qe = 0; !(ae = g.next()).done; )
            ae = ae.value, Ce = lt + Ae(ae, Qe++), me += Me(
              ae,
              M,
              P,
              Ce,
              he
            );
        else if (Ce === "object") {
          if (typeof g.then == "function")
            return Me(
              Je(g),
              M,
              P,
              ae,
              he
            );
          throw M = String(g), Error(
            "Objects are not valid as a React child (found: " + (M === "[object Object]" ? "object with keys {" + Object.keys(g).join(", ") + "}" : M) + "). If you meant to render a collection of children, use an array instead."
          );
        }
        return me;
      }
      function se(g, M, P) {
        if (g == null) return g;
        var ae = [], he = 0;
        return Me(g, ae, "", "", function(Ce) {
          return M.call(P, Ce, he++);
        }), ae;
      }
      function Yt(g) {
        if (g._status === -1) {
          var M = g._ioInfo;
          M != null && (M.start = M.end = performance.now()), M = g._result;
          var P = M();
          if (P.then(
            function(he) {
              if (g._status === 0 || g._status === -1) {
                g._status = 1, g._result = he;
                var Ce = g._ioInfo;
                Ce != null && (Ce.end = performance.now()), P.status === void 0 && (P.status = "fulfilled", P.value = he);
              }
            },
            function(he) {
              if (g._status === 0 || g._status === -1) {
                g._status = 2, g._result = he;
                var Ce = g._ioInfo;
                Ce != null && (Ce.end = performance.now()), P.status === void 0 && (P.status = "rejected", P.reason = he);
              }
            }
          ), M = g._ioInfo, M != null) {
            M.value = P;
            var ae = P.displayName;
            typeof ae == "string" && (M.name = ae);
          }
          g._status === -1 && (g._status = 0, g._result = P);
        }
        if (g._status === 1)
          return M = g._result, M === void 0 && console.error(
            `lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like: 
  const MyComponent = lazy(() => import('./MyComponent'))

Did you accidentally put curly braces around the import?`,
            M
          ), "default" in M || console.error(
            `lazy: Expected the result of a dynamic import() call. Instead received: %s

Your code should look like: 
  const MyComponent = lazy(() => import('./MyComponent'))`,
            M
          ), M.default;
        throw g._result;
      }
      function pe() {
        var g = de.H;
        return g === null && console.error(
          `Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://react.dev/link/invalid-hook-call for tips about how to debug and fix this problem.`
        ), g;
      }
      function Xe() {
        de.asyncTransitions--;
      }
      function Kt(g) {
        if (Ei === null)
          try {
            var M = ("require" + Math.random()).slice(0, 7);
            Ei = (Q && Q[M]).call(
              Q,
              "timers"
            ).setImmediate;
          } catch {
            Ei = function(ae) {
              ms === !1 && (ms = !0, typeof MessageChannel > "u" && console.error(
                "This browser does not have a MessageChannel implementation, so enqueuing tasks via await act(async () => ...) will fail. Please file an issue at https://github.com/facebook/react/issues if you encounter this warning."
              ));
              var he = new MessageChannel();
              he.port1.onmessage = ae, he.port2.postMessage(void 0);
            };
          }
        return Ei(g);
      }
      function Xt(g) {
        return 1 < g.length && typeof AggregateError == "function" ? new AggregateError(g) : g[0];
      }
      function R(g, M) {
        M !== hn - 1 && console.error(
          "You seem to have overlapping act() calls, this is not supported. Be sure to await previous act() calls before making a new one. "
        ), hn = M;
      }
      function Z(g, M, P) {
        var ae = de.actQueue;
        if (ae !== null)
          if (ae.length !== 0)
            try {
              ee(ae), Kt(function() {
                return Z(g, M, P);
              });
              return;
            } catch (he) {
              de.thrownErrors.push(he);
            }
          else de.actQueue = null;
        0 < de.thrownErrors.length ? (ae = Xt(de.thrownErrors), de.thrownErrors.length = 0, P(ae)) : M(g);
      }
      function ee(g) {
        if (!Xa) {
          Xa = !0;
          var M = 0;
          try {
            for (; M < g.length; M++) {
              var P = g[M];
              do {
                de.didUsePromise = !1;
                var ae = P(!1);
                if (ae !== null) {
                  if (de.didUsePromise) {
                    g[M] = P, g.splice(0, M);
                    return;
                  }
                  P = ae;
                } else break;
              } while (!0);
            }
            g.length = 0;
          } catch (he) {
            g.splice(0, M + 1), de.thrownErrors.push(he);
          } finally {
            Xa = !1;
          }
        }
      }
      typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error());
      var ge = /* @__PURE__ */ Symbol.for("react.transitional.element"), De = /* @__PURE__ */ Symbol.for("react.portal"), S = /* @__PURE__ */ Symbol.for("react.fragment"), H = /* @__PURE__ */ Symbol.for("react.strict_mode"), I = /* @__PURE__ */ Symbol.for("react.profiler"), F = /* @__PURE__ */ Symbol.for("react.consumer"), be = /* @__PURE__ */ Symbol.for("react.context"), Le = /* @__PURE__ */ Symbol.for("react.forward_ref"), Oe = /* @__PURE__ */ Symbol.for("react.suspense"), $t = /* @__PURE__ */ Symbol.for("react.suspense_list"), gt = /* @__PURE__ */ Symbol.for("react.memo"), wa = /* @__PURE__ */ Symbol.for("react.lazy"), oe = /* @__PURE__ */ Symbol.for("react.activity"), _c = Symbol.iterator, Mc = {}, Ga = {
        isMounted: function() {
          return !1;
        },
        enqueueForceUpdate: function(g) {
          Re(g, "forceUpdate");
        },
        enqueueReplaceState: function(g) {
          Re(g, "replaceState");
        },
        enqueueSetState: function(g) {
          Re(g, "setState");
        }
      }, iu = Object.assign, vt = {};
      Object.freeze(vt), Se.prototype.isReactComponent = {}, Se.prototype.setState = function(g, M) {
        if (typeof g != "object" && typeof g != "function" && g != null)
          throw Error(
            "takes an object of state variables to update or a function which returns an object of state variables."
          );
        this.updater.enqueueSetState(this, g, M, "setState");
      }, Se.prototype.forceUpdate = function(g) {
        this.updater.enqueueForceUpdate(this, g, "forceUpdate");
      };
      var ta = {
        isMounted: [
          "isMounted",
          "Instead, make sure to clean up subscriptions and pending requests in componentWillUnmount to prevent memory leaks."
        ],
        replaceState: [
          "replaceState",
          "Refactor your code to use setState instead (see https://github.com/facebook/react/issues/3236)."
        ]
      };
      for (Uc in ta)
        ta.hasOwnProperty(Uc) && Be(Uc, ta[Uc]);
      mt.prototype = Se.prototype, ta = le.prototype = new mt(), ta.constructor = le, iu(ta, Se.prototype), ta.isPureReactComponent = !0;
      var Si = Array.isArray, hs = /* @__PURE__ */ Symbol.for("react.client.reference"), de = {
        H: null,
        A: null,
        T: null,
        S: null,
        actQueue: null,
        asyncTransitions: 0,
        isBatchingLegacy: !1,
        didScheduleLegacyUpdate: !1,
        didUsePromise: !1,
        thrownErrors: [],
        getCurrentStack: null,
        recentlyCreatedOwnerStacks: 0
      }, Cc = Object.prototype.hasOwnProperty, ou = console.createTask ? console.createTask : function() {
        return null;
      };
      ta = {
        react_stack_bottom_frame: function(g) {
          return g();
        }
      };
      var bi, bl, td = {}, Uo = ta.react_stack_bottom_frame.bind(
        ta,
        Ge
      )(), xo = ou(x(Ge)), Un = !1, ld = /\/+/g, No = typeof reportError == "function" ? reportError : function(g) {
        if (typeof window == "object" && typeof window.ErrorEvent == "function") {
          var M = new window.ErrorEvent("error", {
            bubbles: !0,
            cancelable: !0,
            message: typeof g == "object" && g !== null && typeof g.message == "string" ? String(g.message) : String(g),
            error: g
          });
          if (!window.dispatchEvent(M)) return;
        } else if (typeof process == "object" && typeof process.emit == "function") {
          process.emit("uncaughtException", g);
          return;
        }
        console.error(g);
      }, ms = !1, Ei = null, hn = 0, zl = !1, Xa = !1, Nl = typeof queueMicrotask == "function" ? function(g) {
        queueMicrotask(function() {
          return queueMicrotask(g);
        });
      } : Kt;
      ta = Object.freeze({
        __proto__: null,
        c: function(g) {
          return pe().useMemoCache(g);
        }
      });
      var Uc = {
        map: se,
        forEach: function(g, M, P) {
          se(
            g,
            function() {
              M.apply(this, arguments);
            },
            P
          );
        },
        count: function(g) {
          var M = 0;
          return se(g, function() {
            M++;
          }), M;
        },
        toArray: function(g) {
          return se(g, function(M) {
            return M;
          }) || [];
        },
        only: function(g) {
          if (!wt(g))
            throw Error(
              "React.Children.only expected to receive a single React element child."
            );
          return g;
        }
      };
      te.Activity = oe, te.Children = Uc, te.Component = Se, te.Fragment = S, te.Profiler = I, te.PureComponent = le, te.StrictMode = H, te.Suspense = Oe, te.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = de, te.__COMPILER_RUNTIME = ta, te.act = function(g) {
        var M = de.actQueue, P = hn;
        hn++;
        var ae = de.actQueue = M !== null ? M : [], he = !1;
        try {
          var Ce = g();
        } catch (Qe) {
          de.thrownErrors.push(Qe);
        }
        if (0 < de.thrownErrors.length)
          throw R(M, P), g = Xt(de.thrownErrors), de.thrownErrors.length = 0, g;
        if (Ce !== null && typeof Ce == "object" && typeof Ce.then == "function") {
          var me = Ce;
          return Nl(function() {
            he || zl || (zl = !0, console.error(
              "You called act(async () => ...) without await. This could lead to unexpected testing behaviour, interleaving multiple act calls and mixing their scopes. You should - await act(async () => ...);"
            ));
          }), {
            then: function(Qe, la) {
              he = !0, me.then(
                function(mn) {
                  if (R(M, P), P === 0) {
                    try {
                      ee(ae), Kt(function() {
                        return Z(
                          mn,
                          Qe,
                          la
                        );
                      });
                    } catch (Ho) {
                      de.thrownErrors.push(Ho);
                    }
                    if (0 < de.thrownErrors.length) {
                      var xc = Xt(
                        de.thrownErrors
                      );
                      de.thrownErrors.length = 0, la(xc);
                    }
                  } else Qe(mn);
                },
                function(mn) {
                  R(M, P), 0 < de.thrownErrors.length && (mn = Xt(
                    de.thrownErrors
                  ), de.thrownErrors.length = 0), la(mn);
                }
              );
            }
          };
        }
        var lt = Ce;
        if (R(M, P), P === 0 && (ee(ae), ae.length !== 0 && Nl(function() {
          he || zl || (zl = !0, console.error(
            "A component suspended inside an `act` scope, but the `act` call was not awaited. When testing React components that depend on asynchronous data, you must await the result:\n\nawait act(() => ...)"
          ));
        }), de.actQueue = null), 0 < de.thrownErrors.length)
          throw g = Xt(de.thrownErrors), de.thrownErrors.length = 0, g;
        return {
          then: function(Qe, la) {
            he = !0, P === 0 ? (de.actQueue = ae, Kt(function() {
              return Z(
                lt,
                Qe,
                la
              );
            })) : Qe(lt);
          }
        };
      }, te.cache = function(g) {
        return function() {
          return g.apply(null, arguments);
        };
      }, te.cacheSignal = function() {
        return null;
      }, te.captureOwnerStack = function() {
        var g = de.getCurrentStack;
        return g === null ? null : g();
      }, te.cloneElement = function(g, M, P) {
        if (g == null)
          throw Error(
            "The argument must be a React element, but you passed " + g + "."
          );
        var ae = iu({}, g.props), he = g.key, Ce = g._owner;
        if (M != null) {
          var me;
          e: {
            if (Cc.call(M, "ref") && (me = Object.getOwnPropertyDescriptor(
              M,
              "ref"
            ).get) && me.isReactWarning) {
              me = !1;
              break e;
            }
            me = M.ref !== void 0;
          }
          me && (Ce = ce()), it(M) && (Ne(M.key), he = "" + M.key);
          for (lt in M)
            !Cc.call(M, lt) || lt === "key" || lt === "__self" || lt === "__source" || lt === "ref" && M.ref === void 0 || (ae[lt] = M[lt]);
        }
        var lt = arguments.length - 2;
        if (lt === 1) ae.children = P;
        else if (1 < lt) {
          me = Array(lt);
          for (var Qe = 0; Qe < lt; Qe++)
            me[Qe] = arguments[Qe + 2];
          ae.children = me;
        }
        for (ae = qt(
          g.type,
          he,
          ae,
          Ce,
          g._debugStack,
          g._debugTask
        ), he = 2; he < arguments.length; he++)
          Ct(arguments[he]);
        return ae;
      }, te.createContext = function(g) {
        return g = {
          $$typeof: be,
          _currentValue: g,
          _currentValue2: g,
          _threadCount: 0,
          Provider: null,
          Consumer: null
        }, g.Provider = g, g.Consumer = {
          $$typeof: F,
          _context: g
        }, g._currentRenderer = null, g._currentRenderer2 = null, g;
      }, te.createElement = function(g, M, P) {
        for (var ae = 2; ae < arguments.length; ae++)
          Ct(arguments[ae]);
        ae = {};
        var he = null;
        if (M != null)
          for (Qe in bl || !("__self" in M) || "key" in M || (bl = !0, console.warn(
            "Your app (or one of its dependencies) is using an outdated JSX transform. Update to the modern JSX transform for faster performance: https://react.dev/link/new-jsx-transform"
          )), it(M) && (Ne(M.key), he = "" + M.key), M)
            Cc.call(M, Qe) && Qe !== "key" && Qe !== "__self" && Qe !== "__source" && (ae[Qe] = M[Qe]);
        var Ce = arguments.length - 2;
        if (Ce === 1) ae.children = P;
        else if (1 < Ce) {
          for (var me = Array(Ce), lt = 0; lt < Ce; lt++)
            me[lt] = arguments[lt + 2];
          Object.freeze && Object.freeze(me), ae.children = me;
        }
        if (g && g.defaultProps)
          for (Qe in Ce = g.defaultProps, Ce)
            ae[Qe] === void 0 && (ae[Qe] = Ce[Qe]);
        he && ut(
          ae,
          typeof g == "function" ? g.displayName || g.name || "Unknown" : g
        );
        var Qe = 1e4 > de.recentlyCreatedOwnerStacks++;
        return qt(
          g,
          he,
          ae,
          ce(),
          Qe ? Error("react-stack-top-frame") : Uo,
          Qe ? ou(x(g)) : xo
        );
      }, te.createRef = function() {
        var g = { current: null };
        return Object.seal(g), g;
      }, te.forwardRef = function(g) {
        g != null && g.$$typeof === gt ? console.error(
          "forwardRef requires a render function but received a `memo` component. Instead of forwardRef(memo(...)), use memo(forwardRef(...))."
        ) : typeof g != "function" ? console.error(
          "forwardRef requires a render function but was given %s.",
          g === null ? "null" : typeof g
        ) : g.length !== 0 && g.length !== 2 && console.error(
          "forwardRef render functions accept exactly two parameters: props and ref. %s",
          g.length === 1 ? "Did you forget to use the ref parameter?" : "Any additional parameter will be undefined."
        ), g != null && g.defaultProps != null && console.error(
          "forwardRef render functions do not support defaultProps. Did you accidentally pass a React component?"
        );
        var M = { $$typeof: Le, render: g }, P;
        return Object.defineProperty(M, "displayName", {
          enumerable: !1,
          configurable: !0,
          get: function() {
            return P;
          },
          set: function(ae) {
            P = ae, g.name || g.displayName || (Object.defineProperty(g, "name", { value: ae }), g.displayName = ae);
          }
        }), M;
      }, te.isValidElement = wt, te.lazy = function(g) {
        g = { _status: -1, _result: g };
        var M = {
          $$typeof: wa,
          _payload: g,
          _init: Yt
        }, P = {
          name: "lazy",
          start: -1,
          end: -1,
          value: null,
          owner: null,
          debugStack: Error("react-stack-top-frame"),
          debugTask: console.createTask ? console.createTask("lazy()") : null
        };
        return g._ioInfo = P, M._debugInfo = [{ awaited: P }], M;
      }, te.memo = function(g, M) {
        g == null && console.error(
          "memo: The first argument must be a component. Instead received: %s",
          g === null ? "null" : typeof g
        ), M = {
          $$typeof: gt,
          type: g,
          compare: M === void 0 ? null : M
        };
        var P;
        return Object.defineProperty(M, "displayName", {
          enumerable: !1,
          configurable: !0,
          get: function() {
            return P;
          },
          set: function(ae) {
            P = ae, g.name || g.displayName || (Object.defineProperty(g, "name", { value: ae }), g.displayName = ae);
          }
        }), M;
      }, te.startTransition = function(g) {
        var M = de.T, P = {};
        P._updatedFibers = /* @__PURE__ */ new Set(), de.T = P;
        try {
          var ae = g(), he = de.S;
          he !== null && he(P, ae), typeof ae == "object" && ae !== null && typeof ae.then == "function" && (de.asyncTransitions++, ae.then(Xe, Xe), ae.then(ne, No));
        } catch (Ce) {
          No(Ce);
        } finally {
          M === null && P._updatedFibers && (g = P._updatedFibers.size, P._updatedFibers.clear(), 10 < g && console.warn(
            "Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."
          )), M !== null && P.types !== null && (M.types !== null && M.types !== P.types && console.error(
            "We expected inner Transitions to have transferred the outer types set and that you cannot add to the outer Transition while inside the inner.This is a bug in React."
          ), M.types = P.types), de.T = M;
        }
      }, te.unstable_useCacheRefresh = function() {
        return pe().useCacheRefresh();
      }, te.use = function(g) {
        return pe().use(g);
      }, te.useActionState = function(g, M, P) {
        return pe().useActionState(
          g,
          M,
          P
        );
      }, te.useCallback = function(g, M) {
        return pe().useCallback(g, M);
      }, te.useContext = function(g) {
        var M = pe();
        return g.$$typeof === F && console.error(
          "Calling useContext(Context.Consumer) is not supported and will cause bugs. Did you mean to call useContext(Context) instead?"
        ), M.useContext(g);
      }, te.useDebugValue = function(g, M) {
        return pe().useDebugValue(g, M);
      }, te.useDeferredValue = function(g, M) {
        return pe().useDeferredValue(g, M);
      }, te.useEffect = function(g, M) {
        return g == null && console.warn(
          "React Hook useEffect requires an effect callback. Did you forget to pass a callback to the hook?"
        ), pe().useEffect(g, M);
      }, te.useEffectEvent = function(g) {
        return pe().useEffectEvent(g);
      }, te.useId = function() {
        return pe().useId();
      }, te.useImperativeHandle = function(g, M, P) {
        return pe().useImperativeHandle(g, M, P);
      }, te.useInsertionEffect = function(g, M) {
        return g == null && console.warn(
          "React Hook useInsertionEffect requires an effect callback. Did you forget to pass a callback to the hook?"
        ), pe().useInsertionEffect(g, M);
      }, te.useLayoutEffect = function(g, M) {
        return g == null && console.warn(
          "React Hook useLayoutEffect requires an effect callback. Did you forget to pass a callback to the hook?"
        ), pe().useLayoutEffect(g, M);
      }, te.useMemo = function(g, M) {
        return pe().useMemo(g, M);
      }, te.useOptimistic = function(g, M) {
        return pe().useOptimistic(g, M);
      }, te.useReducer = function(g, M, P) {
        return pe().useReducer(g, M, P);
      }, te.useRef = function(g) {
        return pe().useRef(g);
      }, te.useState = function(g) {
        return pe().useState(g);
      }, te.useSyncExternalStore = function(g, M, P) {
        return pe().useSyncExternalStore(
          g,
          M,
          P
        );
      }, te.useTransition = function() {
        return pe().useTransition();
      }, te.version = "19.2.4", typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
    })();
  })(Op, Op.exports)), Op.exports;
}
var Q2;
function Om() {
  return Q2 || (Q2 = 1, process.env.NODE_ENV === "production" ? Kv.exports = RT() : Kv.exports = _T()), Kv.exports;
}
var V2;
function MT() {
  return V2 || (V2 = 1, process.env.NODE_ENV !== "production" && (function() {
    function Q(S) {
      if (S == null) return null;
      if (typeof S == "function")
        return S.$$typeof === Yt ? null : S.displayName || S.name || null;
      if (typeof S == "string") return S;
      switch (S) {
        case ut:
          return "Fragment";
        case qt:
          return "Profiler";
        case Ze:
          return "StrictMode";
        case Gt:
          return "Suspense";
        case Ae:
          return "SuspenseList";
        case se:
          return "Activity";
      }
      if (typeof S == "object")
        switch (typeof S.tag == "number" && console.error(
          "Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."
        ), S.$$typeof) {
          case it:
            return "Portal";
          case Ct:
            return S.displayName || "Context";
          case Ot:
            return (S._context.displayName || "Context") + ".Consumer";
          case wt:
            var H = S.render;
            return S = S.displayName, S || (S = H.displayName || H.name || "", S = S !== "" ? "ForwardRef(" + S + ")" : "ForwardRef"), S;
          case Je:
            return H = S.displayName || null, H !== null ? H : Q(S.type) || "Memo";
          case Me:
            H = S._payload, S = S._init;
            try {
              return Q(S(H));
            } catch {
            }
        }
      return null;
    }
    function te(S) {
      return "" + S;
    }
    function Be(S) {
      try {
        te(S);
        var H = !1;
      } catch {
        H = !0;
      }
      if (H) {
        H = console;
        var I = H.error, F = typeof Symbol == "function" && Symbol.toStringTag && S[Symbol.toStringTag] || S.constructor.name || "Object";
        return I.call(
          H,
          "The provided key is an unsupported type %s. This value must be coerced to a string before using it here.",
          F
        ), te(S);
      }
    }
    function U(S) {
      if (S === ut) return "<>";
      if (typeof S == "object" && S !== null && S.$$typeof === Me)
        return "<...>";
      try {
        var H = Q(S);
        return H ? "<" + H + ">" : "<...>";
      } catch {
        return "<...>";
      }
    }
    function Re() {
      var S = pe.A;
      return S === null ? null : S.getOwner();
    }
    function Se() {
      return Error("react-stack-top-frame");
    }
    function mt(S) {
      if (Xe.call(S, "key")) {
        var H = Object.getOwnPropertyDescriptor(S, "key").get;
        if (H && H.isReactWarning) return !1;
      }
      return S.key !== void 0;
    }
    function le(S, H) {
      function I() {
        R || (R = !0, console.error(
          "%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)",
          H
        ));
      }
      I.isReactWarning = !0, Object.defineProperty(S, "key", {
        get: I,
        configurable: !0
      });
    }
    function ne() {
      var S = Q(this.type);
      return Z[S] || (Z[S] = !0, console.error(
        "Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release."
      )), S = this.props.ref, S !== void 0 ? S : null;
    }
    function W(S, H, I, F, be, Le) {
      var Oe = I.ref;
      return S = {
        $$typeof: Ge,
        type: S,
        key: H,
        props: I,
        _owner: F
      }, (Oe !== void 0 ? Oe : null) !== null ? Object.defineProperty(S, "ref", {
        enumerable: !1,
        get: ne
      }) : Object.defineProperty(S, "ref", { enumerable: !1, value: null }), S._store = {}, Object.defineProperty(S._store, "validated", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: 0
      }), Object.defineProperty(S, "_debugInfo", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: null
      }), Object.defineProperty(S, "_debugStack", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: be
      }), Object.defineProperty(S, "_debugTask", {
        configurable: !1,
        enumerable: !1,
        writable: !0,
        value: Le
      }), Object.freeze && (Object.freeze(S.props), Object.freeze(S)), S;
    }
    function Ne(S, H, I, F, be, Le) {
      var Oe = H.children;
      if (Oe !== void 0)
        if (F)
          if (Kt(Oe)) {
            for (F = 0; F < Oe.length; F++)
              w(Oe[F]);
            Object.freeze && Object.freeze(Oe);
          } else
            console.error(
              "React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead."
            );
        else w(Oe);
      if (Xe.call(H, "key")) {
        Oe = Q(S);
        var $t = Object.keys(H).filter(function(wa) {
          return wa !== "key";
        });
        F = 0 < $t.length ? "{key: someKey, " + $t.join(": ..., ") + ": ...}" : "{key: someKey}", De[Oe + F] || ($t = 0 < $t.length ? "{" + $t.join(": ..., ") + ": ...}" : "{}", console.error(
          `A props object containing a "key" prop is being spread into JSX:
  let props = %s;
  <%s {...props} />
React keys must be passed directly to JSX without using spread:
  let props = %s;
  <%s key={someKey} {...props} />`,
          F,
          Oe,
          $t,
          Oe
        ), De[Oe + F] = !0);
      }
      if (Oe = null, I !== void 0 && (Be(I), Oe = "" + I), mt(H) && (Be(H.key), Oe = "" + H.key), "key" in H) {
        I = {};
        for (var gt in H)
          gt !== "key" && (I[gt] = H[gt]);
      } else I = H;
      return Oe && le(
        I,
        typeof S == "function" ? S.displayName || S.name || "Unknown" : S
      ), W(
        S,
        Oe,
        I,
        Re(),
        be,
        Le
      );
    }
    function w(S) {
      x(S) ? S._store && (S._store.validated = 1) : typeof S == "object" && S !== null && S.$$typeof === Me && (S._payload.status === "fulfilled" ? x(S._payload.value) && S._payload.value._store && (S._payload.value._store.validated = 1) : S._store && (S._store.validated = 1));
    }
    function x(S) {
      return typeof S == "object" && S !== null && S.$$typeof === Ge;
    }
    var ce = Om(), Ge = /* @__PURE__ */ Symbol.for("react.transitional.element"), it = /* @__PURE__ */ Symbol.for("react.portal"), ut = /* @__PURE__ */ Symbol.for("react.fragment"), Ze = /* @__PURE__ */ Symbol.for("react.strict_mode"), qt = /* @__PURE__ */ Symbol.for("react.profiler"), Ot = /* @__PURE__ */ Symbol.for("react.consumer"), Ct = /* @__PURE__ */ Symbol.for("react.context"), wt = /* @__PURE__ */ Symbol.for("react.forward_ref"), Gt = /* @__PURE__ */ Symbol.for("react.suspense"), Ae = /* @__PURE__ */ Symbol.for("react.suspense_list"), Je = /* @__PURE__ */ Symbol.for("react.memo"), Me = /* @__PURE__ */ Symbol.for("react.lazy"), se = /* @__PURE__ */ Symbol.for("react.activity"), Yt = /* @__PURE__ */ Symbol.for("react.client.reference"), pe = ce.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, Xe = Object.prototype.hasOwnProperty, Kt = Array.isArray, Xt = console.createTask ? console.createTask : function() {
      return null;
    };
    ce = {
      react_stack_bottom_frame: function(S) {
        return S();
      }
    };
    var R, Z = {}, ee = ce.react_stack_bottom_frame.bind(
      ce,
      Se
    )(), ge = Xt(U(Se)), De = {};
    Ep.Fragment = ut, Ep.jsx = function(S, H, I) {
      var F = 1e4 > pe.recentlyCreatedOwnerStacks++;
      return Ne(
        S,
        H,
        I,
        !1,
        F ? Error("react-stack-top-frame") : ee,
        F ? Xt(U(S)) : ge
      );
    }, Ep.jsxs = function(S, H, I) {
      var F = 1e4 > pe.recentlyCreatedOwnerStacks++;
      return Ne(
        S,
        H,
        I,
        !0,
        F ? Error("react-stack-top-frame") : ee,
        F ? Xt(U(S)) : ge
      );
    };
  })()), Ep;
}
var Z2;
function CT() {
  return Z2 || (Z2 = 1, process.env.NODE_ENV === "production" ? Jv.exports = DT() : Jv.exports = MT()), Jv.exports;
}
var L = CT(), ds = Om();
const UT = /* @__PURE__ */ tE(ds);
var $v = { exports: {} }, Tp = {}, kv = { exports: {} }, OS = {};
var J2;
function xT() {
  return J2 || (J2 = 1, (function(Q) {
    function te(R, Z) {
      var ee = R.length;
      R.push(Z);
      e: for (; 0 < ee; ) {
        var ge = ee - 1 >>> 1, De = R[ge];
        if (0 < Re(De, Z))
          R[ge] = Z, R[ee] = De, ee = ge;
        else break e;
      }
    }
    function Be(R) {
      return R.length === 0 ? null : R[0];
    }
    function U(R) {
      if (R.length === 0) return null;
      var Z = R[0], ee = R.pop();
      if (ee !== Z) {
        R[0] = ee;
        e: for (var ge = 0, De = R.length, S = De >>> 1; ge < S; ) {
          var H = 2 * (ge + 1) - 1, I = R[H], F = H + 1, be = R[F];
          if (0 > Re(I, ee))
            F < De && 0 > Re(be, I) ? (R[ge] = be, R[F] = ee, ge = F) : (R[ge] = I, R[H] = ee, ge = H);
          else if (F < De && 0 > Re(be, ee))
            R[ge] = be, R[F] = ee, ge = F;
          else break e;
        }
      }
      return Z;
    }
    function Re(R, Z) {
      var ee = R.sortIndex - Z.sortIndex;
      return ee !== 0 ? ee : R.id - Z.id;
    }
    if (Q.unstable_now = void 0, typeof performance == "object" && typeof performance.now == "function") {
      var Se = performance;
      Q.unstable_now = function() {
        return Se.now();
      };
    } else {
      var mt = Date, le = mt.now();
      Q.unstable_now = function() {
        return mt.now() - le;
      };
    }
    var ne = [], W = [], Ne = 1, w = null, x = 3, ce = !1, Ge = !1, it = !1, ut = !1, Ze = typeof setTimeout == "function" ? setTimeout : null, qt = typeof clearTimeout == "function" ? clearTimeout : null, Ot = typeof setImmediate < "u" ? setImmediate : null;
    function Ct(R) {
      for (var Z = Be(W); Z !== null; ) {
        if (Z.callback === null) U(W);
        else if (Z.startTime <= R)
          U(W), Z.sortIndex = Z.expirationTime, te(ne, Z);
        else break;
        Z = Be(W);
      }
    }
    function wt(R) {
      if (it = !1, Ct(R), !Ge)
        if (Be(ne) !== null)
          Ge = !0, Gt || (Gt = !0, pe());
        else {
          var Z = Be(W);
          Z !== null && Xt(wt, Z.startTime - R);
        }
    }
    var Gt = !1, Ae = -1, Je = 5, Me = -1;
    function se() {
      return ut ? !0 : !(Q.unstable_now() - Me < Je);
    }
    function Yt() {
      if (ut = !1, Gt) {
        var R = Q.unstable_now();
        Me = R;
        var Z = !0;
        try {
          e: {
            Ge = !1, it && (it = !1, qt(Ae), Ae = -1), ce = !0;
            var ee = x;
            try {
              t: {
                for (Ct(R), w = Be(ne); w !== null && !(w.expirationTime > R && se()); ) {
                  var ge = w.callback;
                  if (typeof ge == "function") {
                    w.callback = null, x = w.priorityLevel;
                    var De = ge(
                      w.expirationTime <= R
                    );
                    if (R = Q.unstable_now(), typeof De == "function") {
                      w.callback = De, Ct(R), Z = !0;
                      break t;
                    }
                    w === Be(ne) && U(ne), Ct(R);
                  } else U(ne);
                  w = Be(ne);
                }
                if (w !== null) Z = !0;
                else {
                  var S = Be(W);
                  S !== null && Xt(
                    wt,
                    S.startTime - R
                  ), Z = !1;
                }
              }
              break e;
            } finally {
              w = null, x = ee, ce = !1;
            }
            Z = void 0;
          }
        } finally {
          Z ? pe() : Gt = !1;
        }
      }
    }
    var pe;
    if (typeof Ot == "function")
      pe = function() {
        Ot(Yt);
      };
    else if (typeof MessageChannel < "u") {
      var Xe = new MessageChannel(), Kt = Xe.port2;
      Xe.port1.onmessage = Yt, pe = function() {
        Kt.postMessage(null);
      };
    } else
      pe = function() {
        Ze(Yt, 0);
      };
    function Xt(R, Z) {
      Ae = Ze(function() {
        R(Q.unstable_now());
      }, Z);
    }
    Q.unstable_IdlePriority = 5, Q.unstable_ImmediatePriority = 1, Q.unstable_LowPriority = 4, Q.unstable_NormalPriority = 3, Q.unstable_Profiling = null, Q.unstable_UserBlockingPriority = 2, Q.unstable_cancelCallback = function(R) {
      R.callback = null;
    }, Q.unstable_forceFrameRate = function(R) {
      0 > R || 125 < R ? console.error(
        "forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"
      ) : Je = 0 < R ? Math.floor(1e3 / R) : 5;
    }, Q.unstable_getCurrentPriorityLevel = function() {
      return x;
    }, Q.unstable_next = function(R) {
      switch (x) {
        case 1:
        case 2:
        case 3:
          var Z = 3;
          break;
        default:
          Z = x;
      }
      var ee = x;
      x = Z;
      try {
        return R();
      } finally {
        x = ee;
      }
    }, Q.unstable_requestPaint = function() {
      ut = !0;
    }, Q.unstable_runWithPriority = function(R, Z) {
      switch (R) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          R = 3;
      }
      var ee = x;
      x = R;
      try {
        return Z();
      } finally {
        x = ee;
      }
    }, Q.unstable_scheduleCallback = function(R, Z, ee) {
      var ge = Q.unstable_now();
      switch (typeof ee == "object" && ee !== null ? (ee = ee.delay, ee = typeof ee == "number" && 0 < ee ? ge + ee : ge) : ee = ge, R) {
        case 1:
          var De = -1;
          break;
        case 2:
          De = 250;
          break;
        case 5:
          De = 1073741823;
          break;
        case 4:
          De = 1e4;
          break;
        default:
          De = 5e3;
      }
      return De = ee + De, R = {
        id: Ne++,
        callback: Z,
        priorityLevel: R,
        startTime: ee,
        expirationTime: De,
        sortIndex: -1
      }, ee > ge ? (R.sortIndex = ee, te(W, R), Be(ne) === null && R === Be(W) && (it ? (qt(Ae), Ae = -1) : it = !0, Xt(wt, ee - ge))) : (R.sortIndex = De, te(ne, R), Ge || ce || (Ge = !0, Gt || (Gt = !0, pe()))), R;
    }, Q.unstable_shouldYield = se, Q.unstable_wrapCallback = function(R) {
      var Z = x;
      return function() {
        var ee = x;
        x = Z;
        try {
          return R.apply(this, arguments);
        } finally {
          x = ee;
        }
      };
    };
  })(OS)), OS;
}
var zS = {};
var K2;
function NT() {
  return K2 || (K2 = 1, (function(Q) {
    process.env.NODE_ENV !== "production" && (function() {
      function te() {
        if (wt = !1, Me) {
          var R = Q.unstable_now();
          pe = R;
          var Z = !0;
          try {
            e: {
              Ot = !1, Ct && (Ct = !1, Ae(se), se = -1), qt = !0;
              var ee = Ze;
              try {
                t: {
                  for (mt(R), ut = U(ce); ut !== null && !(ut.expirationTime > R && ne()); ) {
                    var ge = ut.callback;
                    if (typeof ge == "function") {
                      ut.callback = null, Ze = ut.priorityLevel;
                      var De = ge(
                        ut.expirationTime <= R
                      );
                      if (R = Q.unstable_now(), typeof De == "function") {
                        ut.callback = De, mt(R), Z = !0;
                        break t;
                      }
                      ut === U(ce) && Re(ce), mt(R);
                    } else Re(ce);
                    ut = U(ce);
                  }
                  if (ut !== null) Z = !0;
                  else {
                    var S = U(Ge);
                    S !== null && W(
                      le,
                      S.startTime - R
                    ), Z = !1;
                  }
                }
                break e;
              } finally {
                ut = null, Ze = ee, qt = !1;
              }
              Z = void 0;
            }
          } finally {
            Z ? Xe() : Me = !1;
          }
        }
      }
      function Be(R, Z) {
        var ee = R.length;
        R.push(Z);
        e: for (; 0 < ee; ) {
          var ge = ee - 1 >>> 1, De = R[ge];
          if (0 < Se(De, Z))
            R[ge] = Z, R[ee] = De, ee = ge;
          else break e;
        }
      }
      function U(R) {
        return R.length === 0 ? null : R[0];
      }
      function Re(R) {
        if (R.length === 0) return null;
        var Z = R[0], ee = R.pop();
        if (ee !== Z) {
          R[0] = ee;
          e: for (var ge = 0, De = R.length, S = De >>> 1; ge < S; ) {
            var H = 2 * (ge + 1) - 1, I = R[H], F = H + 1, be = R[F];
            if (0 > Se(I, ee))
              F < De && 0 > Se(be, I) ? (R[ge] = be, R[F] = ee, ge = F) : (R[ge] = I, R[H] = ee, ge = H);
            else if (F < De && 0 > Se(be, ee))
              R[ge] = be, R[F] = ee, ge = F;
            else break e;
          }
        }
        return Z;
      }
      function Se(R, Z) {
        var ee = R.sortIndex - Z.sortIndex;
        return ee !== 0 ? ee : R.id - Z.id;
      }
      function mt(R) {
        for (var Z = U(Ge); Z !== null; ) {
          if (Z.callback === null) Re(Ge);
          else if (Z.startTime <= R)
            Re(Ge), Z.sortIndex = Z.expirationTime, Be(ce, Z);
          else break;
          Z = U(Ge);
        }
      }
      function le(R) {
        if (Ct = !1, mt(R), !Ot)
          if (U(ce) !== null)
            Ot = !0, Me || (Me = !0, Xe());
          else {
            var Z = U(Ge);
            Z !== null && W(
              le,
              Z.startTime - R
            );
          }
      }
      function ne() {
        return wt ? !0 : !(Q.unstable_now() - pe < Yt);
      }
      function W(R, Z) {
        se = Gt(function() {
          R(Q.unstable_now());
        }, Z);
      }
      if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error()), Q.unstable_now = void 0, typeof performance == "object" && typeof performance.now == "function") {
        var Ne = performance;
        Q.unstable_now = function() {
          return Ne.now();
        };
      } else {
        var w = Date, x = w.now();
        Q.unstable_now = function() {
          return w.now() - x;
        };
      }
      var ce = [], Ge = [], it = 1, ut = null, Ze = 3, qt = !1, Ot = !1, Ct = !1, wt = !1, Gt = typeof setTimeout == "function" ? setTimeout : null, Ae = typeof clearTimeout == "function" ? clearTimeout : null, Je = typeof setImmediate < "u" ? setImmediate : null, Me = !1, se = -1, Yt = 5, pe = -1;
      if (typeof Je == "function")
        var Xe = function() {
          Je(te);
        };
      else if (typeof MessageChannel < "u") {
        var Kt = new MessageChannel(), Xt = Kt.port2;
        Kt.port1.onmessage = te, Xe = function() {
          Xt.postMessage(null);
        };
      } else
        Xe = function() {
          Gt(te, 0);
        };
      Q.unstable_IdlePriority = 5, Q.unstable_ImmediatePriority = 1, Q.unstable_LowPriority = 4, Q.unstable_NormalPriority = 3, Q.unstable_Profiling = null, Q.unstable_UserBlockingPriority = 2, Q.unstable_cancelCallback = function(R) {
        R.callback = null;
      }, Q.unstable_forceFrameRate = function(R) {
        0 > R || 125 < R ? console.error(
          "forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"
        ) : Yt = 0 < R ? Math.floor(1e3 / R) : 5;
      }, Q.unstable_getCurrentPriorityLevel = function() {
        return Ze;
      }, Q.unstable_next = function(R) {
        switch (Ze) {
          case 1:
          case 2:
          case 3:
            var Z = 3;
            break;
          default:
            Z = Ze;
        }
        var ee = Ze;
        Ze = Z;
        try {
          return R();
        } finally {
          Ze = ee;
        }
      }, Q.unstable_requestPaint = function() {
        wt = !0;
      }, Q.unstable_runWithPriority = function(R, Z) {
        switch (R) {
          case 1:
          case 2:
          case 3:
          case 4:
          case 5:
            break;
          default:
            R = 3;
        }
        var ee = Ze;
        Ze = R;
        try {
          return Z();
        } finally {
          Ze = ee;
        }
      }, Q.unstable_scheduleCallback = function(R, Z, ee) {
        var ge = Q.unstable_now();
        switch (typeof ee == "object" && ee !== null ? (ee = ee.delay, ee = typeof ee == "number" && 0 < ee ? ge + ee : ge) : ee = ge, R) {
          case 1:
            var De = -1;
            break;
          case 2:
            De = 250;
            break;
          case 5:
            De = 1073741823;
            break;
          case 4:
            De = 1e4;
            break;
          default:
            De = 5e3;
        }
        return De = ee + De, R = {
          id: it++,
          callback: Z,
          priorityLevel: R,
          startTime: ee,
          expirationTime: De,
          sortIndex: -1
        }, ee > ge ? (R.sortIndex = ee, Be(Ge, R), U(ce) === null && R === U(Ge) && (Ct ? (Ae(se), se = -1) : Ct = !0, W(le, ee - ge))) : (R.sortIndex = De, Be(ce, R), Ot || qt || (Ot = !0, Me || (Me = !0, Xe()))), R;
      }, Q.unstable_shouldYield = ne, Q.unstable_wrapCallback = function(R) {
        var Z = Ze;
        return function() {
          var ee = Ze;
          Ze = Z;
          try {
            return R.apply(this, arguments);
          } finally {
            Ze = ee;
          }
        };
      }, typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
    })();
  })(zS)), zS;
}
var $2;
function lE() {
  return $2 || ($2 = 1, process.env.NODE_ENV === "production" ? kv.exports = xT() : kv.exports = NT()), kv.exports;
}
var Wv = { exports: {} }, Ya = {};
var k2;
function HT() {
  if (k2) return Ya;
  k2 = 1;
  var Q = Om();
  function te(ne) {
    var W = "https://react.dev/errors/" + ne;
    if (1 < arguments.length) {
      W += "?args[]=" + encodeURIComponent(arguments[1]);
      for (var Ne = 2; Ne < arguments.length; Ne++)
        W += "&args[]=" + encodeURIComponent(arguments[Ne]);
    }
    return "Minified React error #" + ne + "; visit " + W + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  function Be() {
  }
  var U = {
    d: {
      f: Be,
      r: function() {
        throw Error(te(522));
      },
      D: Be,
      C: Be,
      L: Be,
      m: Be,
      X: Be,
      S: Be,
      M: Be
    },
    p: 0,
    findDOMNode: null
  }, Re = /* @__PURE__ */ Symbol.for("react.portal");
  function Se(ne, W, Ne) {
    var w = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return {
      $$typeof: Re,
      key: w == null ? null : "" + w,
      children: ne,
      containerInfo: W,
      implementation: Ne
    };
  }
  var mt = Q.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
  function le(ne, W) {
    if (ne === "font") return "";
    if (typeof W == "string")
      return W === "use-credentials" ? W : "";
  }
  return Ya.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = U, Ya.createPortal = function(ne, W) {
    var Ne = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!W || W.nodeType !== 1 && W.nodeType !== 9 && W.nodeType !== 11)
      throw Error(te(299));
    return Se(ne, W, null, Ne);
  }, Ya.flushSync = function(ne) {
    var W = mt.T, Ne = U.p;
    try {
      if (mt.T = null, U.p = 2, ne) return ne();
    } finally {
      mt.T = W, U.p = Ne, U.d.f();
    }
  }, Ya.preconnect = function(ne, W) {
    typeof ne == "string" && (W ? (W = W.crossOrigin, W = typeof W == "string" ? W === "use-credentials" ? W : "" : void 0) : W = null, U.d.C(ne, W));
  }, Ya.prefetchDNS = function(ne) {
    typeof ne == "string" && U.d.D(ne);
  }, Ya.preinit = function(ne, W) {
    if (typeof ne == "string" && W && typeof W.as == "string") {
      var Ne = W.as, w = le(Ne, W.crossOrigin), x = typeof W.integrity == "string" ? W.integrity : void 0, ce = typeof W.fetchPriority == "string" ? W.fetchPriority : void 0;
      Ne === "style" ? U.d.S(
        ne,
        typeof W.precedence == "string" ? W.precedence : void 0,
        {
          crossOrigin: w,
          integrity: x,
          fetchPriority: ce
        }
      ) : Ne === "script" && U.d.X(ne, {
        crossOrigin: w,
        integrity: x,
        fetchPriority: ce,
        nonce: typeof W.nonce == "string" ? W.nonce : void 0
      });
    }
  }, Ya.preinitModule = function(ne, W) {
    if (typeof ne == "string")
      if (typeof W == "object" && W !== null) {
        if (W.as == null || W.as === "script") {
          var Ne = le(
            W.as,
            W.crossOrigin
          );
          U.d.M(ne, {
            crossOrigin: Ne,
            integrity: typeof W.integrity == "string" ? W.integrity : void 0,
            nonce: typeof W.nonce == "string" ? W.nonce : void 0
          });
        }
      } else W == null && U.d.M(ne);
  }, Ya.preload = function(ne, W) {
    if (typeof ne == "string" && typeof W == "object" && W !== null && typeof W.as == "string") {
      var Ne = W.as, w = le(Ne, W.crossOrigin);
      U.d.L(ne, Ne, {
        crossOrigin: w,
        integrity: typeof W.integrity == "string" ? W.integrity : void 0,
        nonce: typeof W.nonce == "string" ? W.nonce : void 0,
        type: typeof W.type == "string" ? W.type : void 0,
        fetchPriority: typeof W.fetchPriority == "string" ? W.fetchPriority : void 0,
        referrerPolicy: typeof W.referrerPolicy == "string" ? W.referrerPolicy : void 0,
        imageSrcSet: typeof W.imageSrcSet == "string" ? W.imageSrcSet : void 0,
        imageSizes: typeof W.imageSizes == "string" ? W.imageSizes : void 0,
        media: typeof W.media == "string" ? W.media : void 0
      });
    }
  }, Ya.preloadModule = function(ne, W) {
    if (typeof ne == "string")
      if (W) {
        var Ne = le(W.as, W.crossOrigin);
        U.d.m(ne, {
          as: typeof W.as == "string" && W.as !== "script" ? W.as : void 0,
          crossOrigin: Ne,
          integrity: typeof W.integrity == "string" ? W.integrity : void 0
        });
      } else U.d.m(ne);
  }, Ya.requestFormReset = function(ne) {
    U.d.r(ne);
  }, Ya.unstable_batchedUpdates = function(ne, W) {
    return ne(W);
  }, Ya.useFormState = function(ne, W, Ne) {
    return mt.H.useFormState(ne, W, Ne);
  }, Ya.useFormStatus = function() {
    return mt.H.useHostTransitionStatus();
  }, Ya.version = "19.2.4", Ya;
}
var qa = {};
var W2;
function jT() {
  return W2 || (W2 = 1, process.env.NODE_ENV !== "production" && (function() {
    function Q() {
    }
    function te(w) {
      return "" + w;
    }
    function Be(w, x, ce) {
      var Ge = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
      try {
        te(Ge);
        var it = !1;
      } catch {
        it = !0;
      }
      return it && (console.error(
        "The provided key is an unsupported type %s. This value must be coerced to a string before using it here.",
        typeof Symbol == "function" && Symbol.toStringTag && Ge[Symbol.toStringTag] || Ge.constructor.name || "Object"
      ), te(Ge)), {
        $$typeof: W,
        key: Ge == null ? null : "" + Ge,
        children: w,
        containerInfo: x,
        implementation: ce
      };
    }
    function U(w, x) {
      if (w === "font") return "";
      if (typeof x == "string")
        return x === "use-credentials" ? x : "";
    }
    function Re(w) {
      return w === null ? "`null`" : w === void 0 ? "`undefined`" : w === "" ? "an empty string" : 'something with type "' + typeof w + '"';
    }
    function Se(w) {
      return w === null ? "`null`" : w === void 0 ? "`undefined`" : w === "" ? "an empty string" : typeof w == "string" ? JSON.stringify(w) : typeof w == "number" ? "`" + w + "`" : 'something with type "' + typeof w + '"';
    }
    function mt() {
      var w = Ne.H;
      return w === null && console.error(
        `Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://react.dev/link/invalid-hook-call for tips about how to debug and fix this problem.`
      ), w;
    }
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error());
    var le = Om(), ne = {
      d: {
        f: Q,
        r: function() {
          throw Error(
            "Invalid form element. requestFormReset must be passed a form that was rendered by React."
          );
        },
        D: Q,
        C: Q,
        L: Q,
        m: Q,
        X: Q,
        S: Q,
        M: Q
      },
      p: 0,
      findDOMNode: null
    }, W = /* @__PURE__ */ Symbol.for("react.portal"), Ne = le.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
    typeof Map == "function" && Map.prototype != null && typeof Map.prototype.forEach == "function" && typeof Set == "function" && Set.prototype != null && typeof Set.prototype.clear == "function" && typeof Set.prototype.forEach == "function" || console.error(
      "React depends on Map and Set built-in types. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"
    ), qa.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = ne, qa.createPortal = function(w, x) {
      var ce = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
      if (!x || x.nodeType !== 1 && x.nodeType !== 9 && x.nodeType !== 11)
        throw Error("Target container is not a DOM element.");
      return Be(w, x, null, ce);
    }, qa.flushSync = function(w) {
      var x = Ne.T, ce = ne.p;
      try {
        if (Ne.T = null, ne.p = 2, w)
          return w();
      } finally {
        Ne.T = x, ne.p = ce, ne.d.f() && console.error(
          "flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task."
        );
      }
    }, qa.preconnect = function(w, x) {
      typeof w == "string" && w ? x != null && typeof x != "object" ? console.error(
        "ReactDOM.preconnect(): Expected the `options` argument (second) to be an object but encountered %s instead. The only supported option at this time is `crossOrigin` which accepts a string.",
        Se(x)
      ) : x != null && typeof x.crossOrigin != "string" && console.error(
        "ReactDOM.preconnect(): Expected the `crossOrigin` option (second argument) to be a string but encountered %s instead. Try removing this option or passing a string value instead.",
        Re(x.crossOrigin)
      ) : console.error(
        "ReactDOM.preconnect(): Expected the `href` argument (first) to be a non-empty string but encountered %s instead.",
        Re(w)
      ), typeof w == "string" && (x ? (x = x.crossOrigin, x = typeof x == "string" ? x === "use-credentials" ? x : "" : void 0) : x = null, ne.d.C(w, x));
    }, qa.prefetchDNS = function(w) {
      if (typeof w != "string" || !w)
        console.error(
          "ReactDOM.prefetchDNS(): Expected the `href` argument (first) to be a non-empty string but encountered %s instead.",
          Re(w)
        );
      else if (1 < arguments.length) {
        var x = arguments[1];
        typeof x == "object" && x.hasOwnProperty("crossOrigin") ? console.error(
          "ReactDOM.prefetchDNS(): Expected only one argument, `href`, but encountered %s as a second argument instead. This argument is reserved for future options and is currently disallowed. It looks like the you are attempting to set a crossOrigin property for this DNS lookup hint. Browsers do not perform DNS queries using CORS and setting this attribute on the resource hint has no effect. Try calling ReactDOM.prefetchDNS() with just a single string argument, `href`.",
          Se(x)
        ) : console.error(
          "ReactDOM.prefetchDNS(): Expected only one argument, `href`, but encountered %s as a second argument instead. This argument is reserved for future options and is currently disallowed. Try calling ReactDOM.prefetchDNS() with just a single string argument, `href`.",
          Se(x)
        );
      }
      typeof w == "string" && ne.d.D(w);
    }, qa.preinit = function(w, x) {
      if (typeof w == "string" && w ? x == null || typeof x != "object" ? console.error(
        "ReactDOM.preinit(): Expected the `options` argument (second) to be an object with an `as` property describing the type of resource to be preinitialized but encountered %s instead.",
        Se(x)
      ) : x.as !== "style" && x.as !== "script" && console.error(
        'ReactDOM.preinit(): Expected the `as` property in the `options` argument (second) to contain a valid value describing the type of resource to be preinitialized but encountered %s instead. Valid values for `as` are "style" and "script".',
        Se(x.as)
      ) : console.error(
        "ReactDOM.preinit(): Expected the `href` argument (first) to be a non-empty string but encountered %s instead.",
        Re(w)
      ), typeof w == "string" && x && typeof x.as == "string") {
        var ce = x.as, Ge = U(ce, x.crossOrigin), it = typeof x.integrity == "string" ? x.integrity : void 0, ut = typeof x.fetchPriority == "string" ? x.fetchPriority : void 0;
        ce === "style" ? ne.d.S(
          w,
          typeof x.precedence == "string" ? x.precedence : void 0,
          {
            crossOrigin: Ge,
            integrity: it,
            fetchPriority: ut
          }
        ) : ce === "script" && ne.d.X(w, {
          crossOrigin: Ge,
          integrity: it,
          fetchPriority: ut,
          nonce: typeof x.nonce == "string" ? x.nonce : void 0
        });
      }
    }, qa.preinitModule = function(w, x) {
      var ce = "";
      typeof w == "string" && w || (ce += " The `href` argument encountered was " + Re(w) + "."), x !== void 0 && typeof x != "object" ? ce += " The `options` argument encountered was " + Re(x) + "." : x && "as" in x && x.as !== "script" && (ce += " The `as` option encountered was " + Se(x.as) + "."), ce ? console.error(
        "ReactDOM.preinitModule(): Expected up to two arguments, a non-empty `href` string and, optionally, an `options` object with a valid `as` property.%s",
        ce
      ) : (ce = x && typeof x.as == "string" ? x.as : "script", ce) === "script" || (ce = Se(ce), console.error(
        'ReactDOM.preinitModule(): Currently the only supported "as" type for this function is "script" but received "%s" instead. This warning was generated for `href` "%s". In the future other module types will be supported, aligning with the import-attributes proposal. Learn more here: (https://github.com/tc39/proposal-import-attributes)',
        ce,
        w
      )), typeof w == "string" && (typeof x == "object" && x !== null ? (x.as == null || x.as === "script") && (ce = U(
        x.as,
        x.crossOrigin
      ), ne.d.M(w, {
        crossOrigin: ce,
        integrity: typeof x.integrity == "string" ? x.integrity : void 0,
        nonce: typeof x.nonce == "string" ? x.nonce : void 0
      })) : x == null && ne.d.M(w));
    }, qa.preload = function(w, x) {
      var ce = "";
      if (typeof w == "string" && w || (ce += " The `href` argument encountered was " + Re(w) + "."), x == null || typeof x != "object" ? ce += " The `options` argument encountered was " + Re(x) + "." : typeof x.as == "string" && x.as || (ce += " The `as` option encountered was " + Re(x.as) + "."), ce && console.error(
        'ReactDOM.preload(): Expected two arguments, a non-empty `href` string and an `options` object with an `as` property valid for a `<link rel="preload" as="..." />` tag.%s',
        ce
      ), typeof w == "string" && typeof x == "object" && x !== null && typeof x.as == "string") {
        ce = x.as;
        var Ge = U(
          ce,
          x.crossOrigin
        );
        ne.d.L(w, ce, {
          crossOrigin: Ge,
          integrity: typeof x.integrity == "string" ? x.integrity : void 0,
          nonce: typeof x.nonce == "string" ? x.nonce : void 0,
          type: typeof x.type == "string" ? x.type : void 0,
          fetchPriority: typeof x.fetchPriority == "string" ? x.fetchPriority : void 0,
          referrerPolicy: typeof x.referrerPolicy == "string" ? x.referrerPolicy : void 0,
          imageSrcSet: typeof x.imageSrcSet == "string" ? x.imageSrcSet : void 0,
          imageSizes: typeof x.imageSizes == "string" ? x.imageSizes : void 0,
          media: typeof x.media == "string" ? x.media : void 0
        });
      }
    }, qa.preloadModule = function(w, x) {
      var ce = "";
      typeof w == "string" && w || (ce += " The `href` argument encountered was " + Re(w) + "."), x !== void 0 && typeof x != "object" ? ce += " The `options` argument encountered was " + Re(x) + "." : x && "as" in x && typeof x.as != "string" && (ce += " The `as` option encountered was " + Re(x.as) + "."), ce && console.error(
        'ReactDOM.preloadModule(): Expected two arguments, a non-empty `href` string and, optionally, an `options` object with an `as` property valid for a `<link rel="modulepreload" as="..." />` tag.%s',
        ce
      ), typeof w == "string" && (x ? (ce = U(
        x.as,
        x.crossOrigin
      ), ne.d.m(w, {
        as: typeof x.as == "string" && x.as !== "script" ? x.as : void 0,
        crossOrigin: ce,
        integrity: typeof x.integrity == "string" ? x.integrity : void 0
      })) : ne.d.m(w));
    }, qa.requestFormReset = function(w) {
      ne.d.r(w);
    }, qa.unstable_batchedUpdates = function(w, x) {
      return w(x);
    }, qa.useFormState = function(w, x, ce) {
      return mt().useFormState(w, x, ce);
    }, qa.useFormStatus = function() {
      return mt().useHostTransitionStatus();
    }, qa.version = "19.2.4", typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
  })()), qa;
}
var F2;
function aE() {
  if (F2) return Wv.exports;
  F2 = 1;
  function Q() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) {
      if (process.env.NODE_ENV !== "production")
        throw new Error("^_^");
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Q);
      } catch (te) {
        console.error(te);
      }
    }
  }
  return process.env.NODE_ENV === "production" ? (Q(), Wv.exports = HT()) : Wv.exports = jT(), Wv.exports;
}
var I2;
function BT() {
  if (I2) return Tp;
  I2 = 1;
  var Q = lE(), te = Om(), Be = aE();
  function U(l) {
    var n = "https://react.dev/errors/" + l;
    if (1 < arguments.length) {
      n += "?args[]=" + encodeURIComponent(arguments[1]);
      for (var u = 2; u < arguments.length; u++)
        n += "&args[]=" + encodeURIComponent(arguments[u]);
    }
    return "Minified React error #" + l + "; visit " + n + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  function Re(l) {
    return !(!l || l.nodeType !== 1 && l.nodeType !== 9 && l.nodeType !== 11);
  }
  function Se(l) {
    var n = l, u = l;
    if (l.alternate) for (; n.return; ) n = n.return;
    else {
      l = n;
      do
        n = l, (n.flags & 4098) !== 0 && (u = n.return), l = n.return;
      while (l);
    }
    return n.tag === 3 ? u : null;
  }
  function mt(l) {
    if (l.tag === 13) {
      var n = l.memoizedState;
      if (n === null && (l = l.alternate, l !== null && (n = l.memoizedState)), n !== null) return n.dehydrated;
    }
    return null;
  }
  function le(l) {
    if (l.tag === 31) {
      var n = l.memoizedState;
      if (n === null && (l = l.alternate, l !== null && (n = l.memoizedState)), n !== null) return n.dehydrated;
    }
    return null;
  }
  function ne(l) {
    if (Se(l) !== l)
      throw Error(U(188));
  }
  function W(l) {
    var n = l.alternate;
    if (!n) {
      if (n = Se(l), n === null) throw Error(U(188));
      return n !== l ? null : l;
    }
    for (var u = l, i = n; ; ) {
      var s = u.return;
      if (s === null) break;
      var r = s.alternate;
      if (r === null) {
        if (i = s.return, i !== null) {
          u = i;
          continue;
        }
        break;
      }
      if (s.child === r.child) {
        for (r = s.child; r; ) {
          if (r === u) return ne(s), l;
          if (r === i) return ne(s), n;
          r = r.sibling;
        }
        throw Error(U(188));
      }
      if (u.return !== i.return) u = s, i = r;
      else {
        for (var m = !1, v = s.child; v; ) {
          if (v === u) {
            m = !0, u = s, i = r;
            break;
          }
          if (v === i) {
            m = !0, i = s, u = r;
            break;
          }
          v = v.sibling;
        }
        if (!m) {
          for (v = r.child; v; ) {
            if (v === u) {
              m = !0, u = r, i = s;
              break;
            }
            if (v === i) {
              m = !0, i = r, u = s;
              break;
            }
            v = v.sibling;
          }
          if (!m) throw Error(U(189));
        }
      }
      if (u.alternate !== i) throw Error(U(190));
    }
    if (u.tag !== 3) throw Error(U(188));
    return u.stateNode.current === u ? l : n;
  }
  function Ne(l) {
    var n = l.tag;
    if (n === 5 || n === 26 || n === 27 || n === 6) return l;
    for (l = l.child; l !== null; ) {
      if (n = Ne(l), n !== null) return n;
      l = l.sibling;
    }
    return null;
  }
  var w = Object.assign, x = /* @__PURE__ */ Symbol.for("react.element"), ce = /* @__PURE__ */ Symbol.for("react.transitional.element"), Ge = /* @__PURE__ */ Symbol.for("react.portal"), it = /* @__PURE__ */ Symbol.for("react.fragment"), ut = /* @__PURE__ */ Symbol.for("react.strict_mode"), Ze = /* @__PURE__ */ Symbol.for("react.profiler"), qt = /* @__PURE__ */ Symbol.for("react.consumer"), Ot = /* @__PURE__ */ Symbol.for("react.context"), Ct = /* @__PURE__ */ Symbol.for("react.forward_ref"), wt = /* @__PURE__ */ Symbol.for("react.suspense"), Gt = /* @__PURE__ */ Symbol.for("react.suspense_list"), Ae = /* @__PURE__ */ Symbol.for("react.memo"), Je = /* @__PURE__ */ Symbol.for("react.lazy"), Me = /* @__PURE__ */ Symbol.for("react.activity"), se = /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel"), Yt = Symbol.iterator;
  function pe(l) {
    return l === null || typeof l != "object" ? null : (l = Yt && l[Yt] || l["@@iterator"], typeof l == "function" ? l : null);
  }
  var Xe = /* @__PURE__ */ Symbol.for("react.client.reference");
  function Kt(l) {
    if (l == null) return null;
    if (typeof l == "function")
      return l.$$typeof === Xe ? null : l.displayName || l.name || null;
    if (typeof l == "string") return l;
    switch (l) {
      case it:
        return "Fragment";
      case Ze:
        return "Profiler";
      case ut:
        return "StrictMode";
      case wt:
        return "Suspense";
      case Gt:
        return "SuspenseList";
      case Me:
        return "Activity";
    }
    if (typeof l == "object")
      switch (l.$$typeof) {
        case Ge:
          return "Portal";
        case Ot:
          return l.displayName || "Context";
        case qt:
          return (l._context.displayName || "Context") + ".Consumer";
        case Ct:
          var n = l.render;
          return l = l.displayName, l || (l = n.displayName || n.name || "", l = l !== "" ? "ForwardRef(" + l + ")" : "ForwardRef"), l;
        case Ae:
          return n = l.displayName || null, n !== null ? n : Kt(l.type) || "Memo";
        case Je:
          n = l._payload, l = l._init;
          try {
            return Kt(l(n));
          } catch {
          }
      }
    return null;
  }
  var Xt = Array.isArray, R = te.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, Z = Be.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, ee = {
    pending: !1,
    data: null,
    method: null,
    action: null
  }, ge = [], De = -1;
  function S(l) {
    return { current: l };
  }
  function H(l) {
    0 > De || (l.current = ge[De], ge[De] = null, De--);
  }
  function I(l, n) {
    De++, ge[De] = l.current, l.current = n;
  }
  var F = S(null), be = S(null), Le = S(null), Oe = S(null);
  function $t(l, n) {
    switch (I(Le, n), I(be, l), I(F, null), n.nodeType) {
      case 9:
      case 11:
        l = (l = n.documentElement) && (l = l.namespaceURI) ? Yg(l) : 0;
        break;
      default:
        if (l = n.tagName, n = n.namespaceURI)
          n = Yg(n), l = y0(n, l);
        else
          switch (l) {
            case "svg":
              l = 1;
              break;
            case "math":
              l = 2;
              break;
            default:
              l = 0;
          }
    }
    H(F), I(F, l);
  }
  function gt() {
    H(F), H(be), H(Le);
  }
  function wa(l) {
    l.memoizedState !== null && I(Oe, l);
    var n = F.current, u = y0(n, l.type);
    n !== u && (I(be, l), I(F, u));
  }
  function oe(l) {
    be.current === l && (H(F), H(be)), Oe.current === l && (H(Oe), Rr._currentValue = ee);
  }
  var _c, Mc;
  function Ga(l) {
    if (_c === void 0)
      try {
        throw Error();
      } catch (u) {
        var n = u.stack.trim().match(/\n( *(at )?)/);
        _c = n && n[1] || "", Mc = -1 < u.stack.indexOf(`
    at`) ? " (<anonymous>)" : -1 < u.stack.indexOf("@") ? "@unknown:0:0" : "";
      }
    return `
` + _c + l + Mc;
  }
  var iu = !1;
  function vt(l, n) {
    if (!l || iu) return "";
    iu = !0;
    var u = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      var i = {
        DetermineComponentFrameRoot: function() {
          try {
            if (n) {
              var $ = function() {
                throw Error();
              };
              if (Object.defineProperty($.prototype, "props", {
                set: function() {
                  throw Error();
                }
              }), typeof Reflect == "object" && Reflect.construct) {
                try {
                  Reflect.construct($, []);
                } catch (X) {
                  var B = X;
                }
                Reflect.construct(l, [], $);
              } else {
                try {
                  $.call();
                } catch (X) {
                  B = X;
                }
                l.call($.prototype);
              }
            } else {
              try {
                throw Error();
              } catch (X) {
                B = X;
              }
              ($ = l()) && typeof $.catch == "function" && $.catch(function() {
              });
            }
          } catch (X) {
            if (X && B && typeof X.stack == "string")
              return [X.stack, B.stack];
          }
          return [null, null];
        }
      };
      i.DetermineComponentFrameRoot.displayName = "DetermineComponentFrameRoot";
      var s = Object.getOwnPropertyDescriptor(
        i.DetermineComponentFrameRoot,
        "name"
      );
      s && s.configurable && Object.defineProperty(
        i.DetermineComponentFrameRoot,
        "name",
        { value: "DetermineComponentFrameRoot" }
      );
      var r = i.DetermineComponentFrameRoot(), m = r[0], v = r[1];
      if (m && v) {
        var A = m.split(`
`), j = v.split(`
`);
        for (s = i = 0; i < A.length && !A[i].includes("DetermineComponentFrameRoot"); )
          i++;
        for (; s < j.length && !j[s].includes(
          "DetermineComponentFrameRoot"
        ); )
          s++;
        if (i === A.length || s === j.length)
          for (i = A.length - 1, s = j.length - 1; 1 <= i && 0 <= s && A[i] !== j[s]; )
            s--;
        for (; 1 <= i && 0 <= s; i--, s--)
          if (A[i] !== j[s]) {
            if (i !== 1 || s !== 1)
              do
                if (i--, s--, 0 > s || A[i] !== j[s]) {
                  var V = `
` + A[i].replace(" at new ", " at ");
                  return l.displayName && V.includes("<anonymous>") && (V = V.replace("<anonymous>", l.displayName)), V;
                }
              while (1 <= i && 0 <= s);
            break;
          }
      }
    } finally {
      iu = !1, Error.prepareStackTrace = u;
    }
    return (u = l ? l.displayName || l.name : "") ? Ga(u) : "";
  }
  function ta(l, n) {
    switch (l.tag) {
      case 26:
      case 27:
      case 5:
        return Ga(l.type);
      case 16:
        return Ga("Lazy");
      case 13:
        return l.child !== n && n !== null ? Ga("Suspense Fallback") : Ga("Suspense");
      case 19:
        return Ga("SuspenseList");
      case 0:
      case 15:
        return vt(l.type, !1);
      case 11:
        return vt(l.type.render, !1);
      case 1:
        return vt(l.type, !0);
      case 31:
        return Ga("Activity");
      default:
        return "";
    }
  }
  function Si(l) {
    try {
      var n = "", u = null;
      do
        n += ta(l, u), u = l, l = l.return;
      while (l);
      return n;
    } catch (i) {
      return `
Error generating stack: ` + i.message + `
` + i.stack;
    }
  }
  var hs = Object.prototype.hasOwnProperty, de = Q.unstable_scheduleCallback, Cc = Q.unstable_cancelCallback, ou = Q.unstable_shouldYield, bi = Q.unstable_requestPaint, bl = Q.unstable_now, td = Q.unstable_getCurrentPriorityLevel, Uo = Q.unstable_ImmediatePriority, xo = Q.unstable_UserBlockingPriority, Un = Q.unstable_NormalPriority, ld = Q.unstable_LowPriority, No = Q.unstable_IdlePriority, ms = Q.log, Ei = Q.unstable_setDisableYieldValue, hn = null, zl = null;
  function Xa(l) {
    if (typeof ms == "function" && Ei(l), zl && typeof zl.setStrictMode == "function")
      try {
        zl.setStrictMode(hn, l);
      } catch {
      }
  }
  var Nl = Math.clz32 ? Math.clz32 : M, Uc = Math.log, g = Math.LN2;
  function M(l) {
    return l >>>= 0, l === 0 ? 32 : 31 - (Uc(l) / g | 0) | 0;
  }
  var P = 256, ae = 262144, he = 4194304;
  function Ce(l) {
    var n = l & 42;
    if (n !== 0) return n;
    switch (l & -l) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
        return 64;
      case 128:
        return 128;
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
        return l & 261888;
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return l & 3932160;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
        return l & 62914560;
      case 67108864:
        return 67108864;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 0;
      default:
        return l;
    }
  }
  function me(l, n, u) {
    var i = l.pendingLanes;
    if (i === 0) return 0;
    var s = 0, r = l.suspendedLanes, m = l.pingedLanes;
    l = l.warmLanes;
    var v = i & 134217727;
    return v !== 0 ? (i = v & ~r, i !== 0 ? s = Ce(i) : (m &= v, m !== 0 ? s = Ce(m) : u || (u = v & ~l, u !== 0 && (s = Ce(u))))) : (v = i & ~r, v !== 0 ? s = Ce(v) : m !== 0 ? s = Ce(m) : u || (u = i & ~l, u !== 0 && (s = Ce(u)))), s === 0 ? 0 : n !== 0 && n !== s && (n & r) === 0 && (r = s & -s, u = n & -n, r >= u || r === 32 && (u & 4194048) !== 0) ? n : s;
  }
  function lt(l, n) {
    return (l.pendingLanes & ~(l.suspendedLanes & ~l.pingedLanes) & n) === 0;
  }
  function Qe(l, n) {
    switch (l) {
      case 1:
      case 2:
      case 4:
      case 8:
      case 64:
        return n + 250;
      case 16:
      case 32:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return n + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
        return -1;
      case 67108864:
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function la() {
    var l = he;
    return he <<= 1, (he & 62914560) === 0 && (he = 4194304), l;
  }
  function mn(l) {
    for (var n = [], u = 0; 31 > u; u++) n.push(l);
    return n;
  }
  function xc(l, n) {
    l.pendingLanes |= n, n !== 268435456 && (l.suspendedLanes = 0, l.pingedLanes = 0, l.warmLanes = 0);
  }
  function Ho(l, n, u, i, s, r) {
    var m = l.pendingLanes;
    l.pendingLanes = u, l.suspendedLanes = 0, l.pingedLanes = 0, l.warmLanes = 0, l.expiredLanes &= u, l.entangledLanes &= u, l.errorRecoveryDisabledLanes &= u, l.shellSuspendCounter = 0;
    var v = l.entanglements, A = l.expirationTimes, j = l.hiddenUpdates;
    for (u = m & ~u; 0 < u; ) {
      var V = 31 - Nl(u), $ = 1 << V;
      v[V] = 0, A[V] = -1;
      var B = j[V];
      if (B !== null)
        for (j[V] = null, V = 0; V < B.length; V++) {
          var X = B[V];
          X !== null && (X.lane &= -536870913);
        }
      u &= ~$;
    }
    i !== 0 && ys(l, i, 0), r !== 0 && s === 0 && l.tag !== 0 && (l.suspendedLanes |= r & ~(m & ~n));
  }
  function ys(l, n, u) {
    l.pendingLanes |= n, l.suspendedLanes &= ~n;
    var i = 31 - Nl(n);
    l.entangledLanes |= n, l.entanglements[i] = l.entanglements[i] | 1073741824 | u & 261930;
  }
  function fu(l, n) {
    var u = l.entangledLanes |= n;
    for (l = l.entanglements; u; ) {
      var i = 31 - Nl(u), s = 1 << i;
      s & n | l[i] & n && (l[i] |= n), u &= ~s;
    }
  }
  function La(l, n) {
    var u = n & -n;
    return u = (u & 42) !== 0 ? 1 : ad(u), (u & (l.suspendedLanes | n)) !== 0 ? 0 : u;
  }
  function ad(l) {
    switch (l) {
      case 2:
        l = 1;
        break;
      case 8:
        l = 4;
        break;
      case 32:
        l = 16;
        break;
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
        l = 128;
        break;
      case 268435456:
        l = 134217728;
        break;
      default:
        l = 0;
    }
    return l;
  }
  function zm(l) {
    return l &= -l, 2 < l ? 8 < l ? (l & 134217727) !== 0 ? 32 : 268435456 : 8 : 2;
  }
  function nd() {
    var l = Z.p;
    return l !== 0 ? l : (l = window.event, l === void 0 ? 32 : _r(l.type));
  }
  function Dm(l, n) {
    var u = Z.p;
    try {
      return Z.p = l, n();
    } finally {
      Z.p = u;
    }
  }
  var xn = Math.random().toString(36).slice(2), Ut = "__reactFiber$" + xn, ra = "__reactProps$" + xn, Nc = "__reactContainer$" + xn, ud = "__reactEvents$" + xn, Rm = "__reactListeners$" + xn, zp = "__reactHandles$" + xn, _m = "__reactResources$" + xn, su = "__reactMarker$" + xn;
  function cd(l) {
    delete l[Ut], delete l[ra], delete l[ud], delete l[Rm], delete l[zp];
  }
  function Ti(l) {
    var n = l[Ut];
    if (n) return n;
    for (var u = l.parentNode; u; ) {
      if (n = u[Nc] || u[Ut]) {
        if (u = n.alternate, n.child !== null || u !== null && u.child !== null)
          for (l = Pn(l); l !== null; ) {
            if (u = l[Ut]) return u;
            l = Pn(l);
          }
        return n;
      }
      l = u, u = l.parentNode;
    }
    return null;
  }
  function Ai(l) {
    if (l = l[Ut] || l[Nc]) {
      var n = l.tag;
      if (n === 5 || n === 6 || n === 13 || n === 31 || n === 26 || n === 27 || n === 3)
        return l;
    }
    return null;
  }
  function jo(l) {
    var n = l.tag;
    if (n === 5 || n === 26 || n === 27 || n === 6) return l.stateNode;
    throw Error(U(33));
  }
  function Oi(l) {
    var n = l[_m];
    return n || (n = l[_m] = { hoistableStyles: /* @__PURE__ */ new Map(), hoistableScripts: /* @__PURE__ */ new Map() }), n;
  }
  function zt(l) {
    l[su] = !0;
  }
  var zi = /* @__PURE__ */ new Set(), Hc = {};
  function jc(l, n) {
    ru(l, n), ru(l + "Capture", n);
  }
  function ru(l, n) {
    for (Hc[l] = n, l = 0; l < n.length; l++)
      zi.add(n[l]);
  }
  var id = RegExp(
    "^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
  ), od = {}, Bo = {};
  function Yo(l) {
    return hs.call(Bo, l) ? !0 : hs.call(od, l) ? !1 : id.test(l) ? Bo[l] = !0 : (od[l] = !0, !1);
  }
  function qo(l, n, u) {
    if (Yo(n))
      if (u === null) l.removeAttribute(n);
      else {
        switch (typeof u) {
          case "undefined":
          case "function":
          case "symbol":
            l.removeAttribute(n);
            return;
          case "boolean":
            var i = n.toLowerCase().slice(0, 5);
            if (i !== "data-" && i !== "aria-") {
              l.removeAttribute(n);
              return;
            }
        }
        l.setAttribute(n, "" + u);
      }
  }
  function fd(l, n, u) {
    if (u === null) l.removeAttribute(n);
    else {
      switch (typeof u) {
        case "undefined":
        case "function":
        case "symbol":
        case "boolean":
          l.removeAttribute(n);
          return;
      }
      l.setAttribute(n, "" + u);
    }
  }
  function Pu(l, n, u, i) {
    if (i === null) l.removeAttribute(u);
    else {
      switch (typeof i) {
        case "undefined":
        case "function":
        case "symbol":
        case "boolean":
          l.removeAttribute(u);
          return;
      }
      l.setAttributeNS(n, u, "" + i);
    }
  }
  function Qa(l) {
    switch (typeof l) {
      case "bigint":
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return l;
      case "object":
        return l;
      default:
        return "";
    }
  }
  function sd(l) {
    var n = l.type;
    return (l = l.nodeName) && l.toLowerCase() === "input" && (n === "checkbox" || n === "radio");
  }
  function Mm(l, n, u) {
    var i = Object.getOwnPropertyDescriptor(
      l.constructor.prototype,
      n
    );
    if (!l.hasOwnProperty(n) && typeof i < "u" && typeof i.get == "function" && typeof i.set == "function") {
      var s = i.get, r = i.set;
      return Object.defineProperty(l, n, {
        configurable: !0,
        get: function() {
          return s.call(this);
        },
        set: function(m) {
          u = "" + m, r.call(this, m);
        }
      }), Object.defineProperty(l, n, {
        enumerable: i.enumerable
      }), {
        getValue: function() {
          return u;
        },
        setValue: function(m) {
          u = "" + m;
        },
        stopTracking: function() {
          l._valueTracker = null, delete l[n];
        }
      };
    }
  }
  function rd(l) {
    if (!l._valueTracker) {
      var n = sd(l) ? "checked" : "value";
      l._valueTracker = Mm(
        l,
        n,
        "" + l[n]
      );
    }
  }
  function Cm(l) {
    if (!l) return !1;
    var n = l._valueTracker;
    if (!n) return !0;
    var u = n.getValue(), i = "";
    return l && (i = sd(l) ? l.checked ? "true" : "false" : l.value), l = i, l !== u ? (n.setValue(l), !0) : !1;
  }
  function ps(l) {
    if (l = l || (typeof document < "u" ? document : void 0), typeof l > "u") return null;
    try {
      return l.activeElement || l.body;
    } catch {
      return l.body;
    }
  }
  var Pv = /[\n"\\]/g;
  function Va(l) {
    return l.replace(
      Pv,
      function(n) {
        return "\\" + n.charCodeAt(0).toString(16) + " ";
      }
    );
  }
  function gs(l, n, u, i, s, r, m, v) {
    l.name = "", m != null && typeof m != "function" && typeof m != "symbol" && typeof m != "boolean" ? l.type = m : l.removeAttribute("type"), n != null ? m === "number" ? (n === 0 && l.value === "" || l.value != n) && (l.value = "" + Qa(n)) : l.value !== "" + Qa(n) && (l.value = "" + Qa(n)) : m !== "submit" && m !== "reset" || l.removeAttribute("value"), n != null ? Di(l, m, Qa(n)) : u != null ? Di(l, m, Qa(u)) : i != null && l.removeAttribute("value"), s == null && r != null && (l.defaultChecked = !!r), s != null && (l.checked = s && typeof s != "function" && typeof s != "symbol"), v != null && typeof v != "function" && typeof v != "symbol" && typeof v != "boolean" ? l.name = "" + Qa(v) : l.removeAttribute("name");
  }
  function vs(l, n, u, i, s, r, m, v) {
    if (r != null && typeof r != "function" && typeof r != "symbol" && typeof r != "boolean" && (l.type = r), n != null || u != null) {
      if (!(r !== "submit" && r !== "reset" || n != null)) {
        rd(l);
        return;
      }
      u = u != null ? "" + Qa(u) : "", n = n != null ? "" + Qa(n) : u, v || n === l.value || (l.value = n), l.defaultValue = n;
    }
    i = i ?? s, i = typeof i != "function" && typeof i != "symbol" && !!i, l.checked = v ? l.checked : !!i, l.defaultChecked = !!i, m != null && typeof m != "function" && typeof m != "symbol" && typeof m != "boolean" && (l.name = m), rd(l);
  }
  function Di(l, n, u) {
    n === "number" && ps(l.ownerDocument) === l || l.defaultValue === "" + u || (l.defaultValue = "" + u);
  }
  function wo(l, n, u, i) {
    if (l = l.options, n) {
      n = {};
      for (var s = 0; s < u.length; s++)
        n["$" + u[s]] = !0;
      for (u = 0; u < l.length; u++)
        s = n.hasOwnProperty("$" + l[u].value), l[u].selected !== s && (l[u].selected = s), s && i && (l[u].defaultSelected = !0);
    } else {
      for (u = "" + Qa(u), n = null, s = 0; s < l.length; s++) {
        if (l[s].value === u) {
          l[s].selected = !0, i && (l[s].defaultSelected = !0);
          return;
        }
        n !== null || l[s].disabled || (n = l[s]);
      }
      n !== null && (n.selected = !0);
    }
  }
  function Um(l, n, u) {
    if (n != null && (n = "" + Qa(n), n !== l.value && (l.value = n), u == null)) {
      l.defaultValue !== n && (l.defaultValue = n);
      return;
    }
    l.defaultValue = u != null ? "" + Qa(u) : "";
  }
  function xm(l, n, u, i) {
    if (n == null) {
      if (i != null) {
        if (u != null) throw Error(U(92));
        if (Xt(i)) {
          if (1 < i.length) throw Error(U(93));
          i = i[0];
        }
        u = i;
      }
      u == null && (u = ""), n = u;
    }
    u = Qa(n), l.defaultValue = u, i = l.textContent, i === u && i !== "" && i !== null && (l.value = i), rd(l);
  }
  function du(l, n) {
    if (n) {
      var u = l.firstChild;
      if (u && u === l.lastChild && u.nodeType === 3) {
        u.nodeValue = n;
        return;
      }
    }
    l.textContent = n;
  }
  var Dp = new Set(
    "animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(
      " "
    )
  );
  function Rp(l, n, u) {
    var i = n.indexOf("--") === 0;
    u == null || typeof u == "boolean" || u === "" ? i ? l.setProperty(n, "") : n === "float" ? l.cssFloat = "" : l[n] = "" : i ? l.setProperty(n, u) : typeof u != "number" || u === 0 || Dp.has(n) ? n === "float" ? l.cssFloat = u : l[n] = ("" + u).trim() : l[n] = u + "px";
  }
  function _p(l, n, u) {
    if (n != null && typeof n != "object")
      throw Error(U(62));
    if (l = l.style, u != null) {
      for (var i in u)
        !u.hasOwnProperty(i) || n != null && n.hasOwnProperty(i) || (i.indexOf("--") === 0 ? l.setProperty(i, "") : i === "float" ? l.cssFloat = "" : l[i] = "");
      for (var s in n)
        i = n[s], n.hasOwnProperty(s) && u[s] !== i && Rp(l, s, i);
    } else
      for (var r in n)
        n.hasOwnProperty(r) && Rp(l, r, n[r]);
  }
  function Nm(l) {
    if (l.indexOf("-") === -1) return !1;
    switch (l) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return !1;
      default:
        return !0;
    }
  }
  var e1 = /* @__PURE__ */ new Map([
    ["acceptCharset", "accept-charset"],
    ["htmlFor", "for"],
    ["httpEquiv", "http-equiv"],
    ["crossOrigin", "crossorigin"],
    ["accentHeight", "accent-height"],
    ["alignmentBaseline", "alignment-baseline"],
    ["arabicForm", "arabic-form"],
    ["baselineShift", "baseline-shift"],
    ["capHeight", "cap-height"],
    ["clipPath", "clip-path"],
    ["clipRule", "clip-rule"],
    ["colorInterpolation", "color-interpolation"],
    ["colorInterpolationFilters", "color-interpolation-filters"],
    ["colorProfile", "color-profile"],
    ["colorRendering", "color-rendering"],
    ["dominantBaseline", "dominant-baseline"],
    ["enableBackground", "enable-background"],
    ["fillOpacity", "fill-opacity"],
    ["fillRule", "fill-rule"],
    ["floodColor", "flood-color"],
    ["floodOpacity", "flood-opacity"],
    ["fontFamily", "font-family"],
    ["fontSize", "font-size"],
    ["fontSizeAdjust", "font-size-adjust"],
    ["fontStretch", "font-stretch"],
    ["fontStyle", "font-style"],
    ["fontVariant", "font-variant"],
    ["fontWeight", "font-weight"],
    ["glyphName", "glyph-name"],
    ["glyphOrientationHorizontal", "glyph-orientation-horizontal"],
    ["glyphOrientationVertical", "glyph-orientation-vertical"],
    ["horizAdvX", "horiz-adv-x"],
    ["horizOriginX", "horiz-origin-x"],
    ["imageRendering", "image-rendering"],
    ["letterSpacing", "letter-spacing"],
    ["lightingColor", "lighting-color"],
    ["markerEnd", "marker-end"],
    ["markerMid", "marker-mid"],
    ["markerStart", "marker-start"],
    ["overlinePosition", "overline-position"],
    ["overlineThickness", "overline-thickness"],
    ["paintOrder", "paint-order"],
    ["panose-1", "panose-1"],
    ["pointerEvents", "pointer-events"],
    ["renderingIntent", "rendering-intent"],
    ["shapeRendering", "shape-rendering"],
    ["stopColor", "stop-color"],
    ["stopOpacity", "stop-opacity"],
    ["strikethroughPosition", "strikethrough-position"],
    ["strikethroughThickness", "strikethrough-thickness"],
    ["strokeDasharray", "stroke-dasharray"],
    ["strokeDashoffset", "stroke-dashoffset"],
    ["strokeLinecap", "stroke-linecap"],
    ["strokeLinejoin", "stroke-linejoin"],
    ["strokeMiterlimit", "stroke-miterlimit"],
    ["strokeOpacity", "stroke-opacity"],
    ["strokeWidth", "stroke-width"],
    ["textAnchor", "text-anchor"],
    ["textDecoration", "text-decoration"],
    ["textRendering", "text-rendering"],
    ["transformOrigin", "transform-origin"],
    ["underlinePosition", "underline-position"],
    ["underlineThickness", "underline-thickness"],
    ["unicodeBidi", "unicode-bidi"],
    ["unicodeRange", "unicode-range"],
    ["unitsPerEm", "units-per-em"],
    ["vAlphabetic", "v-alphabetic"],
    ["vHanging", "v-hanging"],
    ["vIdeographic", "v-ideographic"],
    ["vMathematical", "v-mathematical"],
    ["vectorEffect", "vector-effect"],
    ["vertAdvY", "vert-adv-y"],
    ["vertOriginX", "vert-origin-x"],
    ["vertOriginY", "vert-origin-y"],
    ["wordSpacing", "word-spacing"],
    ["writingMode", "writing-mode"],
    ["xmlnsXlink", "xmlns:xlink"],
    ["xHeight", "x-height"]
  ]), Ss = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;
  function yn(l) {
    return Ss.test("" + l) ? "javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')" : l;
  }
  function Nn() {
  }
  var dd = null;
  function hd(l) {
    return l = l.target || l.srcElement || window, l.correspondingUseElement && (l = l.correspondingUseElement), l.nodeType === 3 ? l.parentNode : l;
  }
  var hu = null, Ri = null;
  function bs(l) {
    var n = Ai(l);
    if (n && (l = n.stateNode)) {
      var u = l[ra] || null;
      e: switch (l = n.stateNode, n.type) {
        case "input":
          if (gs(
            l,
            u.value,
            u.defaultValue,
            u.defaultValue,
            u.checked,
            u.defaultChecked,
            u.type,
            u.name
          ), n = u.name, u.type === "radio" && n != null) {
            for (u = l; u.parentNode; ) u = u.parentNode;
            for (u = u.querySelectorAll(
              'input[name="' + Va(
                "" + n
              ) + '"][type="radio"]'
            ), n = 0; n < u.length; n++) {
              var i = u[n];
              if (i !== l && i.form === l.form) {
                var s = i[ra] || null;
                if (!s) throw Error(U(90));
                gs(
                  i,
                  s.value,
                  s.defaultValue,
                  s.defaultValue,
                  s.checked,
                  s.defaultChecked,
                  s.type,
                  s.name
                );
              }
            }
            for (n = 0; n < u.length; n++)
              i = u[n], i.form === l.form && Cm(i);
          }
          break e;
        case "textarea":
          Um(l, u.value, u.defaultValue);
          break e;
        case "select":
          n = u.value, n != null && wo(l, !!u.multiple, n, !1);
      }
    }
  }
  var Go = !1;
  function Hm(l, n, u) {
    if (Go) return l(n, u);
    Go = !0;
    try {
      var i = l(n);
      return i;
    } finally {
      if (Go = !1, (hu !== null || Ri !== null) && (Af(), hu && (n = hu, l = Ri, Ri = hu = null, bs(n), l)))
        for (n = 0; n < l.length; n++) bs(l[n]);
    }
  }
  function Hl(l, n) {
    var u = l.stateNode;
    if (u === null) return null;
    var i = u[ra] || null;
    if (i === null) return null;
    u = i[n];
    e: switch (n) {
      case "onClick":
      case "onClickCapture":
      case "onDoubleClick":
      case "onDoubleClickCapture":
      case "onMouseDown":
      case "onMouseDownCapture":
      case "onMouseMove":
      case "onMouseMoveCapture":
      case "onMouseUp":
      case "onMouseUpCapture":
      case "onMouseEnter":
        (i = !i.disabled) || (l = l.type, i = !(l === "button" || l === "input" || l === "select" || l === "textarea")), l = !i;
        break e;
      default:
        l = !1;
    }
    if (l) return null;
    if (u && typeof u != "function")
      throw Error(
        U(231, n, typeof u)
      );
    return u;
  }
  var ec = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Es = !1;
  if (ec)
    try {
      var Xo = {};
      Object.defineProperty(Xo, "passive", {
        get: function() {
          Es = !0;
        }
      }), window.addEventListener("test", Xo, Xo), window.removeEventListener("test", Xo, Xo);
    } catch {
      Es = !1;
    }
  var tc = null, jm = null, md = null;
  function Bm() {
    if (md) return md;
    var l, n = jm, u = n.length, i, s = "value" in tc ? tc.value : tc.textContent, r = s.length;
    for (l = 0; l < u && n[l] === s[l]; l++) ;
    var m = u - l;
    for (i = 1; i <= m && n[u - i] === s[r - i]; i++) ;
    return md = s.slice(l, 1 < i ? 1 - i : void 0);
  }
  function yd(l) {
    var n = l.keyCode;
    return "charCode" in l ? (l = l.charCode, l === 0 && n === 13 && (l = 13)) : l = n, l === 10 && (l = 13), 32 <= l || l === 13 ? l : 0;
  }
  function Ts() {
    return !0;
  }
  function Mp() {
    return !1;
  }
  function kl(l) {
    function n(u, i, s, r, m) {
      this._reactName = u, this._targetInst = s, this.type = i, this.nativeEvent = r, this.target = m, this.currentTarget = null;
      for (var v in l)
        l.hasOwnProperty(v) && (u = l[v], this[v] = u ? u(r) : r[v]);
      return this.isDefaultPrevented = (r.defaultPrevented != null ? r.defaultPrevented : r.returnValue === !1) ? Ts : Mp, this.isPropagationStopped = Mp, this;
    }
    return w(n.prototype, {
      preventDefault: function() {
        this.defaultPrevented = !0;
        var u = this.nativeEvent;
        u && (u.preventDefault ? u.preventDefault() : typeof u.returnValue != "unknown" && (u.returnValue = !1), this.isDefaultPrevented = Ts);
      },
      stopPropagation: function() {
        var u = this.nativeEvent;
        u && (u.stopPropagation ? u.stopPropagation() : typeof u.cancelBubble != "unknown" && (u.cancelBubble = !0), this.isPropagationStopped = Ts);
      },
      persist: function() {
      },
      isPersistent: Ts
    }), n;
  }
  var Bc = {
    eventPhase: 0,
    bubbles: 0,
    cancelable: 0,
    timeStamp: function(l) {
      return l.timeStamp || Date.now();
    },
    defaultPrevented: 0,
    isTrusted: 0
  }, As = kl(Bc), Lo = w({}, Bc, { view: 0, detail: 0 }), t1 = kl(Lo), Ym, qm, Os, pd = w({}, Lo, {
    screenX: 0,
    screenY: 0,
    clientX: 0,
    clientY: 0,
    pageX: 0,
    pageY: 0,
    ctrlKey: 0,
    shiftKey: 0,
    altKey: 0,
    metaKey: 0,
    getModifierState: pn,
    button: 0,
    buttons: 0,
    relatedTarget: function(l) {
      return l.relatedTarget === void 0 ? l.fromElement === l.srcElement ? l.toElement : l.fromElement : l.relatedTarget;
    },
    movementX: function(l) {
      return "movementX" in l ? l.movementX : (l !== Os && (Os && l.type === "mousemove" ? (Ym = l.screenX - Os.screenX, qm = l.screenY - Os.screenY) : qm = Ym = 0, Os = l), Ym);
    },
    movementY: function(l) {
      return "movementY" in l ? l.movementY : qm;
    }
  }), Qo = kl(pd), Cp = w({}, pd, { dataTransfer: 0 }), Up = kl(Cp), xp = w({}, Lo, { relatedTarget: 0 }), gd = kl(xp), wm = w({}, Bc, {
    animationName: 0,
    elapsedTime: 0,
    pseudoElement: 0
  }), Np = kl(wm), _i = w({}, Bc, {
    clipboardData: function(l) {
      return "clipboardData" in l ? l.clipboardData : window.clipboardData;
    }
  }), Mi = kl(_i), Hn = w({}, Bc, { data: 0 }), Hp = kl(Hn), Gm = {
    Esc: "Escape",
    Spacebar: " ",
    Left: "ArrowLeft",
    Up: "ArrowUp",
    Right: "ArrowRight",
    Down: "ArrowDown",
    Del: "Delete",
    Win: "OS",
    Menu: "ContextMenu",
    Apps: "ContextMenu",
    Scroll: "ScrollLock",
    MozPrintableKey: "Unidentified"
  }, mu = {
    8: "Backspace",
    9: "Tab",
    12: "Clear",
    13: "Enter",
    16: "Shift",
    17: "Control",
    18: "Alt",
    19: "Pause",
    20: "CapsLock",
    27: "Escape",
    32: " ",
    33: "PageUp",
    34: "PageDown",
    35: "End",
    36: "Home",
    37: "ArrowLeft",
    38: "ArrowUp",
    39: "ArrowRight",
    40: "ArrowDown",
    45: "Insert",
    46: "Delete",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    144: "NumLock",
    145: "ScrollLock",
    224: "Meta"
  }, jp = {
    Alt: "altKey",
    Control: "ctrlKey",
    Meta: "metaKey",
    Shift: "shiftKey"
  };
  function jn(l) {
    var n = this.nativeEvent;
    return n.getModifierState ? n.getModifierState(l) : (l = jp[l]) ? !!n[l] : !1;
  }
  function pn() {
    return jn;
  }
  var vd = w({}, Lo, {
    key: function(l) {
      if (l.key) {
        var n = Gm[l.key] || l.key;
        if (n !== "Unidentified") return n;
      }
      return l.type === "keypress" ? (l = yd(l), l === 13 ? "Enter" : String.fromCharCode(l)) : l.type === "keydown" || l.type === "keyup" ? mu[l.keyCode] || "Unidentified" : "";
    },
    code: 0,
    location: 0,
    ctrlKey: 0,
    shiftKey: 0,
    altKey: 0,
    metaKey: 0,
    repeat: 0,
    locale: 0,
    getModifierState: pn,
    charCode: function(l) {
      return l.type === "keypress" ? yd(l) : 0;
    },
    keyCode: function(l) {
      return l.type === "keydown" || l.type === "keyup" ? l.keyCode : 0;
    },
    which: function(l) {
      return l.type === "keypress" ? yd(l) : l.type === "keydown" || l.type === "keyup" ? l.keyCode : 0;
    }
  }), Sd = kl(vd), Xm = w({}, pd, {
    pointerId: 0,
    width: 0,
    height: 0,
    pressure: 0,
    tangentialPressure: 0,
    tiltX: 0,
    tiltY: 0,
    twist: 0,
    pointerType: 0,
    isPrimary: 0
  }), Bn = kl(Xm), l1 = w({}, Lo, {
    touches: 0,
    targetTouches: 0,
    changedTouches: 0,
    altKey: 0,
    metaKey: 0,
    ctrlKey: 0,
    shiftKey: 0,
    getModifierState: pn
  }), Bp = kl(l1), Yp = w({}, Bc, {
    propertyName: 0,
    elapsedTime: 0,
    pseudoElement: 0
  }), a1 = kl(Yp), Lm = w({}, pd, {
    deltaX: function(l) {
      return "deltaX" in l ? l.deltaX : "wheelDeltaX" in l ? -l.wheelDeltaX : 0;
    },
    deltaY: function(l) {
      return "deltaY" in l ? l.deltaY : "wheelDeltaY" in l ? -l.wheelDeltaY : "wheelDelta" in l ? -l.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), n1 = kl(Lm), qp = w({}, Bc, {
    newState: 0,
    oldState: 0
  }), Qm = kl(qp), bd = [9, 13, 27, 32], Vo = ec && "CompositionEvent" in window, Ci = null;
  ec && "documentMode" in document && (Ci = document.documentMode);
  var aa = ec && "TextEvent" in window && !Ci, Vm = ec && (!Vo || Ci && 8 < Ci && 11 >= Ci), zs = " ", Yc = !1;
  function Ed(l, n) {
    switch (l) {
      case "keyup":
        return bd.indexOf(n.keyCode) !== -1;
      case "keydown":
        return n.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return !0;
      default:
        return !1;
    }
  }
  function Zm(l) {
    return l = l.detail, typeof l == "object" && "data" in l ? l.data : null;
  }
  var Ui = !1;
  function wp(l, n) {
    switch (l) {
      case "compositionend":
        return Zm(n);
      case "keypress":
        return n.which !== 32 ? null : (Yc = !0, zs);
      case "textInput":
        return l = n.data, l === zs && Yc ? null : l;
      default:
        return null;
    }
  }
  function u1(l, n) {
    if (Ui)
      return l === "compositionend" || !Vo && Ed(l, n) ? (l = Bm(), md = jm = tc = null, Ui = !1, l) : null;
    switch (l) {
      case "paste":
        return null;
      case "keypress":
        if (!(n.ctrlKey || n.altKey || n.metaKey) || n.ctrlKey && n.altKey) {
          if (n.char && 1 < n.char.length)
            return n.char;
          if (n.which) return String.fromCharCode(n.which);
        }
        return null;
      case "compositionend":
        return Vm && n.locale !== "ko" ? null : n.data;
      default:
        return null;
    }
  }
  var Jm = {
    color: !0,
    date: !0,
    datetime: !0,
    "datetime-local": !0,
    email: !0,
    month: !0,
    number: !0,
    password: !0,
    range: !0,
    search: !0,
    tel: !0,
    text: !0,
    time: !0,
    url: !0,
    week: !0
  };
  function yu(l) {
    var n = l && l.nodeName && l.nodeName.toLowerCase();
    return n === "input" ? !!Jm[l.type] : n === "textarea";
  }
  function Km(l, n, u, i) {
    hu ? Ri ? Ri.push(i) : Ri = [i] : hu = i, n = Er(n, "onChange"), 0 < n.length && (u = new As(
      "onChange",
      "change",
      null,
      u,
      i
    ), l.push({ event: u, listeners: n }));
  }
  var xi = null, qc = null;
  function Ni(l) {
    Hg(l, 0);
  }
  function Zo(l) {
    var n = jo(l);
    if (Cm(n)) return l;
  }
  function $m(l, n) {
    if (l === "change") return n;
  }
  var Td = !1;
  if (ec) {
    var da;
    if (ec) {
      var Yn = "oninput" in document;
      if (!Yn) {
        var km = document.createElement("div");
        km.setAttribute("oninput", "return;"), Yn = typeof km.oninput == "function";
      }
      da = Yn;
    } else da = !1;
    Td = da && (!document.documentMode || 9 < document.documentMode);
  }
  function Ad() {
    xi && (xi.detachEvent("onpropertychange", Od), qc = xi = null);
  }
  function Od(l) {
    if (l.propertyName === "value" && Zo(qc)) {
      var n = [];
      Km(
        n,
        qc,
        l,
        hd(l)
      ), Hm(Ni, n);
    }
  }
  function Gp(l, n, u) {
    l === "focusin" ? (Ad(), xi = n, qc = u, xi.attachEvent("onpropertychange", Od)) : l === "focusout" && Ad();
  }
  function Xp(l) {
    if (l === "selectionchange" || l === "keyup" || l === "keydown")
      return Zo(qc);
  }
  function wc(l, n) {
    if (l === "click") return Zo(n);
  }
  function Hi(l, n) {
    if (l === "input" || l === "change")
      return Zo(n);
  }
  function Lp(l, n) {
    return l === n && (l !== 0 || 1 / l === 1 / n) || l !== l && n !== n;
  }
  var na = typeof Object.is == "function" ? Object.is : Lp;
  function gn(l, n) {
    if (na(l, n)) return !0;
    if (typeof l != "object" || l === null || typeof n != "object" || n === null)
      return !1;
    var u = Object.keys(l), i = Object.keys(n);
    if (u.length !== i.length) return !1;
    for (i = 0; i < u.length; i++) {
      var s = u[i];
      if (!hs.call(n, s) || !na(l[s], n[s]))
        return !1;
    }
    return !0;
  }
  function Wm(l) {
    for (; l && l.firstChild; ) l = l.firstChild;
    return l;
  }
  function Fm(l, n) {
    var u = Wm(l);
    l = 0;
    for (var i; u; ) {
      if (u.nodeType === 3) {
        if (i = l + u.textContent.length, l <= n && i >= n)
          return { node: u, offset: n - l };
        l = i;
      }
      e: {
        for (; u; ) {
          if (u.nextSibling) {
            u = u.nextSibling;
            break e;
          }
          u = u.parentNode;
        }
        u = void 0;
      }
      u = Wm(u);
    }
  }
  function ji(l, n) {
    return l && n ? l === n ? !0 : l && l.nodeType === 3 ? !1 : n && n.nodeType === 3 ? ji(l, n.parentNode) : "contains" in l ? l.contains(n) : l.compareDocumentPosition ? !!(l.compareDocumentPosition(n) & 16) : !1 : !1;
  }
  function Gc(l) {
    l = l != null && l.ownerDocument != null && l.ownerDocument.defaultView != null ? l.ownerDocument.defaultView : window;
    for (var n = ps(l.document); n instanceof l.HTMLIFrameElement; ) {
      try {
        var u = typeof n.contentWindow.location.href == "string";
      } catch {
        u = !1;
      }
      if (u) l = n.contentWindow;
      else break;
      n = ps(l.document);
    }
    return n;
  }
  function Ds(l) {
    var n = l && l.nodeName && l.nodeName.toLowerCase();
    return n && (n === "input" && (l.type === "text" || l.type === "search" || l.type === "tel" || l.type === "url" || l.type === "password") || n === "textarea" || l.contentEditable === "true");
  }
  var Rs = ec && "documentMode" in document && 11 >= document.documentMode, Xc = null, Jo = null, vn = null, qn = !1;
  function zd(l, n, u) {
    var i = u.window === u ? u.document : u.nodeType === 9 ? u : u.ownerDocument;
    qn || Xc == null || Xc !== ps(i) || (i = Xc, "selectionStart" in i && Ds(i) ? i = { start: i.selectionStart, end: i.selectionEnd } : (i = (i.ownerDocument && i.ownerDocument.defaultView || window).getSelection(), i = {
      anchorNode: i.anchorNode,
      anchorOffset: i.anchorOffset,
      focusNode: i.focusNode,
      focusOffset: i.focusOffset
    }), vn && gn(vn, i) || (vn = i, i = Er(Jo, "onSelect"), 0 < i.length && (n = new As(
      "onSelect",
      "select",
      null,
      n,
      u
    ), l.push({ event: n, listeners: i }), n.target = Xc)));
  }
  function lc(l, n) {
    var u = {};
    return u[l.toLowerCase()] = n.toLowerCase(), u["Webkit" + l] = "webkit" + n, u["Moz" + l] = "moz" + n, u;
  }
  var wn = {
    animationend: lc("Animation", "AnimationEnd"),
    animationiteration: lc("Animation", "AnimationIteration"),
    animationstart: lc("Animation", "AnimationStart"),
    transitionrun: lc("Transition", "TransitionRun"),
    transitionstart: lc("Transition", "TransitionStart"),
    transitioncancel: lc("Transition", "TransitionCancel"),
    transitionend: lc("Transition", "TransitionEnd")
  }, Ko = {}, Lc = {};
  ec && (Lc = document.createElement("div").style, "AnimationEvent" in window || (delete wn.animationend.animation, delete wn.animationiteration.animation, delete wn.animationstart.animation), "TransitionEvent" in window || delete wn.transitionend.transition);
  function Et(l) {
    if (Ko[l]) return Ko[l];
    if (!wn[l]) return l;
    var n = wn[l], u;
    for (u in n)
      if (n.hasOwnProperty(u) && u in Lc)
        return Ko[l] = n[u];
    return l;
  }
  var _s = Et("animationend"), Im = Et("animationiteration"), Dd = Et("animationstart"), Bi = Et("transitionrun"), Ms = Et("transitionstart"), pu = Et("transitioncancel"), Qp = Et("transitionend"), gu = /* @__PURE__ */ new Map(), $o = "abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(
    " "
  );
  $o.push("scrollEnd");
  function ha(l, n) {
    gu.set(l, n), jc(n, [l]);
  }
  var Yi = typeof reportError == "function" ? reportError : function(l) {
    if (typeof window == "object" && typeof window.ErrorEvent == "function") {
      var n = new window.ErrorEvent("error", {
        bubbles: !0,
        cancelable: !0,
        message: typeof l == "object" && l !== null && typeof l.message == "string" ? String(l.message) : String(l),
        error: l
      });
      if (!window.dispatchEvent(n)) return;
    } else if (typeof process == "object" && typeof process.emit == "function") {
      process.emit("uncaughtException", l);
      return;
    }
    console.error(l);
  }, Ft = [], jl = 0, Sn = 0;
  function Za() {
    for (var l = jl, n = Sn = jl = 0; n < l; ) {
      var u = Ft[n];
      Ft[n++] = null;
      var i = Ft[n];
      Ft[n++] = null;
      var s = Ft[n];
      Ft[n++] = null;
      var r = Ft[n];
      if (Ft[n++] = null, i !== null && s !== null) {
        var m = i.pending;
        m === null ? s.next = s : (s.next = m.next, m.next = s), i.pending = s;
      }
      r !== 0 && Rd(u, s, r);
    }
  }
  function Ja(l, n, u, i) {
    Ft[jl++] = l, Ft[jl++] = n, Ft[jl++] = u, Ft[jl++] = i, Sn |= i, l.lanes |= i, l = l.alternate, l !== null && (l.lanes |= i);
  }
  function bn(l, n, u, i) {
    return Ja(l, n, u, i), Cs(l);
  }
  function ac(l, n) {
    return Ja(l, null, null, n), Cs(l);
  }
  function Rd(l, n, u) {
    l.lanes |= u;
    var i = l.alternate;
    i !== null && (i.lanes |= u);
    for (var s = !1, r = l.return; r !== null; )
      r.childLanes |= u, i = r.alternate, i !== null && (i.childLanes |= u), r.tag === 22 && (l = r.stateNode, l === null || l._visibility & 1 || (s = !0)), l = r, r = r.return;
    return l.tag === 3 ? (r = l.stateNode, s && n !== null && (s = 31 - Nl(u), l = r.hiddenUpdates, i = l[s], i === null ? l[s] = [n] : i.push(n), n.lane = u | 536870912), r) : null;
  }
  function Cs(l) {
    if (50 < Tf)
      throw Tf = 0, dr = null, Error(U(185));
    for (var n = l.return; n !== null; )
      l = n, n = l.return;
    return l.tag === 3 ? l.stateNode : null;
  }
  var ma = {};
  function Vp(l, n, u, i) {
    this.tag = l, this.key = u, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.refCleanup = this.ref = null, this.pendingProps = n, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = i, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function ol(l, n, u, i) {
    return new Vp(l, n, u, i);
  }
  function qi(l) {
    return l = l.prototype, !(!l || !l.isReactComponent);
  }
  function nc(l, n) {
    var u = l.alternate;
    return u === null ? (u = ol(
      l.tag,
      n,
      l.key,
      l.mode
    ), u.elementType = l.elementType, u.type = l.type, u.stateNode = l.stateNode, u.alternate = l, l.alternate = u) : (u.pendingProps = n, u.type = l.type, u.flags = 0, u.subtreeFlags = 0, u.deletions = null), u.flags = l.flags & 65011712, u.childLanes = l.childLanes, u.lanes = l.lanes, u.child = l.child, u.memoizedProps = l.memoizedProps, u.memoizedState = l.memoizedState, u.updateQueue = l.updateQueue, n = l.dependencies, u.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }, u.sibling = l.sibling, u.index = l.index, u.ref = l.ref, u.refCleanup = l.refCleanup, u;
  }
  function Pm(l, n) {
    l.flags &= 65011714;
    var u = l.alternate;
    return u === null ? (l.childLanes = 0, l.lanes = n, l.child = null, l.subtreeFlags = 0, l.memoizedProps = null, l.memoizedState = null, l.updateQueue = null, l.dependencies = null, l.stateNode = null) : (l.childLanes = u.childLanes, l.lanes = u.lanes, l.child = u.child, l.subtreeFlags = 0, l.deletions = null, l.memoizedProps = u.memoizedProps, l.memoizedState = u.memoizedState, l.updateQueue = u.updateQueue, l.type = u.type, n = u.dependencies, l.dependencies = n === null ? null : {
      lanes: n.lanes,
      firstContext: n.firstContext
    }), l;
  }
  function _d(l, n, u, i, s, r) {
    var m = 0;
    if (i = l, typeof l == "function") qi(l) && (m = 1);
    else if (typeof l == "string")
      m = T0(
        l,
        u,
        F.current
      ) ? 26 : l === "html" || l === "head" || l === "body" ? 27 : 5;
    else
      e: switch (l) {
        case Me:
          return l = ol(31, u, n, s), l.elementType = Me, l.lanes = r, l;
        case it:
          return uc(u.children, s, r, n);
        case ut:
          m = 8, s |= 24;
          break;
        case Ze:
          return l = ol(12, u, n, s | 2), l.elementType = Ze, l.lanes = r, l;
        case wt:
          return l = ol(13, u, n, s), l.elementType = wt, l.lanes = r, l;
        case Gt:
          return l = ol(19, u, n, s), l.elementType = Gt, l.lanes = r, l;
        default:
          if (typeof l == "object" && l !== null)
            switch (l.$$typeof) {
              case Ot:
                m = 10;
                break e;
              case qt:
                m = 9;
                break e;
              case Ct:
                m = 11;
                break e;
              case Ae:
                m = 14;
                break e;
              case Je:
                m = 16, i = null;
                break e;
            }
          m = 29, u = Error(
            U(130, l === null ? "null" : typeof l, "")
          ), i = null;
      }
    return n = ol(m, u, n, s), n.elementType = l, n.type = i, n.lanes = r, n;
  }
  function uc(l, n, u, i) {
    return l = ol(7, l, i, n), l.lanes = u, l;
  }
  function ko(l, n, u) {
    return l = ol(6, l, null, n), l.lanes = u, l;
  }
  function ey(l) {
    var n = ol(18, null, null, 0);
    return n.stateNode = l, n;
  }
  function Md(l, n, u) {
    return n = ol(
      4,
      l.children !== null ? l.children : [],
      l.key,
      n
    ), n.lanes = u, n.stateNode = {
      containerInfo: l.containerInfo,
      pendingChildren: null,
      implementation: l.implementation
    }, n;
  }
  var ty = /* @__PURE__ */ new WeakMap();
  function Ka(l, n) {
    if (typeof l == "object" && l !== null) {
      var u = ty.get(l);
      return u !== void 0 ? u : (n = {
        value: l,
        source: n,
        stack: Si(n)
      }, ty.set(l, n), n);
    }
    return {
      value: l,
      source: n,
      stack: Si(n)
    };
  }
  var $a = [], wi = 0, Us = null, ml = 0, _a = [], ya = 0, Gn = null, Ma = 1, Xn = "";
  function En(l, n) {
    $a[wi++] = ml, $a[wi++] = Us, Us = l, ml = n;
  }
  function ly(l, n, u) {
    _a[ya++] = Ma, _a[ya++] = Xn, _a[ya++] = Gn, Gn = l;
    var i = Ma;
    l = Xn;
    var s = 32 - Nl(i) - 1;
    i &= ~(1 << s), u += 1;
    var r = 32 - Nl(n) + s;
    if (30 < r) {
      var m = s - s % 5;
      r = (i & (1 << m) - 1).toString(32), i >>= m, s -= m, Ma = 1 << 32 - Nl(n) + s | u << s | i, Xn = r + l;
    } else
      Ma = 1 << r | u << s | i, Xn = l;
  }
  function Wo(l) {
    l.return !== null && (En(l, 1), ly(l, 1, 0));
  }
  function Cd(l) {
    for (; l === Us; )
      Us = $a[--wi], $a[wi] = null, ml = $a[--wi], $a[wi] = null;
    for (; l === Gn; )
      Gn = _a[--ya], _a[ya] = null, Xn = _a[--ya], _a[ya] = null, Ma = _a[--ya], _a[ya] = null;
  }
  function xs(l, n) {
    _a[ya++] = Ma, _a[ya++] = Xn, _a[ya++] = Gn, Ma = n.id, Xn = n.overflow, Gn = l;
  }
  var Bl = null, Lt = null, ot = !1, vu = null, Dl = !1, Su = Error(U(519));
  function Tn(l) {
    var n = Error(
      U(
        418,
        1 < arguments.length && arguments[1] !== void 0 && arguments[1] ? "text" : "HTML",
        ""
      )
    );
    throw Io(Ka(n, l)), Su;
  }
  function Ns(l) {
    var n = l.stateNode, u = l.type, i = l.memoizedProps;
    switch (n[Ut] = l, n[ra] = i, u) {
      case "dialog":
        ct("cancel", n), ct("close", n);
        break;
      case "iframe":
      case "object":
      case "embed":
        ct("load", n);
        break;
      case "video":
      case "audio":
        for (u = 0; u < _f.length; u++)
          ct(_f[u], n);
        break;
      case "source":
        ct("error", n);
        break;
      case "img":
      case "image":
      case "link":
        ct("error", n), ct("load", n);
        break;
      case "details":
        ct("toggle", n);
        break;
      case "input":
        ct("invalid", n), vs(
          n,
          i.value,
          i.defaultValue,
          i.checked,
          i.defaultChecked,
          i.type,
          i.name,
          !0
        );
        break;
      case "select":
        ct("invalid", n);
        break;
      case "textarea":
        ct("invalid", n), xm(n, i.value, i.defaultValue, i.children);
    }
    u = i.children, typeof u != "string" && typeof u != "number" && typeof u != "bigint" || n.textContent === "" + u || i.suppressHydrationWarning === !0 || r0(n.textContent, u) ? (i.popover != null && (ct("beforetoggle", n), ct("toggle", n)), i.onScroll != null && ct("scroll", n), i.onScrollEnd != null && ct("scrollend", n), i.onClick != null && (n.onclick = Nn), n = !0) : n = !1, n || Tn(l, !0);
  }
  function Fo(l) {
    for (Bl = l.return; Bl; )
      switch (Bl.tag) {
        case 5:
        case 31:
        case 13:
          Dl = !1;
          return;
        case 27:
        case 3:
          Dl = !0;
          return;
        default:
          Bl = Bl.return;
      }
  }
  function bu(l) {
    if (l !== Bl) return !1;
    if (!ot) return Fo(l), ot = !0, !1;
    var n = l.tag, u;
    if ((u = n !== 3 && n !== 27) && ((u = n === 5) && (u = l.type, u = !(u !== "form" && u !== "button") || Cf(l.type, l.memoizedProps)), u = !u), u && Lt && Tn(l), Fo(l), n === 13) {
      if (l = l.memoizedState, l = l !== null ? l.dehydrated : null, !l) throw Error(U(317));
      Lt = Nh(l);
    } else if (n === 31) {
      if (l = l.memoizedState, l = l !== null ? l.dehydrated : null, !l) throw Error(U(317));
      Lt = Nh(l);
    } else
      n === 27 ? (n = Lt, In(l.type) ? (l = Or, Or = null, Lt = l) : Lt = n) : Lt = Bl ? za(l.stateNode.nextSibling) : null;
    return !0;
  }
  function Qc() {
    Lt = Bl = null, ot = !1;
  }
  function ay() {
    var l = vu;
    return l !== null && (cl === null ? cl = l : cl.push.apply(
      cl,
      l
    ), vu = null), l;
  }
  function Io(l) {
    vu === null ? vu = [l] : vu.push(l);
  }
  var Ud = S(null), cc = null, Ln = null;
  function pa(l, n, u) {
    I(Ud, n._currentValue), n._currentValue = u;
  }
  function Qn(l) {
    l._currentValue = Ud.current, H(Ud);
  }
  function xd(l, n, u) {
    for (; l !== null; ) {
      var i = l.alternate;
      if ((l.childLanes & n) !== n ? (l.childLanes |= n, i !== null && (i.childLanes |= n)) : i !== null && (i.childLanes & n) !== n && (i.childLanes |= n), l === u) break;
      l = l.return;
    }
  }
  function Eu(l, n, u, i) {
    var s = l.child;
    for (s !== null && (s.return = l); s !== null; ) {
      var r = s.dependencies;
      if (r !== null) {
        var m = s.child;
        r = r.firstContext;
        e: for (; r !== null; ) {
          var v = r;
          r = s;
          for (var A = 0; A < n.length; A++)
            if (v.context === n[A]) {
              r.lanes |= u, v = r.alternate, v !== null && (v.lanes |= u), xd(
                r.return,
                u,
                l
              ), i || (m = null);
              break e;
            }
          r = v.next;
        }
      } else if (s.tag === 18) {
        if (m = s.return, m === null) throw Error(U(341));
        m.lanes |= u, r = m.alternate, r !== null && (r.lanes |= u), xd(m, u, l), m = null;
      } else m = s.child;
      if (m !== null) m.return = s;
      else
        for (m = s; m !== null; ) {
          if (m === l) {
            m = null;
            break;
          }
          if (s = m.sibling, s !== null) {
            s.return = m.return, m = s;
            break;
          }
          m = m.return;
        }
      s = m;
    }
  }
  function Yl(l, n, u, i) {
    l = null;
    for (var s = n, r = !1; s !== null; ) {
      if (!r) {
        if ((s.flags & 524288) !== 0) r = !0;
        else if ((s.flags & 262144) !== 0) break;
      }
      if (s.tag === 10) {
        var m = s.alternate;
        if (m === null) throw Error(U(387));
        if (m = m.memoizedProps, m !== null) {
          var v = s.type;
          na(s.pendingProps.value, m.value) || (l !== null ? l.push(v) : l = [v]);
        }
      } else if (s === Oe.current) {
        if (m = s.alternate, m === null) throw Error(U(387));
        m.memoizedState.memoizedState !== s.memoizedState.memoizedState && (l !== null ? l.push(Rr) : l = [Rr]);
      }
      s = s.return;
    }
    l !== null && Eu(
      n,
      l,
      u,
      i
    ), n.flags |= 262144;
  }
  function Gi(l) {
    for (l = l.firstContext; l !== null; ) {
      if (!na(
        l.context._currentValue,
        l.memoizedValue
      ))
        return !0;
      l = l.next;
    }
    return !1;
  }
  function Ye(l) {
    cc = l, Ln = null, l = l.dependencies, l !== null && (l.firstContext = null);
  }
  function k(l) {
    return Hs(cc, l);
  }
  function ic(l, n) {
    return cc === null && Ye(l), Hs(l, n);
  }
  function Hs(l, n) {
    var u = n._currentValue;
    if (n = { context: n, memoizedValue: u, next: null }, Ln === null) {
      if (l === null) throw Error(U(308));
      Ln = n, l.dependencies = { lanes: 0, firstContext: n }, l.flags |= 524288;
    } else Ln = Ln.next = n;
    return u;
  }
  var fl = typeof AbortController < "u" ? AbortController : function() {
    var l = [], n = this.signal = {
      aborted: !1,
      addEventListener: function(u, i) {
        l.push(i);
      }
    };
    this.abort = function() {
      n.aborted = !0, l.forEach(function(u) {
        return u();
      });
    };
  }, ny = Q.unstable_scheduleCallback, uy = Q.unstable_NormalPriority, yl = {
    $$typeof: Ot,
    Consumer: null,
    Provider: null,
    _currentValue: null,
    _currentValue2: null,
    _threadCount: 0
  };
  function js() {
    return {
      controller: new fl(),
      data: /* @__PURE__ */ new Map(),
      refCount: 0
    };
  }
  function Bs(l) {
    l.refCount--, l.refCount === 0 && ny(uy, function() {
      l.controller.abort();
    });
  }
  var Xi = null, Ys = 0, Vc = 0, El = null;
  function Dt(l, n) {
    if (Xi === null) {
      var u = Xi = [];
      Ys = 0, Vc = zh(), El = {
        status: "pending",
        value: void 0,
        then: function(i) {
          u.push(i);
        }
      };
    }
    return Ys++, n.then(qs, qs), n;
  }
  function qs() {
    if (--Ys === 0 && Xi !== null) {
      El !== null && (El.status = "fulfilled");
      var l = Xi;
      Xi = null, Vc = 0, El = null;
      for (var n = 0; n < l.length; n++) (0, l[n])();
    }
  }
  function ws(l, n) {
    var u = [], i = {
      status: "pending",
      value: null,
      reason: null,
      then: function(s) {
        u.push(s);
      }
    };
    return l.then(
      function() {
        i.status = "fulfilled", i.value = n;
        for (var s = 0; s < u.length; s++) (0, u[s])(n);
      },
      function(s) {
        for (i.status = "rejected", i.reason = s, s = 0; s < u.length; s++)
          (0, u[s])(void 0);
      }
    ), i;
  }
  var oc = R.S;
  R.S = function(l, n) {
    Iy = bl(), typeof n == "object" && n !== null && typeof n.then == "function" && Dt(l, n), oc !== null && oc(l, n);
  };
  var ka = S(null);
  function Wa() {
    var l = ka.current;
    return l !== null ? l : Nt.pooledCache;
  }
  function Po(l, n) {
    n === null ? I(ka, ka.current) : I(ka, n.pool);
  }
  function Li() {
    var l = Wa();
    return l === null ? null : { parent: yl._currentValue, pool: l };
  }
  var Zc = Error(U(460)), Qi = Error(U(474)), ef = Error(U(542)), Vi = { then: function() {
  } };
  function cy(l) {
    return l = l.status, l === "fulfilled" || l === "rejected";
  }
  function iy(l, n, u) {
    switch (u = l[u], u === void 0 ? l.push(n) : u !== n && (n.then(Nn, Nn), n = u), n.status) {
      case "fulfilled":
        return n.value;
      case "rejected":
        throw l = n.reason, Nd(l), l;
      default:
        if (typeof n.status == "string") n.then(Nn, Nn);
        else {
          if (l = Nt, l !== null && 100 < l.shellSuspendCounter)
            throw Error(U(482));
          l = n, l.status = "pending", l.then(
            function(i) {
              if (n.status === "pending") {
                var s = n;
                s.status = "fulfilled", s.value = i;
              }
            },
            function(i) {
              if (n.status === "pending") {
                var s = n;
                s.status = "rejected", s.reason = i;
              }
            }
          );
        }
        switch (n.status) {
          case "fulfilled":
            return n.value;
          case "rejected":
            throw l = n.reason, Nd(l), l;
        }
        throw Kc = n, Zc;
    }
  }
  function Jc(l) {
    try {
      var n = l._init;
      return n(l._payload);
    } catch (u) {
      throw u !== null && typeof u == "object" && typeof u.then == "function" ? (Kc = u, Zc) : u;
    }
  }
  var Kc = null;
  function oy() {
    if (Kc === null) throw Error(U(459));
    var l = Kc;
    return Kc = null, l;
  }
  function Nd(l) {
    if (l === Zc || l === ef)
      throw Error(U(483));
  }
  var $c = null, Zi = 0;
  function Gs(l) {
    var n = Zi;
    return Zi += 1, $c === null && ($c = []), iy($c, l, n);
  }
  function tf(l, n) {
    n = n.props.ref, l.ref = n !== void 0 ? n : null;
  }
  function Xs(l, n) {
    throw n.$$typeof === x ? Error(U(525)) : (l = Object.prototype.toString.call(n), Error(
      U(
        31,
        l === "[object Object]" ? "object with keys {" + Object.keys(n).join(", ") + "}" : l
      )
    ));
  }
  function Zp(l) {
    function n(C, D) {
      if (l) {
        var N = C.deletions;
        N === null ? (C.deletions = [D], C.flags |= 16) : N.push(D);
      }
    }
    function u(C, D) {
      if (!l) return null;
      for (; D !== null; )
        n(C, D), D = D.sibling;
      return null;
    }
    function i(C) {
      for (var D = /* @__PURE__ */ new Map(); C !== null; )
        C.key !== null ? D.set(C.key, C) : D.set(C.index, C), C = C.sibling;
      return D;
    }
    function s(C, D) {
      return C = nc(C, D), C.index = 0, C.sibling = null, C;
    }
    function r(C, D, N) {
      return C.index = N, l ? (N = C.alternate, N !== null ? (N = N.index, N < D ? (C.flags |= 67108866, D) : N) : (C.flags |= 67108866, D)) : (C.flags |= 1048576, D);
    }
    function m(C) {
      return l && C.alternate === null && (C.flags |= 67108866), C;
    }
    function v(C, D, N, K) {
      return D === null || D.tag !== 6 ? (D = ko(N, C.mode, K), D.return = C, D) : (D = s(D, N), D.return = C, D);
    }
    function A(C, D, N, K) {
      var Ee = N.type;
      return Ee === it ? V(
        C,
        D,
        N.props.children,
        K,
        N.key
      ) : D !== null && (D.elementType === Ee || typeof Ee == "object" && Ee !== null && Ee.$$typeof === Je && Jc(Ee) === D.type) ? (D = s(D, N.props), tf(D, N), D.return = C, D) : (D = _d(
        N.type,
        N.key,
        N.props,
        null,
        C.mode,
        K
      ), tf(D, N), D.return = C, D);
    }
    function j(C, D, N, K) {
      return D === null || D.tag !== 4 || D.stateNode.containerInfo !== N.containerInfo || D.stateNode.implementation !== N.implementation ? (D = Md(N, C.mode, K), D.return = C, D) : (D = s(D, N.children || []), D.return = C, D);
    }
    function V(C, D, N, K, Ee) {
      return D === null || D.tag !== 7 ? (D = uc(
        N,
        C.mode,
        K,
        Ee
      ), D.return = C, D) : (D = s(D, N), D.return = C, D);
    }
    function $(C, D, N) {
      if (typeof D == "string" && D !== "" || typeof D == "number" || typeof D == "bigint")
        return D = ko(
          "" + D,
          C.mode,
          N
        ), D.return = C, D;
      if (typeof D == "object" && D !== null) {
        switch (D.$$typeof) {
          case ce:
            return N = _d(
              D.type,
              D.key,
              D.props,
              null,
              C.mode,
              N
            ), tf(N, D), N.return = C, N;
          case Ge:
            return D = Md(
              D,
              C.mode,
              N
            ), D.return = C, D;
          case Je:
            return D = Jc(D), $(C, D, N);
        }
        if (Xt(D) || pe(D))
          return D = uc(
            D,
            C.mode,
            N,
            null
          ), D.return = C, D;
        if (typeof D.then == "function")
          return $(C, Gs(D), N);
        if (D.$$typeof === Ot)
          return $(
            C,
            ic(C, D),
            N
          );
        Xs(C, D);
      }
      return null;
    }
    function B(C, D, N, K) {
      var Ee = D !== null ? D.key : null;
      if (typeof N == "string" && N !== "" || typeof N == "number" || typeof N == "bigint")
        return Ee !== null ? null : v(C, D, "" + N, K);
      if (typeof N == "object" && N !== null) {
        switch (N.$$typeof) {
          case ce:
            return N.key === Ee ? A(C, D, N, K) : null;
          case Ge:
            return N.key === Ee ? j(C, D, N, K) : null;
          case Je:
            return N = Jc(N), B(C, D, N, K);
        }
        if (Xt(N) || pe(N))
          return Ee !== null ? null : V(C, D, N, K, null);
        if (typeof N.then == "function")
          return B(
            C,
            D,
            Gs(N),
            K
          );
        if (N.$$typeof === Ot)
          return B(
            C,
            D,
            ic(C, N),
            K
          );
        Xs(C, N);
      }
      return null;
    }
    function X(C, D, N, K, Ee) {
      if (typeof K == "string" && K !== "" || typeof K == "number" || typeof K == "bigint")
        return C = C.get(N) || null, v(D, C, "" + K, Ee);
      if (typeof K == "object" && K !== null) {
        switch (K.$$typeof) {
          case ce:
            return C = C.get(
              K.key === null ? N : K.key
            ) || null, A(D, C, K, Ee);
          case Ge:
            return C = C.get(
              K.key === null ? N : K.key
            ) || null, j(D, C, K, Ee);
          case Je:
            return K = Jc(K), X(
              C,
              D,
              N,
              K,
              Ee
            );
        }
        if (Xt(K) || pe(K))
          return C = C.get(N) || null, V(D, C, K, Ee, null);
        if (typeof K.then == "function")
          return X(
            C,
            D,
            N,
            Gs(K),
            Ee
          );
        if (K.$$typeof === Ot)
          return X(
            C,
            D,
            N,
            ic(D, K),
            Ee
          );
        Xs(D, K);
      }
      return null;
    }
    function re(C, D, N, K) {
      for (var Ee = null, yt = null, ye = D, Ve = D = 0, We = null; ye !== null && Ve < N.length; Ve++) {
        ye.index > Ve ? (We = ye, ye = null) : We = ye.sibling;
        var bt = B(
          C,
          ye,
          N[Ve],
          K
        );
        if (bt === null) {
          ye === null && (ye = We);
          break;
        }
        l && ye && bt.alternate === null && n(C, ye), D = r(bt, D, Ve), yt === null ? Ee = bt : yt.sibling = bt, yt = bt, ye = We;
      }
      if (Ve === N.length)
        return u(C, ye), ot && En(C, Ve), Ee;
      if (ye === null) {
        for (; Ve < N.length; Ve++)
          ye = $(C, N[Ve], K), ye !== null && (D = r(
            ye,
            D,
            Ve
          ), yt === null ? Ee = ye : yt.sibling = ye, yt = ye);
        return ot && En(C, Ve), Ee;
      }
      for (ye = i(ye); Ve < N.length; Ve++)
        We = X(
          ye,
          C,
          Ve,
          N[Ve],
          K
        ), We !== null && (l && We.alternate !== null && ye.delete(
          We.key === null ? Ve : We.key
        ), D = r(
          We,
          D,
          Ve
        ), yt === null ? Ee = We : yt.sibling = We, yt = We);
      return l && ye.forEach(function(tu) {
        return n(C, tu);
      }), ot && En(C, Ve), Ee;
    }
    function _e(C, D, N, K) {
      if (N == null) throw Error(U(151));
      for (var Ee = null, yt = null, ye = D, Ve = D = 0, We = null, bt = N.next(); ye !== null && !bt.done; Ve++, bt = N.next()) {
        ye.index > Ve ? (We = ye, ye = null) : We = ye.sibling;
        var tu = B(C, ye, bt.value, K);
        if (tu === null) {
          ye === null && (ye = We);
          break;
        }
        l && ye && tu.alternate === null && n(C, ye), D = r(tu, D, Ve), yt === null ? Ee = tu : yt.sibling = tu, yt = tu, ye = We;
      }
      if (bt.done)
        return u(C, ye), ot && En(C, Ve), Ee;
      if (ye === null) {
        for (; !bt.done; Ve++, bt = N.next())
          bt = $(C, bt.value, K), bt !== null && (D = r(bt, D, Ve), yt === null ? Ee = bt : yt.sibling = bt, yt = bt);
        return ot && En(C, Ve), Ee;
      }
      for (ye = i(ye); !bt.done; Ve++, bt = N.next())
        bt = X(ye, C, Ve, bt.value, K), bt !== null && (l && bt.alternate !== null && ye.delete(bt.key === null ? Ve : bt.key), D = r(bt, D, Ve), yt === null ? Ee = bt : yt.sibling = bt, yt = bt);
      return l && ye.forEach(function(kg) {
        return n(C, kg);
      }), ot && En(C, Ve), Ee;
    }
    function jt(C, D, N, K) {
      if (typeof N == "object" && N !== null && N.type === it && N.key === null && (N = N.props.children), typeof N == "object" && N !== null) {
        switch (N.$$typeof) {
          case ce:
            e: {
              for (var Ee = N.key; D !== null; ) {
                if (D.key === Ee) {
                  if (Ee = N.type, Ee === it) {
                    if (D.tag === 7) {
                      u(
                        C,
                        D.sibling
                      ), K = s(
                        D,
                        N.props.children
                      ), K.return = C, C = K;
                      break e;
                    }
                  } else if (D.elementType === Ee || typeof Ee == "object" && Ee !== null && Ee.$$typeof === Je && Jc(Ee) === D.type) {
                    u(
                      C,
                      D.sibling
                    ), K = s(D, N.props), tf(K, N), K.return = C, C = K;
                    break e;
                  }
                  u(C, D);
                  break;
                } else n(C, D);
                D = D.sibling;
              }
              N.type === it ? (K = uc(
                N.props.children,
                C.mode,
                K,
                N.key
              ), K.return = C, C = K) : (K = _d(
                N.type,
                N.key,
                N.props,
                null,
                C.mode,
                K
              ), tf(K, N), K.return = C, C = K);
            }
            return m(C);
          case Ge:
            e: {
              for (Ee = N.key; D !== null; ) {
                if (D.key === Ee)
                  if (D.tag === 4 && D.stateNode.containerInfo === N.containerInfo && D.stateNode.implementation === N.implementation) {
                    u(
                      C,
                      D.sibling
                    ), K = s(D, N.children || []), K.return = C, C = K;
                    break e;
                  } else {
                    u(C, D);
                    break;
                  }
                else n(C, D);
                D = D.sibling;
              }
              K = Md(N, C.mode, K), K.return = C, C = K;
            }
            return m(C);
          case Je:
            return N = Jc(N), jt(
              C,
              D,
              N,
              K
            );
        }
        if (Xt(N))
          return re(
            C,
            D,
            N,
            K
          );
        if (pe(N)) {
          if (Ee = pe(N), typeof Ee != "function") throw Error(U(150));
          return N = Ee.call(N), _e(
            C,
            D,
            N,
            K
          );
        }
        if (typeof N.then == "function")
          return jt(
            C,
            D,
            Gs(N),
            K
          );
        if (N.$$typeof === Ot)
          return jt(
            C,
            D,
            ic(C, N),
            K
          );
        Xs(C, N);
      }
      return typeof N == "string" && N !== "" || typeof N == "number" || typeof N == "bigint" ? (N = "" + N, D !== null && D.tag === 6 ? (u(C, D.sibling), K = s(D, N), K.return = C, C = K) : (u(C, D), K = ko(N, C.mode, K), K.return = C, C = K), m(C)) : u(C, D);
    }
    return function(C, D, N, K) {
      try {
        Zi = 0;
        var Ee = jt(
          C,
          D,
          N,
          K
        );
        return $c = null, Ee;
      } catch (ye) {
        if (ye === Zc || ye === ef) throw ye;
        var yt = ol(29, ye, null, C.mode);
        return yt.lanes = K, yt.return = C, yt;
      }
    };
  }
  var kc = Zp(!0), fy = Zp(!1), fc = !1;
  function Ls(l) {
    l.updateQueue = {
      baseState: l.memoizedState,
      firstBaseUpdate: null,
      lastBaseUpdate: null,
      shared: { pending: null, lanes: 0, hiddenCallbacks: null },
      callbacks: null
    };
  }
  function Hd(l, n) {
    l = l.updateQueue, n.updateQueue === l && (n.updateQueue = {
      baseState: l.baseState,
      firstBaseUpdate: l.firstBaseUpdate,
      lastBaseUpdate: l.lastBaseUpdate,
      shared: l.shared,
      callbacks: null
    });
  }
  function sc(l) {
    return { lane: l, tag: 0, payload: null, callback: null, next: null };
  }
  function Fa(l, n, u) {
    var i = l.updateQueue;
    if (i === null) return null;
    if (i = i.shared, (St & 2) !== 0) {
      var s = i.pending;
      return s === null ? n.next = n : (n.next = s.next, s.next = n), i.pending = n, n = Cs(l), Rd(l, null, u), n;
    }
    return Ja(l, i, n, u), Cs(l);
  }
  function Wc(l, n, u) {
    if (n = n.updateQueue, n !== null && (n = n.shared, (u & 4194048) !== 0)) {
      var i = n.lanes;
      i &= l.pendingLanes, u |= i, n.lanes = u, fu(l, u);
    }
  }
  function jd(l, n) {
    var u = l.updateQueue, i = l.alternate;
    if (i !== null && (i = i.updateQueue, u === i)) {
      var s = null, r = null;
      if (u = u.firstBaseUpdate, u !== null) {
        do {
          var m = {
            lane: u.lane,
            tag: u.tag,
            payload: u.payload,
            callback: null,
            next: null
          };
          r === null ? s = r = m : r = r.next = m, u = u.next;
        } while (u !== null);
        r === null ? s = r = n : r = r.next = n;
      } else s = r = n;
      u = {
        baseState: i.baseState,
        firstBaseUpdate: s,
        lastBaseUpdate: r,
        shared: i.shared,
        callbacks: i.callbacks
      }, l.updateQueue = u;
      return;
    }
    l = u.lastBaseUpdate, l === null ? u.firstBaseUpdate = n : l.next = n, u.lastBaseUpdate = n;
  }
  var sy = !1;
  function Fc() {
    if (sy) {
      var l = El;
      if (l !== null) throw l;
    }
  }
  function Tu(l, n, u, i) {
    sy = !1;
    var s = l.updateQueue;
    fc = !1;
    var r = s.firstBaseUpdate, m = s.lastBaseUpdate, v = s.shared.pending;
    if (v !== null) {
      s.shared.pending = null;
      var A = v, j = A.next;
      A.next = null, m === null ? r = j : m.next = j, m = A;
      var V = l.alternate;
      V !== null && (V = V.updateQueue, v = V.lastBaseUpdate, v !== m && (v === null ? V.firstBaseUpdate = j : v.next = j, V.lastBaseUpdate = A));
    }
    if (r !== null) {
      var $ = s.baseState;
      m = 0, V = j = A = null, v = r;
      do {
        var B = v.lane & -536870913, X = B !== v.lane;
        if (X ? (at & B) === B : (i & B) === B) {
          B !== 0 && B === Vc && (sy = !0), V !== null && (V = V.next = {
            lane: 0,
            tag: v.tag,
            payload: v.payload,
            callback: null,
            next: null
          });
          e: {
            var re = l, _e = v;
            B = n;
            var jt = u;
            switch (_e.tag) {
              case 1:
                if (re = _e.payload, typeof re == "function") {
                  $ = re.call(jt, $, B);
                  break e;
                }
                $ = re;
                break e;
              case 3:
                re.flags = re.flags & -65537 | 128;
              case 0:
                if (re = _e.payload, B = typeof re == "function" ? re.call(jt, $, B) : re, B == null) break e;
                $ = w({}, $, B);
                break e;
              case 2:
                fc = !0;
            }
          }
          B = v.callback, B !== null && (l.flags |= 64, X && (l.flags |= 8192), X = s.callbacks, X === null ? s.callbacks = [B] : X.push(B));
        } else
          X = {
            lane: B,
            tag: v.tag,
            payload: v.payload,
            callback: v.callback,
            next: null
          }, V === null ? (j = V = X, A = $) : V = V.next = X, m |= B;
        if (v = v.next, v === null) {
          if (v = s.shared.pending, v === null)
            break;
          X = v, v = X.next, X.next = null, s.lastBaseUpdate = X, s.shared.pending = null;
        }
      } while (!0);
      V === null && (A = $), s.baseState = A, s.firstBaseUpdate = j, s.lastBaseUpdate = V, r === null && (s.shared.lanes = 0), Wn |= m, l.lanes = m, l.memoizedState = $;
    }
  }
  function Bd(l, n) {
    if (typeof l != "function")
      throw Error(U(191, l));
    l.call(n);
  }
  function Ic(l, n) {
    var u = l.callbacks;
    if (u !== null)
      for (l.callbacks = null, l = 0; l < u.length; l++)
        Bd(u[l], n);
  }
  var Rl = S(null), Ji = S(0);
  function Jp(l, n) {
    l = kn, I(Ji, l), I(Rl, n), kn = l | n.baseLanes;
  }
  function Qs() {
    I(Ji, kn), I(Rl, Rl.current);
  }
  function lf() {
    kn = Ji.current, H(Rl), H(Ji);
  }
  var ga = S(null), Ia = null;
  function Au(l) {
    var n = l.alternate;
    I(It, It.current & 1), I(ga, l), Ia === null && (n === null || Rl.current !== null || n.memoizedState !== null) && (Ia = l);
  }
  function af(l) {
    I(It, It.current), I(ga, l), Ia === null && (Ia = l);
  }
  function Yd(l) {
    l.tag === 22 ? (I(It, It.current), I(ga, l), Ia === null && (Ia = l)) : Vn();
  }
  function Vn() {
    I(It, It.current), I(ga, ga.current);
  }
  function va(l) {
    H(ga), Ia === l && (Ia = null), H(It);
  }
  var It = S(0);
  function nf(l) {
    for (var n = l; n !== null; ) {
      if (n.tag === 13) {
        var u = n.memoizedState;
        if (u !== null && (u = u.dehydrated, u === null || Dn(u) || si(u)))
          return n;
      } else if (n.tag === 19 && (n.memoizedProps.revealOrder === "forwards" || n.memoizedProps.revealOrder === "backwards" || n.memoizedProps.revealOrder === "unstable_legacy-backwards" || n.memoizedProps.revealOrder === "together")) {
        if ((n.flags & 128) !== 0) return n;
      } else if (n.child !== null) {
        n.child.return = n, n = n.child;
        continue;
      }
      if (n === l) break;
      for (; n.sibling === null; ) {
        if (n.return === null || n.return === l) return null;
        n = n.return;
      }
      n.sibling.return = n.return, n = n.sibling;
    }
    return null;
  }
  var Ou = 0, Ke = null, Rt = null, pl = null, Ki = !1, $i = !1, rc = !1, Vs = 0, uf = 0, Pc = null, Kp = 0;
  function nl() {
    throw Error(U(321));
  }
  function dc(l, n) {
    if (n === null) return !1;
    for (var u = 0; u < n.length && u < l.length; u++)
      if (!na(l[u], n[u])) return !1;
    return !0;
  }
  function Zs(l, n, u, i, s, r) {
    return Ou = r, Ke = n, n.memoizedState = null, n.updateQueue = null, n.lanes = 0, R.H = l === null || l.memoizedState === null ? tg : eh, rc = !1, r = u(i, s), rc = !1, $i && (r = $p(
      n,
      u,
      i,
      s
    )), qd(l), r;
  }
  function qd(l) {
    R.H = er;
    var n = Rt !== null && Rt.next !== null;
    if (Ou = 0, pl = Rt = Ke = null, Ki = !1, uf = 0, Pc = null, n) throw Error(U(300));
    l === null || gl || (l = l.dependencies, l !== null && Gi(l) && (gl = !0));
  }
  function $p(l, n, u, i) {
    Ke = l;
    var s = 0;
    do {
      if ($i && (Pc = null), uf = 0, $i = !1, 25 <= s) throw Error(U(301));
      if (s += 1, pl = Rt = null, l.updateQueue != null) {
        var r = l.updateQueue;
        r.lastEffect = null, r.events = null, r.stores = null, r.memoCache != null && (r.memoCache.index = 0);
      }
      R.H = lg, r = n(u, i);
    } while ($i);
    return r;
  }
  function c1() {
    var l = R.H, n = l.useState()[0];
    return n = typeof n.then == "function" ? Wi(n) : n, l = l.useState()[0], (Rt !== null ? Rt.memoizedState : null) !== l && (Ke.flags |= 1024), n;
  }
  function wd() {
    var l = Vs !== 0;
    return Vs = 0, l;
  }
  function ki(l, n, u) {
    n.updateQueue = l.updateQueue, n.flags &= -2053, l.lanes &= ~u;
  }
  function Js(l) {
    if (Ki) {
      for (l = l.memoizedState; l !== null; ) {
        var n = l.queue;
        n !== null && (n.pending = null), l = l.next;
      }
      Ki = !1;
    }
    Ou = 0, pl = Rt = Ke = null, $i = !1, uf = Vs = 0, Pc = null;
  }
  function ql() {
    var l = {
      memoizedState: null,
      baseState: null,
      baseQueue: null,
      queue: null,
      next: null
    };
    return pl === null ? Ke.memoizedState = pl = l : pl = pl.next = l, pl;
  }
  function sl() {
    if (Rt === null) {
      var l = Ke.alternate;
      l = l !== null ? l.memoizedState : null;
    } else l = Rt.next;
    var n = pl === null ? Ke.memoizedState : pl.next;
    if (n !== null)
      pl = n, Rt = l;
    else {
      if (l === null)
        throw Ke.alternate === null ? Error(U(467)) : Error(U(310));
      Rt = l, l = {
        memoizedState: Rt.memoizedState,
        baseState: Rt.baseState,
        baseQueue: Rt.baseQueue,
        queue: Rt.queue,
        next: null
      }, pl === null ? Ke.memoizedState = pl = l : pl = pl.next = l;
    }
    return pl;
  }
  function Ks() {
    return { lastEffect: null, events: null, stores: null, memoCache: null };
  }
  function Wi(l) {
    var n = uf;
    return uf += 1, Pc === null && (Pc = []), l = iy(Pc, l, n), n = Ke, (pl === null ? n.memoizedState : pl.next) === null && (n = n.alternate, R.H = n === null || n.memoizedState === null ? tg : eh), l;
  }
  function cf(l) {
    if (l !== null && typeof l == "object") {
      if (typeof l.then == "function") return Wi(l);
      if (l.$$typeof === Ot) return k(l);
    }
    throw Error(U(438, String(l)));
  }
  function Gd(l) {
    var n = null, u = Ke.updateQueue;
    if (u !== null && (n = u.memoCache), n == null) {
      var i = Ke.alternate;
      i !== null && (i = i.updateQueue, i !== null && (i = i.memoCache, i != null && (n = {
        data: i.data.map(function(s) {
          return s.slice();
        }),
        index: 0
      })));
    }
    if (n == null && (n = { data: [], index: 0 }), u === null && (u = Ks(), Ke.updateQueue = u), u.memoCache = n, u = n.data[n.index], u === void 0)
      for (u = n.data[n.index] = Array(l), i = 0; i < l; i++)
        u[i] = se;
    return n.index++, u;
  }
  function zu(l, n) {
    return typeof n == "function" ? n(l) : n;
  }
  function Du(l) {
    var n = sl();
    return Xd(n, Rt, l);
  }
  function Xd(l, n, u) {
    var i = l.queue;
    if (i === null) throw Error(U(311));
    i.lastRenderedReducer = u;
    var s = l.baseQueue, r = i.pending;
    if (r !== null) {
      if (s !== null) {
        var m = s.next;
        s.next = r.next, r.next = m;
      }
      n.baseQueue = s = r, i.pending = null;
    }
    if (r = l.baseState, s === null) l.memoizedState = r;
    else {
      n = s.next;
      var v = m = null, A = null, j = n, V = !1;
      do {
        var $ = j.lane & -536870913;
        if ($ !== j.lane ? (at & $) === $ : (Ou & $) === $) {
          var B = j.revertLane;
          if (B === 0)
            A !== null && (A = A.next = {
              lane: 0,
              revertLane: 0,
              gesture: null,
              action: j.action,
              hasEagerState: j.hasEagerState,
              eagerState: j.eagerState,
              next: null
            }), $ === Vc && (V = !0);
          else if ((Ou & B) === B) {
            j = j.next, B === Vc && (V = !0);
            continue;
          } else
            $ = {
              lane: 0,
              revertLane: j.revertLane,
              gesture: null,
              action: j.action,
              hasEagerState: j.hasEagerState,
              eagerState: j.eagerState,
              next: null
            }, A === null ? (v = A = $, m = r) : A = A.next = $, Ke.lanes |= B, Wn |= B;
          $ = j.action, rc && u(r, $), r = j.hasEagerState ? j.eagerState : u(r, $);
        } else
          B = {
            lane: $,
            revertLane: j.revertLane,
            gesture: j.gesture,
            action: j.action,
            hasEagerState: j.hasEagerState,
            eagerState: j.eagerState,
            next: null
          }, A === null ? (v = A = B, m = r) : A = A.next = B, Ke.lanes |= $, Wn |= $;
        j = j.next;
      } while (j !== null && j !== n);
      if (A === null ? m = r : A.next = v, !na(r, l.memoizedState) && (gl = !0, V && (u = El, u !== null)))
        throw u;
      l.memoizedState = r, l.baseState = m, l.baseQueue = A, i.lastRenderedState = r;
    }
    return s === null && (i.lanes = 0), [l.memoizedState, i.dispatch];
  }
  function Ld(l) {
    var n = sl(), u = n.queue;
    if (u === null) throw Error(U(311));
    u.lastRenderedReducer = l;
    var i = u.dispatch, s = u.pending, r = n.memoizedState;
    if (s !== null) {
      u.pending = null;
      var m = s = s.next;
      do
        r = l(r, m.action), m = m.next;
      while (m !== s);
      na(r, n.memoizedState) || (gl = !0), n.memoizedState = r, n.baseQueue === null && (n.baseState = r), u.lastRenderedState = r;
    }
    return [r, i];
  }
  function ry(l, n, u) {
    var i = Ke, s = sl(), r = ot;
    if (r) {
      if (u === void 0) throw Error(U(407));
      u = u();
    } else u = n();
    var m = !na(
      (Rt || s).memoizedState,
      u
    );
    if (m && (s.memoizedState = u, gl = !0), s = s.queue, Kd(Qd.bind(null, i, s, l), [
      l
    ]), s.getSnapshot !== n || m || pl !== null && pl.memoizedState.tag & 1) {
      if (i.flags |= 2048, Ii(
        9,
        { destroy: void 0 },
        dy.bind(
          null,
          i,
          s,
          u,
          n
        ),
        null
      ), Nt === null) throw Error(U(349));
      r || (Ou & 127) !== 0 || $s(i, n, u);
    }
    return u;
  }
  function $s(l, n, u) {
    l.flags |= 16384, l = { getSnapshot: n, value: u }, n = Ke.updateQueue, n === null ? (n = Ks(), Ke.updateQueue = n, n.stores = [l]) : (u = n.stores, u === null ? n.stores = [l] : u.push(l));
  }
  function dy(l, n, u, i) {
    n.value = u, n.getSnapshot = i, Vd(n) && Zd(l);
  }
  function Qd(l, n, u) {
    return u(function() {
      Vd(n) && Zd(l);
    });
  }
  function Vd(l) {
    var n = l.getSnapshot;
    l = l.value;
    try {
      var u = n();
      return !na(l, u);
    } catch {
      return !0;
    }
  }
  function Zd(l) {
    var n = ac(l, 2);
    n !== null && Oa(n, l, 2);
  }
  function hy(l) {
    var n = ql();
    if (typeof l == "function") {
      var u = l;
      if (l = u(), rc) {
        Xa(!0);
        try {
          u();
        } finally {
          Xa(!1);
        }
      }
    }
    return n.memoizedState = n.baseState = l, n.queue = {
      pending: null,
      lanes: 0,
      dispatch: null,
      lastRenderedReducer: zu,
      lastRenderedState: l
    }, n;
  }
  function wl(l, n, u, i) {
    return l.baseState = u, Xd(
      l,
      Rt,
      typeof i == "function" ? i : zu
    );
  }
  function kp(l, n, u, i, s) {
    if (Ps(l)) throw Error(U(485));
    if (l = n.action, l !== null) {
      var r = {
        payload: s,
        action: l,
        next: null,
        isTransition: !0,
        status: "pending",
        value: null,
        reason: null,
        listeners: [],
        then: function(m) {
          r.listeners.push(m);
        }
      };
      R.T !== null ? u(!0) : r.isTransition = !1, i(r), u = n.pending, u === null ? (r.next = n.pending = r, my(n, r)) : (r.next = u.next, n.pending = u.next = r);
    }
  }
  function my(l, n) {
    var u = n.action, i = n.payload, s = l.state;
    if (n.isTransition) {
      var r = R.T, m = {};
      R.T = m;
      try {
        var v = u(s, i), A = R.S;
        A !== null && A(m, v), yy(l, n, v);
      } catch (j) {
        Fi(l, n, j);
      } finally {
        r !== null && m.types !== null && (r.types = m.types), R.T = r;
      }
    } else
      try {
        r = u(s, i), yy(l, n, r);
      } catch (j) {
        Fi(l, n, j);
      }
  }
  function yy(l, n, u) {
    u !== null && typeof u == "object" && typeof u.then == "function" ? u.then(
      function(i) {
        py(l, n, i);
      },
      function(i) {
        return Fi(l, n, i);
      }
    ) : py(l, n, u);
  }
  function py(l, n, u) {
    n.status = "fulfilled", n.value = u, gy(n), l.state = u, n = l.pending, n !== null && (u = n.next, u === n ? l.pending = null : (u = u.next, n.next = u, my(l, u)));
  }
  function Fi(l, n, u) {
    var i = l.pending;
    if (l.pending = null, i !== null) {
      i = i.next;
      do
        n.status = "rejected", n.reason = u, gy(n), n = n.next;
      while (n !== i);
    }
    l.action = null;
  }
  function gy(l) {
    l = l.listeners;
    for (var n = 0; n < l.length; n++) (0, l[n])();
  }
  function ks(l, n) {
    return n;
  }
  function vy(l, n) {
    if (ot) {
      var u = Nt.formState;
      if (u !== null) {
        e: {
          var i = Ke;
          if (ot) {
            if (Lt) {
              t: {
                for (var s = Lt, r = Dl; s.nodeType !== 8; ) {
                  if (!r) {
                    s = null;
                    break t;
                  }
                  if (s = za(
                    s.nextSibling
                  ), s === null) {
                    s = null;
                    break t;
                  }
                }
                r = s.data, s = r === "F!" || r === "F" ? s : null;
              }
              if (s) {
                Lt = za(
                  s.nextSibling
                ), i = s.data === "F!";
                break e;
              }
            }
            Tn(i);
          }
          i = !1;
        }
        i && (n = u[0]);
      }
    }
    return u = ql(), u.memoizedState = u.baseState = n, i = {
      pending: null,
      lanes: 0,
      dispatch: null,
      lastRenderedReducer: ks,
      lastRenderedState: n
    }, u.queue = i, u = Id.bind(
      null,
      Ke,
      i
    ), i.dispatch = u, i = hy(!1), r = ei.bind(
      null,
      Ke,
      !1,
      i.queue
    ), i = ql(), s = {
      state: n,
      dispatch: null,
      action: l,
      pending: null
    }, i.queue = s, u = kp.bind(
      null,
      Ke,
      s,
      r,
      u
    ), s.dispatch = u, i.memoizedState = l, [n, u, !1];
  }
  function Wp(l) {
    var n = sl();
    return Ws(n, Rt, l);
  }
  function Ws(l, n, u) {
    if (n = Xd(
      l,
      n,
      ks
    )[0], l = Du(zu)[0], typeof n == "object" && n !== null && typeof n.then == "function")
      try {
        var i = Wi(n);
      } catch (m) {
        throw m === Zc ? ef : m;
      }
    else i = n;
    n = sl();
    var s = n.queue, r = s.dispatch;
    return u !== n.memoizedState && (Ke.flags |= 2048, Ii(
      9,
      { destroy: void 0 },
      Sy.bind(null, s, u),
      null
    )), [i, r, l];
  }
  function Sy(l, n) {
    l.action = n;
  }
  function by(l) {
    var n = sl(), u = Rt;
    if (u !== null)
      return Ws(n, u, l);
    sl(), n = n.memoizedState, u = sl();
    var i = u.queue.dispatch;
    return u.memoizedState = l, [n, i, !1];
  }
  function Ii(l, n, u, i) {
    return l = { tag: l, create: u, deps: i, inst: n, next: null }, n = Ke.updateQueue, n === null && (n = Ks(), Ke.updateQueue = n), u = n.lastEffect, u === null ? n.lastEffect = l.next = l : (i = u.next, u.next = l, l.next = i, n.lastEffect = l), l;
  }
  function Ey() {
    return sl().memoizedState;
  }
  function of(l, n, u, i) {
    var s = ql();
    Ke.flags |= l, s.memoizedState = Ii(
      1 | n,
      { destroy: void 0 },
      u,
      i === void 0 ? null : i
    );
  }
  function ff(l, n, u, i) {
    var s = sl();
    i = i === void 0 ? null : i;
    var r = s.memoizedState.inst;
    Rt !== null && i !== null && dc(i, Rt.memoizedState.deps) ? s.memoizedState = Ii(n, r, u, i) : (Ke.flags |= l, s.memoizedState = Ii(
      1 | n,
      r,
      u,
      i
    ));
  }
  function Jd(l, n) {
    of(8390656, 8, l, n);
  }
  function Kd(l, n) {
    ff(2048, 8, l, n);
  }
  function Ty(l) {
    Ke.flags |= 4;
    var n = Ke.updateQueue;
    if (n === null)
      n = Ks(), Ke.updateQueue = n, n.events = [l];
    else {
      var u = n.events;
      u === null ? n.events = [l] : u.push(l);
    }
  }
  function Fs(l) {
    var n = sl().memoizedState;
    return Ty({ ref: n, nextImpl: l }), function() {
      if ((St & 2) !== 0) throw Error(U(440));
      return n.impl.apply(void 0, arguments);
    };
  }
  function $d(l, n) {
    return ff(4, 2, l, n);
  }
  function Ay(l, n) {
    return ff(4, 4, l, n);
  }
  function kd(l, n) {
    if (typeof n == "function") {
      l = l();
      var u = n(l);
      return function() {
        typeof u == "function" ? u() : n(null);
      };
    }
    if (n != null)
      return l = l(), n.current = l, function() {
        n.current = null;
      };
  }
  function Oy(l, n, u) {
    u = u != null ? u.concat([l]) : null, ff(4, 4, kd.bind(null, n, l), u);
  }
  function Zn() {
  }
  function Wd(l, n) {
    var u = sl();
    n = n === void 0 ? null : n;
    var i = u.memoizedState;
    return n !== null && dc(n, i[1]) ? i[0] : (u.memoizedState = [l, n], l);
  }
  function Fp(l, n) {
    var u = sl();
    n = n === void 0 ? null : n;
    var i = u.memoizedState;
    if (n !== null && dc(n, i[1]))
      return i[0];
    if (i = l(), rc) {
      Xa(!0);
      try {
        l();
      } finally {
        Xa(!1);
      }
    }
    return u.memoizedState = [i, n], i;
  }
  function Is(l, n, u) {
    return u === void 0 || (Ou & 1073741824) !== 0 && (at & 261930) === 0 ? l.memoizedState = n : (l.memoizedState = u, l = dg(), Ke.lanes |= l, Wn |= l, u);
  }
  function Ru(l, n, u, i) {
    return na(u, n) ? u : Rl.current !== null ? (l = Is(l, u, i), na(l, n) || (gl = !0), l) : (Ou & 42) === 0 || (Ou & 1073741824) !== 0 && (at & 261930) === 0 ? (gl = !0, l.memoizedState = u) : (l = dg(), Ke.lanes |= l, Wn |= l, n);
  }
  function Fd(l, n, u, i, s) {
    var r = Z.p;
    Z.p = r !== 0 && 8 > r ? r : 8;
    var m = R.T, v = {};
    R.T = v, ei(l, !1, n, u);
    try {
      var A = s(), j = R.S;
      if (j !== null && j(v, A), A !== null && typeof A == "object" && typeof A.then == "function") {
        var V = ws(
          A,
          i
        );
        hc(
          l,
          n,
          V,
          Na(l)
        );
      } else
        hc(
          l,
          n,
          i,
          Na(l)
        );
    } catch ($) {
      hc(
        l,
        n,
        { then: function() {
        }, status: "rejected", reason: $ },
        Na()
      );
    } finally {
      Z.p = r, m !== null && v.types !== null && (m.types = v.types), R.T = m;
    }
  }
  function Ip() {
  }
  function sf(l, n, u, i) {
    if (l.tag !== 5) throw Error(U(476));
    var s = rf(l).queue;
    Fd(
      l,
      s,
      n,
      ee,
      u === null ? Ip : function() {
        return xt(l), u(i);
      }
    );
  }
  function rf(l) {
    var n = l.memoizedState;
    if (n !== null) return n;
    n = {
      memoizedState: ee,
      baseState: ee,
      baseQueue: null,
      queue: {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: zu,
        lastRenderedState: ee
      },
      next: null
    };
    var u = {};
    return n.next = {
      memoizedState: u,
      baseState: u,
      baseQueue: null,
      queue: {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: zu,
        lastRenderedState: u
      },
      next: null
    }, l.memoizedState = n, l = l.alternate, l !== null && (l.memoizedState = n), n;
  }
  function xt(l) {
    var n = rf(l);
    n.next === null && (n = l.alternate.memoizedState), hc(
      l,
      n.next.queue,
      {},
      Na()
    );
  }
  function zy() {
    return k(Rr);
  }
  function Pp() {
    return sl().memoizedState;
  }
  function Dy() {
    return sl().memoizedState;
  }
  function _u(l) {
    for (var n = l.return; n !== null; ) {
      switch (n.tag) {
        case 24:
        case 3:
          var u = Na();
          l = sc(u);
          var i = Fa(n, l, u);
          i !== null && (Oa(i, n, u), Wc(i, n, u)), n = { cache: js() }, l.payload = n;
          return;
      }
      n = n.return;
    }
  }
  function eg(l, n, u) {
    var i = Na();
    u = {
      lane: i,
      revertLane: 0,
      gesture: null,
      action: u,
      hasEagerState: !1,
      eagerState: null,
      next: null
    }, Ps(l) ? Pd(n, u) : (u = bn(l, n, u, i), u !== null && (Oa(u, l, i), Ry(u, n, i)));
  }
  function Id(l, n, u) {
    var i = Na();
    hc(l, n, u, i);
  }
  function hc(l, n, u, i) {
    var s = {
      lane: i,
      revertLane: 0,
      gesture: null,
      action: u,
      hasEagerState: !1,
      eagerState: null,
      next: null
    };
    if (Ps(l)) Pd(n, s);
    else {
      var r = l.alternate;
      if (l.lanes === 0 && (r === null || r.lanes === 0) && (r = n.lastRenderedReducer, r !== null))
        try {
          var m = n.lastRenderedState, v = r(m, u);
          if (s.hasEagerState = !0, s.eagerState = v, na(v, m))
            return Ja(l, n, s, 0), Nt === null && Za(), !1;
        } catch {
        }
      if (u = bn(l, n, s, i), u !== null)
        return Oa(u, l, i), Ry(u, n, i), !0;
    }
    return !1;
  }
  function ei(l, n, u, i) {
    if (i = {
      lane: 2,
      revertLane: zh(),
      gesture: null,
      action: i,
      hasEagerState: !1,
      eagerState: null,
      next: null
    }, Ps(l)) {
      if (n) throw Error(U(479));
    } else
      n = bn(
        l,
        u,
        i,
        2
      ), n !== null && Oa(n, l, 2);
  }
  function Ps(l) {
    var n = l.alternate;
    return l === Ke || n !== null && n === Ke;
  }
  function Pd(l, n) {
    $i = Ki = !0;
    var u = l.pending;
    u === null ? n.next = n : (n.next = u.next, u.next = n), l.pending = n;
  }
  function Ry(l, n, u) {
    if ((u & 4194048) !== 0) {
      var i = n.lanes;
      i &= l.pendingLanes, u |= i, n.lanes = u, fu(l, u);
    }
  }
  var er = {
    readContext: k,
    use: cf,
    useCallback: nl,
    useContext: nl,
    useEffect: nl,
    useImperativeHandle: nl,
    useLayoutEffect: nl,
    useInsertionEffect: nl,
    useMemo: nl,
    useReducer: nl,
    useRef: nl,
    useState: nl,
    useDebugValue: nl,
    useDeferredValue: nl,
    useTransition: nl,
    useSyncExternalStore: nl,
    useId: nl,
    useHostTransitionStatus: nl,
    useFormState: nl,
    useActionState: nl,
    useOptimistic: nl,
    useMemoCache: nl,
    useCacheRefresh: nl
  };
  er.useEffectEvent = nl;
  var tg = {
    readContext: k,
    use: cf,
    useCallback: function(l, n) {
      return ql().memoizedState = [
        l,
        n === void 0 ? null : n
      ], l;
    },
    useContext: k,
    useEffect: Jd,
    useImperativeHandle: function(l, n, u) {
      u = u != null ? u.concat([l]) : null, of(
        4194308,
        4,
        kd.bind(null, n, l),
        u
      );
    },
    useLayoutEffect: function(l, n) {
      return of(4194308, 4, l, n);
    },
    useInsertionEffect: function(l, n) {
      of(4, 2, l, n);
    },
    useMemo: function(l, n) {
      var u = ql();
      n = n === void 0 ? null : n;
      var i = l();
      if (rc) {
        Xa(!0);
        try {
          l();
        } finally {
          Xa(!1);
        }
      }
      return u.memoizedState = [i, n], i;
    },
    useReducer: function(l, n, u) {
      var i = ql();
      if (u !== void 0) {
        var s = u(n);
        if (rc) {
          Xa(!0);
          try {
            u(n);
          } finally {
            Xa(!1);
          }
        }
      } else s = n;
      return i.memoizedState = i.baseState = s, l = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: l,
        lastRenderedState: s
      }, i.queue = l, l = l.dispatch = eg.bind(
        null,
        Ke,
        l
      ), [i.memoizedState, l];
    },
    useRef: function(l) {
      var n = ql();
      return l = { current: l }, n.memoizedState = l;
    },
    useState: function(l) {
      l = hy(l);
      var n = l.queue, u = Id.bind(null, Ke, n);
      return n.dispatch = u, [l.memoizedState, u];
    },
    useDebugValue: Zn,
    useDeferredValue: function(l, n) {
      var u = ql();
      return Is(u, l, n);
    },
    useTransition: function() {
      var l = hy(!1);
      return l = Fd.bind(
        null,
        Ke,
        l.queue,
        !0,
        !1
      ), ql().memoizedState = l, [!1, l];
    },
    useSyncExternalStore: function(l, n, u) {
      var i = Ke, s = ql();
      if (ot) {
        if (u === void 0)
          throw Error(U(407));
        u = u();
      } else {
        if (u = n(), Nt === null)
          throw Error(U(349));
        (at & 127) !== 0 || $s(i, n, u);
      }
      s.memoizedState = u;
      var r = { value: u, getSnapshot: n };
      return s.queue = r, Jd(Qd.bind(null, i, r, l), [
        l
      ]), i.flags |= 2048, Ii(
        9,
        { destroy: void 0 },
        dy.bind(
          null,
          i,
          r,
          u,
          n
        ),
        null
      ), u;
    },
    useId: function() {
      var l = ql(), n = Nt.identifierPrefix;
      if (ot) {
        var u = Xn, i = Ma;
        u = (i & ~(1 << 32 - Nl(i) - 1)).toString(32) + u, n = "_" + n + "R_" + u, u = Vs++, 0 < u && (n += "H" + u.toString(32)), n += "_";
      } else
        u = Kp++, n = "_" + n + "r_" + u.toString(32) + "_";
      return l.memoizedState = n;
    },
    useHostTransitionStatus: zy,
    useFormState: vy,
    useActionState: vy,
    useOptimistic: function(l) {
      var n = ql();
      n.memoizedState = n.baseState = l;
      var u = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: null,
        lastRenderedState: null
      };
      return n.queue = u, n = ei.bind(
        null,
        Ke,
        !0,
        u
      ), u.dispatch = n, [l, n];
    },
    useMemoCache: Gd,
    useCacheRefresh: function() {
      return ql().memoizedState = _u.bind(
        null,
        Ke
      );
    },
    useEffectEvent: function(l) {
      var n = ql(), u = { impl: l };
      return n.memoizedState = u, function() {
        if ((St & 2) !== 0)
          throw Error(U(440));
        return u.impl.apply(void 0, arguments);
      };
    }
  }, eh = {
    readContext: k,
    use: cf,
    useCallback: Wd,
    useContext: k,
    useEffect: Kd,
    useImperativeHandle: Oy,
    useInsertionEffect: $d,
    useLayoutEffect: Ay,
    useMemo: Fp,
    useReducer: Du,
    useRef: Ey,
    useState: function() {
      return Du(zu);
    },
    useDebugValue: Zn,
    useDeferredValue: function(l, n) {
      var u = sl();
      return Ru(
        u,
        Rt.memoizedState,
        l,
        n
      );
    },
    useTransition: function() {
      var l = Du(zu)[0], n = sl().memoizedState;
      return [
        typeof l == "boolean" ? l : Wi(l),
        n
      ];
    },
    useSyncExternalStore: ry,
    useId: Pp,
    useHostTransitionStatus: zy,
    useFormState: Wp,
    useActionState: Wp,
    useOptimistic: function(l, n) {
      var u = sl();
      return wl(u, Rt, l, n);
    },
    useMemoCache: Gd,
    useCacheRefresh: Dy
  };
  eh.useEffectEvent = Fs;
  var lg = {
    readContext: k,
    use: cf,
    useCallback: Wd,
    useContext: k,
    useEffect: Kd,
    useImperativeHandle: Oy,
    useInsertionEffect: $d,
    useLayoutEffect: Ay,
    useMemo: Fp,
    useReducer: Ld,
    useRef: Ey,
    useState: function() {
      return Ld(zu);
    },
    useDebugValue: Zn,
    useDeferredValue: function(l, n) {
      var u = sl();
      return Rt === null ? Is(u, l, n) : Ru(
        u,
        Rt.memoizedState,
        l,
        n
      );
    },
    useTransition: function() {
      var l = Ld(zu)[0], n = sl().memoizedState;
      return [
        typeof l == "boolean" ? l : Wi(l),
        n
      ];
    },
    useSyncExternalStore: ry,
    useId: Pp,
    useHostTransitionStatus: zy,
    useFormState: by,
    useActionState: by,
    useOptimistic: function(l, n) {
      var u = sl();
      return Rt !== null ? wl(u, Rt, l, n) : (u.baseState = l, [l, u.queue.dispatch]);
    },
    useMemoCache: Gd,
    useCacheRefresh: Dy
  };
  lg.useEffectEvent = Fs;
  function Pi(l, n, u, i) {
    n = l.memoizedState, u = u(i, n), u = u == null ? n : w({}, n, u), l.memoizedState = u, l.lanes === 0 && (l.updateQueue.baseState = u);
  }
  var An = {
    enqueueSetState: function(l, n, u) {
      l = l._reactInternals;
      var i = Na(), s = sc(i);
      s.payload = n, u != null && (s.callback = u), n = Fa(l, s, i), n !== null && (Oa(n, l, i), Wc(n, l, i));
    },
    enqueueReplaceState: function(l, n, u) {
      l = l._reactInternals;
      var i = Na(), s = sc(i);
      s.tag = 1, s.payload = n, u != null && (s.callback = u), n = Fa(l, s, i), n !== null && (Oa(n, l, i), Wc(n, l, i));
    },
    enqueueForceUpdate: function(l, n) {
      l = l._reactInternals;
      var u = Na(), i = sc(u);
      i.tag = 2, n != null && (i.callback = n), n = Fa(l, i, u), n !== null && (Oa(n, l, u), Wc(n, l, u));
    }
  };
  function _y(l, n, u, i, s, r, m) {
    return l = l.stateNode, typeof l.shouldComponentUpdate == "function" ? l.shouldComponentUpdate(i, r, m) : n.prototype && n.prototype.isPureReactComponent ? !gn(u, i) || !gn(s, r) : !0;
  }
  function ag(l, n, u, i) {
    l = n.state, typeof n.componentWillReceiveProps == "function" && n.componentWillReceiveProps(u, i), typeof n.UNSAFE_componentWillReceiveProps == "function" && n.UNSAFE_componentWillReceiveProps(u, i), n.state !== l && An.enqueueReplaceState(n, n.state, null);
  }
  function ti(l, n) {
    var u = n;
    if ("ref" in n) {
      u = {};
      for (var i in n)
        i !== "ref" && (u[i] = n[i]);
    }
    if (l = l.defaultProps) {
      u === n && (u = w({}, u));
      for (var s in l)
        u[s] === void 0 && (u[s] = l[s]);
    }
    return u;
  }
  function th(l) {
    Yi(l);
  }
  function My(l) {
    console.error(l);
  }
  function lh(l) {
    Yi(l);
  }
  function df(l, n) {
    try {
      var u = l.onUncaughtError;
      u(n.value, { componentStack: n.stack });
    } catch (i) {
      setTimeout(function() {
        throw i;
      });
    }
  }
  function tr(l, n, u) {
    try {
      var i = l.onCaughtError;
      i(u.value, {
        componentStack: u.stack,
        errorBoundary: n.tag === 1 ? n.stateNode : null
      });
    } catch (s) {
      setTimeout(function() {
        throw s;
      });
    }
  }
  function Cy(l, n, u) {
    return u = sc(u), u.tag = 3, u.payload = { element: null }, u.callback = function() {
      df(l, n);
    }, u;
  }
  function Uy(l) {
    return l = sc(l), l.tag = 3, l;
  }
  function xy(l, n, u, i) {
    var s = u.type.getDerivedStateFromError;
    if (typeof s == "function") {
      var r = i.value;
      l.payload = function() {
        return s(r);
      }, l.callback = function() {
        tr(n, u, i);
      };
    }
    var m = u.stateNode;
    m !== null && typeof m.componentDidCatch == "function" && (l.callback = function() {
      tr(n, u, i), typeof s != "function" && (Pt === null ? Pt = /* @__PURE__ */ new Set([this]) : Pt.add(this));
      var v = i.stack;
      this.componentDidCatch(i.value, {
        componentStack: v !== null ? v : ""
      });
    });
  }
  function i1(l, n, u, i, s) {
    if (u.flags |= 32768, i !== null && typeof i == "object" && typeof i.then == "function") {
      if (n = u.alternate, n !== null && Yl(
        n,
        u,
        s,
        !0
      ), u = ga.current, u !== null) {
        switch (u.tag) {
          case 31:
          case 13:
            return Ia === null ? Eh() : u.alternate === null && Vt === 0 && (Vt = 3), u.flags &= -257, u.flags |= 65536, u.lanes = s, i === Vi ? u.flags |= 16384 : (n = u.updateQueue, n === null ? u.updateQueue = /* @__PURE__ */ new Set([i]) : n.add(i), yr(l, i, s)), !1;
          case 22:
            return u.flags |= 65536, i === Vi ? u.flags |= 16384 : (n = u.updateQueue, n === null ? (n = {
              transitions: null,
              markerInstances: null,
              retryQueue: /* @__PURE__ */ new Set([i])
            }, u.updateQueue = n) : (u = n.retryQueue, u === null ? n.retryQueue = /* @__PURE__ */ new Set([i]) : u.add(i)), yr(l, i, s)), !1;
        }
        throw Error(U(435, u.tag));
      }
      return yr(l, i, s), Eh(), !1;
    }
    if (ot)
      return n = ga.current, n !== null ? ((n.flags & 65536) === 0 && (n.flags |= 256), n.flags |= 65536, n.lanes = s, i !== Su && (l = Error(U(422), { cause: i }), Io(Ka(l, u)))) : (i !== Su && (n = Error(U(423), {
        cause: i
      }), Io(
        Ka(n, u)
      )), l = l.current.alternate, l.flags |= 65536, s &= -s, l.lanes |= s, i = Ka(i, u), s = Cy(
        l.stateNode,
        i,
        s
      ), jd(l, s), Vt !== 4 && (Vt = 2)), !1;
    var r = Error(U(520), { cause: i });
    if (r = Ka(r, u), rr === null ? rr = [r] : rr.push(r), Vt !== 4 && (Vt = 2), n === null) return !0;
    i = Ka(i, u), u = n;
    do {
      switch (u.tag) {
        case 3:
          return u.flags |= 65536, l = s & -s, u.lanes |= l, l = Cy(u.stateNode, i, l), jd(u, l), !1;
        case 1:
          if (n = u.type, r = u.stateNode, (u.flags & 128) === 0 && (typeof n.getDerivedStateFromError == "function" || r !== null && typeof r.componentDidCatch == "function" && (Pt === null || !Pt.has(r))))
            return u.flags |= 65536, s &= -s, u.lanes |= s, s = Uy(s), xy(
              s,
              l,
              u,
              i
            ), jd(u, s), !1;
      }
      u = u.return;
    } while (u !== null);
    return !1;
  }
  var ah = Error(U(461)), gl = !1;
  function kt(l, n, u, i) {
    n.child = l === null ? fy(n, null, u, i) : kc(
      n,
      l.child,
      u,
      i
    );
  }
  function Ny(l, n, u, i, s) {
    u = u.render;
    var r = n.ref;
    if ("ref" in i) {
      var m = {};
      for (var v in i)
        v !== "ref" && (m[v] = i[v]);
    } else m = i;
    return Ye(n), i = Zs(
      l,
      n,
      u,
      m,
      r,
      s
    ), v = wd(), l !== null && !gl ? (ki(l, n, s), tn(l, n, s)) : (ot && v && Wo(n), n.flags |= 1, kt(l, n, i, s), n.child);
  }
  function Hy(l, n, u, i, s) {
    if (l === null) {
      var r = u.type;
      return typeof r == "function" && !qi(r) && r.defaultProps === void 0 && u.compare === null ? (n.tag = 15, n.type = r, jy(
        l,
        n,
        r,
        i,
        s
      )) : (l = _d(
        u.type,
        null,
        i,
        n,
        n.mode,
        s
      ), l.ref = n.ref, l.return = n, n.child = l);
    }
    if (r = l.child, !ch(l, s)) {
      var m = r.memoizedProps;
      if (u = u.compare, u = u !== null ? u : gn, u(m, i) && l.ref === n.ref)
        return tn(l, n, s);
    }
    return n.flags |= 1, l = nc(r, i), l.ref = n.ref, l.return = n, n.child = l;
  }
  function jy(l, n, u, i, s) {
    if (l !== null) {
      var r = l.memoizedProps;
      if (gn(r, i) && l.ref === n.ref)
        if (gl = !1, n.pendingProps = i = r, ch(l, s))
          (l.flags & 131072) !== 0 && (gl = !0);
        else
          return n.lanes = l.lanes, tn(l, n, s);
    }
    return nh(
      l,
      n,
      u,
      i,
      s
    );
  }
  function ng(l, n, u, i) {
    var s = i.children, r = l !== null ? l.memoizedState : null;
    if (l === null && n.stateNode === null && (n.stateNode = {
      _visibility: 1,
      _pendingMarkers: null,
      _retryCache: null,
      _transitions: null
    }), i.mode === "hidden") {
      if ((n.flags & 128) !== 0) {
        if (r = r !== null ? r.baseLanes | u : u, l !== null) {
          for (i = n.child = l.child, s = 0; i !== null; )
            s = s | i.lanes | i.childLanes, i = i.sibling;
          i = s & ~r;
        } else i = 0, n.child = null;
        return Sa(
          l,
          n,
          r,
          u,
          i
        );
      }
      if ((u & 536870912) !== 0)
        n.memoizedState = { baseLanes: 0, cachePool: null }, l !== null && Po(
          n,
          r !== null ? r.cachePool : null
        ), r !== null ? Jp(n, r) : Qs(), Yd(n);
      else
        return i = n.lanes = 536870912, Sa(
          l,
          n,
          r !== null ? r.baseLanes | u : u,
          u,
          i
        );
    } else
      r !== null ? (Po(n, r.cachePool), Jp(n, r), Vn(), n.memoizedState = null) : (l !== null && Po(n, null), Qs(), Vn());
    return kt(l, n, s, u), n.child;
  }
  function li(l, n) {
    return l !== null && l.tag === 22 || n.stateNode !== null || (n.stateNode = {
      _visibility: 1,
      _pendingMarkers: null,
      _retryCache: null,
      _transitions: null
    }), n.sibling;
  }
  function Sa(l, n, u, i, s) {
    var r = Wa();
    return r = r === null ? null : { parent: yl._currentValue, pool: r }, n.memoizedState = {
      baseLanes: u,
      cachePool: r
    }, l !== null && Po(n, null), Qs(), Yd(n), l !== null && Yl(l, n, i, !0), n.childLanes = s, null;
  }
  function lr(l, n) {
    return n = ur(
      { mode: n.mode, children: n.children },
      l.mode
    ), n.ref = l.ref, l.child = n, n.return = l, n;
  }
  function ba(l, n, u) {
    return kc(n, l.child, null, u), l = lr(n, n.pendingProps), l.flags |= 2, va(n), n.memoizedState = null, l;
  }
  function ug(l, n, u) {
    var i = n.pendingProps, s = (n.flags & 128) !== 0;
    if (n.flags &= -129, l === null) {
      if (ot) {
        if (i.mode === "hidden")
          return l = lr(n, i), n.lanes = 536870912, li(null, l);
        if (af(n), (l = Lt) ? (l = Gg(
          l,
          Dl
        ), l = l !== null && l.data === "&" ? l : null, l !== null && (n.memoizedState = {
          dehydrated: l,
          treeContext: Gn !== null ? { id: Ma, overflow: Xn } : null,
          retryLane: 536870912,
          hydrationErrors: null
        }, u = ey(l), u.return = n, n.child = u, Bl = n, Lt = null)) : l = null, l === null) throw Tn(n);
        return n.lanes = 536870912, null;
      }
      return lr(n, i);
    }
    var r = l.memoizedState;
    if (r !== null) {
      var m = r.dehydrated;
      if (af(n), s)
        if (n.flags & 256)
          n.flags &= -257, n = ba(
            l,
            n,
            u
          );
        else if (n.memoizedState !== null)
          n.child = l.child, n.flags |= 128, n = null;
        else throw Error(U(558));
      else if (gl || Yl(l, n, u, !1), s = (u & l.childLanes) !== 0, gl || s) {
        if (i = Nt, i !== null && (m = La(i, u), m !== 0 && m !== r.retryLane))
          throw r.retryLane = m, ac(l, m), Oa(i, l, m), ah;
        Eh(), n = ba(
          l,
          n,
          u
        );
      } else
        l = r.treeContext, Lt = za(m.nextSibling), Bl = n, ot = !0, vu = null, Dl = !1, l !== null && xs(n, l), n = lr(n, i), n.flags |= 4096;
      return n;
    }
    return l = nc(l.child, {
      mode: i.mode,
      children: i.children
    }), l.ref = n.ref, n.child = l, l.return = n, l;
  }
  function Pa(l, n) {
    var u = n.ref;
    if (u === null)
      l !== null && l.ref !== null && (n.flags |= 4194816);
    else {
      if (typeof u != "function" && typeof u != "object")
        throw Error(U(284));
      (l === null || l.ref !== u) && (n.flags |= 4194816);
    }
  }
  function nh(l, n, u, i, s) {
    return Ye(n), u = Zs(
      l,
      n,
      u,
      i,
      void 0,
      s
    ), i = wd(), l !== null && !gl ? (ki(l, n, s), tn(l, n, s)) : (ot && i && Wo(n), n.flags |= 1, kt(l, n, u, s), n.child);
  }
  function ai(l, n, u, i, s, r) {
    return Ye(n), n.updateQueue = null, u = $p(
      n,
      i,
      u,
      s
    ), qd(l), i = wd(), l !== null && !gl ? (ki(l, n, r), tn(l, n, r)) : (ot && i && Wo(n), n.flags |= 1, kt(l, n, u, r), n.child);
  }
  function By(l, n, u, i, s) {
    if (Ye(n), n.stateNode === null) {
      var r = ma, m = u.contextType;
      typeof m == "object" && m !== null && (r = k(m)), r = new u(i, r), n.memoizedState = r.state !== null && r.state !== void 0 ? r.state : null, r.updater = An, n.stateNode = r, r._reactInternals = n, r = n.stateNode, r.props = i, r.state = n.memoizedState, r.refs = {}, Ls(n), m = u.contextType, r.context = typeof m == "object" && m !== null ? k(m) : ma, r.state = n.memoizedState, m = u.getDerivedStateFromProps, typeof m == "function" && (Pi(
        n,
        u,
        m,
        i
      ), r.state = n.memoizedState), typeof u.getDerivedStateFromProps == "function" || typeof r.getSnapshotBeforeUpdate == "function" || typeof r.UNSAFE_componentWillMount != "function" && typeof r.componentWillMount != "function" || (m = r.state, typeof r.componentWillMount == "function" && r.componentWillMount(), typeof r.UNSAFE_componentWillMount == "function" && r.UNSAFE_componentWillMount(), m !== r.state && An.enqueueReplaceState(r, r.state, null), Tu(n, i, r, s), Fc(), r.state = n.memoizedState), typeof r.componentDidMount == "function" && (n.flags |= 4194308), i = !0;
    } else if (l === null) {
      r = n.stateNode;
      var v = n.memoizedProps, A = ti(u, v);
      r.props = A;
      var j = r.context, V = u.contextType;
      m = ma, typeof V == "object" && V !== null && (m = k(V));
      var $ = u.getDerivedStateFromProps;
      V = typeof $ == "function" || typeof r.getSnapshotBeforeUpdate == "function", v = n.pendingProps !== v, V || typeof r.UNSAFE_componentWillReceiveProps != "function" && typeof r.componentWillReceiveProps != "function" || (v || j !== m) && ag(
        n,
        r,
        i,
        m
      ), fc = !1;
      var B = n.memoizedState;
      r.state = B, Tu(n, i, r, s), Fc(), j = n.memoizedState, v || B !== j || fc ? (typeof $ == "function" && (Pi(
        n,
        u,
        $,
        i
      ), j = n.memoizedState), (A = fc || _y(
        n,
        u,
        A,
        i,
        B,
        j,
        m
      )) ? (V || typeof r.UNSAFE_componentWillMount != "function" && typeof r.componentWillMount != "function" || (typeof r.componentWillMount == "function" && r.componentWillMount(), typeof r.UNSAFE_componentWillMount == "function" && r.UNSAFE_componentWillMount()), typeof r.componentDidMount == "function" && (n.flags |= 4194308)) : (typeof r.componentDidMount == "function" && (n.flags |= 4194308), n.memoizedProps = i, n.memoizedState = j), r.props = i, r.state = j, r.context = m, i = A) : (typeof r.componentDidMount == "function" && (n.flags |= 4194308), i = !1);
    } else {
      r = n.stateNode, Hd(l, n), m = n.memoizedProps, V = ti(u, m), r.props = V, $ = n.pendingProps, B = r.context, j = u.contextType, A = ma, typeof j == "object" && j !== null && (A = k(j)), v = u.getDerivedStateFromProps, (j = typeof v == "function" || typeof r.getSnapshotBeforeUpdate == "function") || typeof r.UNSAFE_componentWillReceiveProps != "function" && typeof r.componentWillReceiveProps != "function" || (m !== $ || B !== A) && ag(
        n,
        r,
        i,
        A
      ), fc = !1, B = n.memoizedState, r.state = B, Tu(n, i, r, s), Fc();
      var X = n.memoizedState;
      m !== $ || B !== X || fc || l !== null && l.dependencies !== null && Gi(l.dependencies) ? (typeof v == "function" && (Pi(
        n,
        u,
        v,
        i
      ), X = n.memoizedState), (V = fc || _y(
        n,
        u,
        V,
        i,
        B,
        X,
        A
      ) || l !== null && l.dependencies !== null && Gi(l.dependencies)) ? (j || typeof r.UNSAFE_componentWillUpdate != "function" && typeof r.componentWillUpdate != "function" || (typeof r.componentWillUpdate == "function" && r.componentWillUpdate(i, X, A), typeof r.UNSAFE_componentWillUpdate == "function" && r.UNSAFE_componentWillUpdate(
        i,
        X,
        A
      )), typeof r.componentDidUpdate == "function" && (n.flags |= 4), typeof r.getSnapshotBeforeUpdate == "function" && (n.flags |= 1024)) : (typeof r.componentDidUpdate != "function" || m === l.memoizedProps && B === l.memoizedState || (n.flags |= 4), typeof r.getSnapshotBeforeUpdate != "function" || m === l.memoizedProps && B === l.memoizedState || (n.flags |= 1024), n.memoizedProps = i, n.memoizedState = X), r.props = i, r.state = X, r.context = A, i = V) : (typeof r.componentDidUpdate != "function" || m === l.memoizedProps && B === l.memoizedState || (n.flags |= 4), typeof r.getSnapshotBeforeUpdate != "function" || m === l.memoizedProps && B === l.memoizedState || (n.flags |= 1024), i = !1);
    }
    return r = i, Pa(l, n), i = (n.flags & 128) !== 0, r || i ? (r = n.stateNode, u = i && typeof u.getDerivedStateFromError != "function" ? null : r.render(), n.flags |= 1, l !== null && i ? (n.child = kc(
      n,
      l.child,
      null,
      s
    ), n.child = kc(
      n,
      null,
      u,
      s
    )) : kt(l, n, u, s), n.memoizedState = r.state, l = n.child) : l = tn(
      l,
      n,
      s
    ), l;
  }
  function Jn(l, n, u, i) {
    return Qc(), n.flags |= 256, kt(l, n, u, i), n.child;
  }
  var ar = {
    dehydrated: null,
    treeContext: null,
    retryLane: 0,
    hydrationErrors: null
  };
  function nr(l) {
    return { baseLanes: l, cachePool: Li() };
  }
  function en(l, n, u) {
    return l = l !== null ? l.childLanes & ~u : 0, n && (l |= Aa), l;
  }
  function Yy(l, n, u) {
    var i = n.pendingProps, s = !1, r = (n.flags & 128) !== 0, m;
    if ((m = r) || (m = l !== null && l.memoizedState === null ? !1 : (It.current & 2) !== 0), m && (s = !0, n.flags &= -129), m = (n.flags & 32) !== 0, n.flags &= -33, l === null) {
      if (ot) {
        if (s ? Au(n) : Vn(), (l = Lt) ? (l = Gg(
          l,
          Dl
        ), l = l !== null && l.data !== "&" ? l : null, l !== null && (n.memoizedState = {
          dehydrated: l,
          treeContext: Gn !== null ? { id: Ma, overflow: Xn } : null,
          retryLane: 536870912,
          hydrationErrors: null
        }, u = ey(l), u.return = n, n.child = u, Bl = n, Lt = null)) : l = null, l === null) throw Tn(n);
        return si(l) ? n.lanes = 32 : n.lanes = 536870912, null;
      }
      var v = i.children;
      return i = i.fallback, s ? (Vn(), s = n.mode, v = ur(
        { mode: "hidden", children: v },
        s
      ), i = uc(
        i,
        s,
        u,
        null
      ), v.return = n, i.return = n, v.sibling = i, n.child = v, i = n.child, i.memoizedState = nr(u), i.childLanes = en(
        l,
        m,
        u
      ), n.memoizedState = ar, li(null, i)) : (Au(n), ni(n, v));
    }
    var A = l.memoizedState;
    if (A !== null && (v = A.dehydrated, v !== null)) {
      if (r)
        n.flags & 256 ? (Au(n), n.flags &= -257, n = eo(
          l,
          n,
          u
        )) : n.memoizedState !== null ? (Vn(), n.child = l.child, n.flags |= 128, n = null) : (Vn(), v = i.fallback, s = n.mode, i = ur(
          { mode: "visible", children: i.children },
          s
        ), v = uc(
          v,
          s,
          u,
          null
        ), v.flags |= 2, i.return = n, v.return = n, i.sibling = v, n.child = i, kc(
          n,
          l.child,
          null,
          u
        ), i = n.child, i.memoizedState = nr(u), i.childLanes = en(
          l,
          m,
          u
        ), n.memoizedState = ar, n = li(null, i));
      else if (Au(n), si(v)) {
        if (m = v.nextSibling && v.nextSibling.dataset, m) var j = m.dgst;
        m = j, i = Error(U(419)), i.stack = "", i.digest = m, Io({ value: i, source: null, stack: null }), n = eo(
          l,
          n,
          u
        );
      } else if (gl || Yl(l, n, u, !1), m = (u & l.childLanes) !== 0, gl || m) {
        if (m = Nt, m !== null && (i = La(m, u), i !== 0 && i !== A.retryLane))
          throw A.retryLane = i, ac(l, i), Oa(m, l, i), ah;
        Dn(v) || Eh(), n = eo(
          l,
          n,
          u
        );
      } else
        Dn(v) ? (n.flags |= 192, n.child = l.child, n = null) : (l = A.treeContext, Lt = za(
          v.nextSibling
        ), Bl = n, ot = !0, vu = null, Dl = !1, l !== null && xs(n, l), n = ni(
          n,
          i.children
        ), n.flags |= 4096);
      return n;
    }
    return s ? (Vn(), v = i.fallback, s = n.mode, A = l.child, j = A.sibling, i = nc(A, {
      mode: "hidden",
      children: i.children
    }), i.subtreeFlags = A.subtreeFlags & 65011712, j !== null ? v = nc(
      j,
      v
    ) : (v = uc(
      v,
      s,
      u,
      null
    ), v.flags |= 2), v.return = n, i.return = n, i.sibling = v, n.child = i, li(null, i), i = n.child, v = l.child.memoizedState, v === null ? v = nr(u) : (s = v.cachePool, s !== null ? (A = yl._currentValue, s = s.parent !== A ? { parent: A, pool: A } : s) : s = Li(), v = {
      baseLanes: v.baseLanes | u,
      cachePool: s
    }), i.memoizedState = v, i.childLanes = en(
      l,
      m,
      u
    ), n.memoizedState = ar, li(l.child, i)) : (Au(n), u = l.child, l = u.sibling, u = nc(u, {
      mode: "visible",
      children: i.children
    }), u.return = n, u.sibling = null, l !== null && (m = n.deletions, m === null ? (n.deletions = [l], n.flags |= 16) : m.push(l)), n.child = u, n.memoizedState = null, u);
  }
  function ni(l, n) {
    return n = ur(
      { mode: "visible", children: n },
      l.mode
    ), n.return = l, l.child = n;
  }
  function ur(l, n) {
    return l = ol(22, l, null, n), l.lanes = 0, l;
  }
  function eo(l, n, u) {
    return kc(n, l.child, null, u), l = ni(
      n,
      n.pendingProps.children
    ), l.flags |= 2, n.memoizedState = null, l;
  }
  function to(l, n, u) {
    l.lanes |= n;
    var i = l.alternate;
    i !== null && (i.lanes |= n), xd(l.return, n, u);
  }
  function uh(l, n, u, i, s, r) {
    var m = l.memoizedState;
    m === null ? l.memoizedState = {
      isBackwards: n,
      rendering: null,
      renderingStartTime: 0,
      last: i,
      tail: u,
      tailMode: s,
      treeForkCount: r
    } : (m.isBackwards = n, m.rendering = null, m.renderingStartTime = 0, m.last = i, m.tail = u, m.tailMode = s, m.treeForkCount = r);
  }
  function qy(l, n, u) {
    var i = n.pendingProps, s = i.revealOrder, r = i.tail;
    i = i.children;
    var m = It.current, v = (m & 2) !== 0;
    if (v ? (m = m & 1 | 2, n.flags |= 128) : m &= 1, I(It, m), kt(l, n, i, u), i = ot ? ml : 0, !v && l !== null && (l.flags & 128) !== 0)
      e: for (l = n.child; l !== null; ) {
        if (l.tag === 13)
          l.memoizedState !== null && to(l, u, n);
        else if (l.tag === 19)
          to(l, u, n);
        else if (l.child !== null) {
          l.child.return = l, l = l.child;
          continue;
        }
        if (l === n) break e;
        for (; l.sibling === null; ) {
          if (l.return === null || l.return === n)
            break e;
          l = l.return;
        }
        l.sibling.return = l.return, l = l.sibling;
      }
    switch (s) {
      case "forwards":
        for (u = n.child, s = null; u !== null; )
          l = u.alternate, l !== null && nf(l) === null && (s = u), u = u.sibling;
        u = s, u === null ? (s = n.child, n.child = null) : (s = u.sibling, u.sibling = null), uh(
          n,
          !1,
          s,
          u,
          r,
          i
        );
        break;
      case "backwards":
      case "unstable_legacy-backwards":
        for (u = null, s = n.child, n.child = null; s !== null; ) {
          if (l = s.alternate, l !== null && nf(l) === null) {
            n.child = s;
            break;
          }
          l = s.sibling, s.sibling = u, u = s, s = l;
        }
        uh(
          n,
          !0,
          u,
          null,
          r,
          i
        );
        break;
      case "together":
        uh(
          n,
          !1,
          null,
          null,
          void 0,
          i
        );
        break;
      default:
        n.memoizedState = null;
    }
    return n.child;
  }
  function tn(l, n, u) {
    if (l !== null && (n.dependencies = l.dependencies), Wn |= n.lanes, (u & n.childLanes) === 0)
      if (l !== null) {
        if (Yl(
          l,
          n,
          u,
          !1
        ), (u & n.childLanes) === 0)
          return null;
      } else return null;
    if (l !== null && n.child !== l.child)
      throw Error(U(153));
    if (n.child !== null) {
      for (l = n.child, u = nc(l, l.pendingProps), n.child = u, u.return = n; l.sibling !== null; )
        l = l.sibling, u = u.sibling = nc(l, l.pendingProps), u.return = n;
      u.sibling = null;
    }
    return n.child;
  }
  function ch(l, n) {
    return (l.lanes & n) !== 0 ? !0 : (l = l.dependencies, !!(l !== null && Gi(l)));
  }
  function ih(l, n, u) {
    switch (n.tag) {
      case 3:
        $t(n, n.stateNode.containerInfo), pa(n, yl, l.memoizedState.cache), Qc();
        break;
      case 27:
      case 5:
        wa(n);
        break;
      case 4:
        $t(n, n.stateNode.containerInfo);
        break;
      case 10:
        pa(
          n,
          n.type,
          n.memoizedProps.value
        );
        break;
      case 31:
        if (n.memoizedState !== null)
          return n.flags |= 128, af(n), null;
        break;
      case 13:
        var i = n.memoizedState;
        if (i !== null)
          return i.dehydrated !== null ? (Au(n), n.flags |= 128, null) : (u & n.child.childLanes) !== 0 ? Yy(l, n, u) : (Au(n), l = tn(
            l,
            n,
            u
          ), l !== null ? l.sibling : null);
        Au(n);
        break;
      case 19:
        var s = (l.flags & 128) !== 0;
        if (i = (u & n.childLanes) !== 0, i || (Yl(
          l,
          n,
          u,
          !1
        ), i = (u & n.childLanes) !== 0), s) {
          if (i)
            return qy(
              l,
              n,
              u
            );
          n.flags |= 128;
        }
        if (s = n.memoizedState, s !== null && (s.rendering = null, s.tail = null, s.lastEffect = null), I(It, It.current), i) break;
        return null;
      case 22:
        return n.lanes = 0, ng(
          l,
          n,
          u,
          n.pendingProps
        );
      case 24:
        pa(n, yl, l.memoizedState.cache);
    }
    return tn(l, n, u);
  }
  function wy(l, n, u) {
    if (l !== null)
      if (l.memoizedProps !== n.pendingProps)
        gl = !0;
      else {
        if (!ch(l, u) && (n.flags & 128) === 0)
          return gl = !1, ih(
            l,
            n,
            u
          );
        gl = (l.flags & 131072) !== 0;
      }
    else
      gl = !1, ot && (n.flags & 1048576) !== 0 && ly(n, ml, n.index);
    switch (n.lanes = 0, n.tag) {
      case 16:
        e: {
          var i = n.pendingProps;
          if (l = Jc(n.elementType), n.type = l, typeof l == "function")
            qi(l) ? (i = ti(l, i), n.tag = 1, n = By(
              null,
              n,
              l,
              i,
              u
            )) : (n.tag = 0, n = nh(
              null,
              n,
              l,
              i,
              u
            ));
          else {
            if (l != null) {
              var s = l.$$typeof;
              if (s === Ct) {
                n.tag = 11, n = Ny(
                  null,
                  n,
                  l,
                  i,
                  u
                );
                break e;
              } else if (s === Ae) {
                n.tag = 14, n = Hy(
                  null,
                  n,
                  l,
                  i,
                  u
                );
                break e;
              }
            }
            throw n = Kt(l) || l, Error(U(306, n, ""));
          }
        }
        return n;
      case 0:
        return nh(
          l,
          n,
          n.type,
          n.pendingProps,
          u
        );
      case 1:
        return i = n.type, s = ti(
          i,
          n.pendingProps
        ), By(
          l,
          n,
          i,
          s,
          u
        );
      case 3:
        e: {
          if ($t(
            n,
            n.stateNode.containerInfo
          ), l === null) throw Error(U(387));
          i = n.pendingProps;
          var r = n.memoizedState;
          s = r.element, Hd(l, n), Tu(n, i, null, u);
          var m = n.memoizedState;
          if (i = m.cache, pa(n, yl, i), i !== r.cache && Eu(
            n,
            [yl],
            u,
            !0
          ), Fc(), i = m.element, r.isDehydrated)
            if (r = {
              element: i,
              isDehydrated: !1,
              cache: m.cache
            }, n.updateQueue.baseState = r, n.memoizedState = r, n.flags & 256) {
              n = Jn(
                l,
                n,
                i,
                u
              );
              break e;
            } else if (i !== s) {
              s = Ka(
                Error(U(424)),
                n
              ), Io(s), n = Jn(
                l,
                n,
                i,
                u
              );
              break e;
            } else
              for (l = n.stateNode.containerInfo, l.nodeType === 9 ? l = l.body : l = l.nodeName === "HTML" ? l.ownerDocument.body : l, Lt = za(l.firstChild), Bl = n, ot = !0, vu = null, Dl = !0, u = fy(
                n,
                null,
                i,
                u
              ), n.child = u; u; )
                u.flags = u.flags & -3 | 4096, u = u.sibling;
          else {
            if (Qc(), i === s) {
              n = tn(
                l,
                n,
                u
              );
              break e;
            }
            kt(l, n, i, u);
          }
          n = n.child;
        }
        return n;
      case 26:
        return Pa(l, n), l === null ? (u = Hf(
          n.type,
          null,
          n.pendingProps,
          null
        )) ? n.memoizedState = u : ot || (u = n.type, l = n.pendingProps, i = fi(
          Le.current
        ).createElement(u), i[Ut] = n, i[ra] = l, Wl(i, u, l), zt(i), n.stateNode = i) : n.memoizedState = Hf(
          n.type,
          l.memoizedProps,
          n.pendingProps,
          l.memoizedState
        ), null;
      case 27:
        return wa(n), l === null && ot && (i = n.stateNode = xf(
          n.type,
          n.pendingProps,
          Le.current
        ), Bl = n, Dl = !0, s = Lt, In(n.type) ? (Or = s, Lt = za(i.firstChild)) : Lt = s), kt(
          l,
          n,
          n.pendingProps.children,
          u
        ), Pa(l, n), l === null && (n.flags |= 4194304), n.child;
      case 5:
        return l === null && ot && ((s = i = Lt) && (i = s1(
          i,
          n.type,
          n.pendingProps,
          Dl
        ), i !== null ? (n.stateNode = i, Bl = n, Lt = za(i.firstChild), Dl = !1, s = !0) : s = !1), s || Tn(n)), wa(n), s = n.type, r = n.pendingProps, m = l !== null ? l.memoizedProps : null, i = r.children, Cf(s, r) ? i = null : m !== null && Cf(s, m) && (n.flags |= 32), n.memoizedState !== null && (s = Zs(
          l,
          n,
          c1,
          null,
          null,
          u
        ), Rr._currentValue = s), Pa(l, n), kt(l, n, i, u), n.child;
      case 6:
        return l === null && ot && ((l = u = Lt) && (u = Ie(
          u,
          n.pendingProps,
          Dl
        ), u !== null ? (n.stateNode = u, Bl = n, Lt = null, l = !0) : l = !1), l || Tn(n)), null;
      case 13:
        return Yy(l, n, u);
      case 4:
        return $t(
          n,
          n.stateNode.containerInfo
        ), i = n.pendingProps, l === null ? n.child = kc(
          n,
          null,
          i,
          u
        ) : kt(l, n, i, u), n.child;
      case 11:
        return Ny(
          l,
          n,
          n.type,
          n.pendingProps,
          u
        );
      case 7:
        return kt(
          l,
          n,
          n.pendingProps,
          u
        ), n.child;
      case 8:
        return kt(
          l,
          n,
          n.pendingProps.children,
          u
        ), n.child;
      case 12:
        return kt(
          l,
          n,
          n.pendingProps.children,
          u
        ), n.child;
      case 10:
        return i = n.pendingProps, pa(n, n.type, i.value), kt(l, n, i.children, u), n.child;
      case 9:
        return s = n.type._context, i = n.pendingProps.children, Ye(n), s = k(s), i = i(s), n.flags |= 1, kt(l, n, i, u), n.child;
      case 14:
        return Hy(
          l,
          n,
          n.type,
          n.pendingProps,
          u
        );
      case 15:
        return jy(
          l,
          n,
          n.type,
          n.pendingProps,
          u
        );
      case 19:
        return qy(l, n, u);
      case 31:
        return ug(l, n, u);
      case 22:
        return ng(
          l,
          n,
          u,
          n.pendingProps
        );
      case 24:
        return Ye(n), i = k(yl), l === null ? (s = Wa(), s === null && (s = Nt, r = js(), s.pooledCache = r, r.refCount++, r !== null && (s.pooledCacheLanes |= u), s = r), n.memoizedState = { parent: i, cache: s }, Ls(n), pa(n, yl, s)) : ((l.lanes & u) !== 0 && (Hd(l, n), Tu(n, null, null, u), Fc()), s = l.memoizedState, r = n.memoizedState, s.parent !== i ? (s = { parent: i, cache: i }, n.memoizedState = s, n.lanes === 0 && (n.memoizedState = n.updateQueue.baseState = s), pa(n, yl, i)) : (i = r.cache, pa(n, yl, i), i !== s.cache && Eu(
          n,
          [yl],
          u,
          !0
        ))), kt(
          l,
          n,
          n.pendingProps.children,
          u
        ), n.child;
      case 29:
        throw n.pendingProps;
    }
    throw Error(U(156, n.tag));
  }
  function Mu(l) {
    l.flags |= 4;
  }
  function Gy(l, n, u, i, s) {
    if ((n = (l.mode & 32) !== 0) && (n = !1), n) {
      if (l.flags |= 16777216, (s & 335544128) === s)
        if (l.stateNode.complete) l.flags |= 8192;
        else if (yg()) l.flags |= 8192;
        else
          throw Kc = Vi, Qi;
    } else l.flags &= -16777217;
  }
  function Xy(l, n) {
    if (n.type !== "stylesheet" || (n.state.loading & 4) !== 0)
      l.flags &= -16777217;
    else if (l.flags |= 16777216, !ja(n))
      if (yg()) l.flags |= 8192;
      else
        throw Kc = Vi, Qi;
  }
  function ua(l, n) {
    n !== null && (l.flags |= 4), l.flags & 16384 && (n = l.tag !== 22 ? la() : 536870912, l.lanes |= n, ul |= n);
  }
  function hf(l, n) {
    if (!ot)
      switch (l.tailMode) {
        case "hidden":
          n = l.tail;
          for (var u = null; n !== null; )
            n.alternate !== null && (u = n), n = n.sibling;
          u === null ? l.tail = null : u.sibling = null;
          break;
        case "collapsed":
          u = l.tail;
          for (var i = null; u !== null; )
            u.alternate !== null && (i = u), u = u.sibling;
          i === null ? n || l.tail === null ? l.tail = null : l.tail.sibling = null : i.sibling = null;
      }
  }
  function je(l) {
    var n = l.alternate !== null && l.alternate.child === l.child, u = 0, i = 0;
    if (n)
      for (var s = l.child; s !== null; )
        u |= s.lanes | s.childLanes, i |= s.subtreeFlags & 65011712, i |= s.flags & 65011712, s.return = l, s = s.sibling;
    else
      for (s = l.child; s !== null; )
        u |= s.lanes | s.childLanes, i |= s.subtreeFlags, i |= s.flags, s.return = l, s = s.sibling;
    return l.subtreeFlags |= i, l.childLanes = u, n;
  }
  function cg(l, n, u) {
    var i = n.pendingProps;
    switch (Cd(n), n.tag) {
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return je(n), null;
      case 1:
        return je(n), null;
      case 3:
        return u = n.stateNode, i = null, l !== null && (i = l.memoizedState.cache), n.memoizedState.cache !== i && (n.flags |= 2048), Qn(yl), gt(), u.pendingContext && (u.context = u.pendingContext, u.pendingContext = null), (l === null || l.child === null) && (bu(n) ? Mu(n) : l === null || l.memoizedState.isDehydrated && (n.flags & 256) === 0 || (n.flags |= 1024, ay())), je(n), null;
      case 26:
        var s = n.type, r = n.memoizedState;
        return l === null ? (Mu(n), r !== null ? (je(n), Xy(n, r)) : (je(n), Gy(
          n,
          s,
          null,
          i,
          u
        ))) : r ? r !== l.memoizedState ? (Mu(n), je(n), Xy(n, r)) : (je(n), n.flags &= -16777217) : (l = l.memoizedProps, l !== i && Mu(n), je(n), Gy(
          n,
          s,
          l,
          i,
          u
        )), null;
      case 27:
        if (oe(n), u = Le.current, s = n.type, l !== null && n.stateNode != null)
          l.memoizedProps !== i && Mu(n);
        else {
          if (!i) {
            if (n.stateNode === null)
              throw Error(U(166));
            return je(n), null;
          }
          l = F.current, bu(n) ? Ns(n) : (l = xf(s, i, u), n.stateNode = l, Mu(n));
        }
        return je(n), null;
      case 5:
        if (oe(n), s = n.type, l !== null && n.stateNode != null)
          l.memoizedProps !== i && Mu(n);
        else {
          if (!i) {
            if (n.stateNode === null)
              throw Error(U(166));
            return je(n), null;
          }
          if (r = F.current, bu(n))
            Ns(n);
          else {
            var m = fi(
              Le.current
            );
            switch (r) {
              case 1:
                r = m.createElementNS(
                  "http://www.w3.org/2000/svg",
                  s
                );
                break;
              case 2:
                r = m.createElementNS(
                  "http://www.w3.org/1998/Math/MathML",
                  s
                );
                break;
              default:
                switch (s) {
                  case "svg":
                    r = m.createElementNS(
                      "http://www.w3.org/2000/svg",
                      s
                    );
                    break;
                  case "math":
                    r = m.createElementNS(
                      "http://www.w3.org/1998/Math/MathML",
                      s
                    );
                    break;
                  case "script":
                    r = m.createElement("div"), r.innerHTML = "<script><\/script>", r = r.removeChild(
                      r.firstChild
                    );
                    break;
                  case "select":
                    r = typeof i.is == "string" ? m.createElement("select", {
                      is: i.is
                    }) : m.createElement("select"), i.multiple ? r.multiple = !0 : i.size && (r.size = i.size);
                    break;
                  default:
                    r = typeof i.is == "string" ? m.createElement(s, { is: i.is }) : m.createElement(s);
                }
            }
            r[Ut] = n, r[ra] = i;
            e: for (m = n.child; m !== null; ) {
              if (m.tag === 5 || m.tag === 6)
                r.appendChild(m.stateNode);
              else if (m.tag !== 4 && m.tag !== 27 && m.child !== null) {
                m.child.return = m, m = m.child;
                continue;
              }
              if (m === n) break e;
              for (; m.sibling === null; ) {
                if (m.return === null || m.return === n)
                  break e;
                m = m.return;
              }
              m.sibling.return = m.return, m = m.sibling;
            }
            n.stateNode = r;
            e: switch (Wl(r, s, i), s) {
              case "button":
              case "input":
              case "select":
              case "textarea":
                i = !!i.autoFocus;
                break e;
              case "img":
                i = !0;
                break e;
              default:
                i = !1;
            }
            i && Mu(n);
          }
        }
        return je(n), Gy(
          n,
          n.type,
          l === null ? null : l.memoizedProps,
          n.pendingProps,
          u
        ), null;
      case 6:
        if (l && n.stateNode != null)
          l.memoizedProps !== i && Mu(n);
        else {
          if (typeof i != "string" && n.stateNode === null)
            throw Error(U(166));
          if (l = Le.current, bu(n)) {
            if (l = n.stateNode, u = n.memoizedProps, i = null, s = Bl, s !== null)
              switch (s.tag) {
                case 27:
                case 5:
                  i = s.memoizedProps;
              }
            l[Ut] = n, l = !!(l.nodeValue === u || i !== null && i.suppressHydrationWarning === !0 || r0(l.nodeValue, u)), l || Tn(n, !0);
          } else
            l = fi(l).createTextNode(
              i
            ), l[Ut] = n, n.stateNode = l;
        }
        return je(n), null;
      case 31:
        if (u = n.memoizedState, l === null || l.memoizedState !== null) {
          if (i = bu(n), u !== null) {
            if (l === null) {
              if (!i) throw Error(U(318));
              if (l = n.memoizedState, l = l !== null ? l.dehydrated : null, !l) throw Error(U(557));
              l[Ut] = n;
            } else
              Qc(), (n.flags & 128) === 0 && (n.memoizedState = null), n.flags |= 4;
            je(n), l = !1;
          } else
            u = ay(), l !== null && l.memoizedState !== null && (l.memoizedState.hydrationErrors = u), l = !0;
          if (!l)
            return n.flags & 256 ? (va(n), n) : (va(n), null);
          if ((n.flags & 128) !== 0)
            throw Error(U(558));
        }
        return je(n), null;
      case 13:
        if (i = n.memoizedState, l === null || l.memoizedState !== null && l.memoizedState.dehydrated !== null) {
          if (s = bu(n), i !== null && i.dehydrated !== null) {
            if (l === null) {
              if (!s) throw Error(U(318));
              if (s = n.memoizedState, s = s !== null ? s.dehydrated : null, !s) throw Error(U(317));
              s[Ut] = n;
            } else
              Qc(), (n.flags & 128) === 0 && (n.memoizedState = null), n.flags |= 4;
            je(n), s = !1;
          } else
            s = ay(), l !== null && l.memoizedState !== null && (l.memoizedState.hydrationErrors = s), s = !0;
          if (!s)
            return n.flags & 256 ? (va(n), n) : (va(n), null);
        }
        return va(n), (n.flags & 128) !== 0 ? (n.lanes = u, n) : (u = i !== null, l = l !== null && l.memoizedState !== null, u && (i = n.child, s = null, i.alternate !== null && i.alternate.memoizedState !== null && i.alternate.memoizedState.cachePool !== null && (s = i.alternate.memoizedState.cachePool.pool), r = null, i.memoizedState !== null && i.memoizedState.cachePool !== null && (r = i.memoizedState.cachePool.pool), r !== s && (i.flags |= 2048)), u !== l && u && (n.child.flags |= 8192), ua(n, n.updateQueue), je(n), null);
      case 4:
        return gt(), l === null && Mf(n.stateNode.containerInfo), je(n), null;
      case 10:
        return Qn(n.type), je(n), null;
      case 19:
        if (H(It), i = n.memoizedState, i === null) return je(n), null;
        if (s = (n.flags & 128) !== 0, r = i.rendering, r === null)
          if (s) hf(i, !1);
          else {
            if (Vt !== 0 || l !== null && (l.flags & 128) !== 0)
              for (l = n.child; l !== null; ) {
                if (r = nf(l), r !== null) {
                  for (n.flags |= 128, hf(i, !1), l = r.updateQueue, n.updateQueue = l, ua(n, l), n.subtreeFlags = 0, l = u, u = n.child; u !== null; )
                    Pm(u, l), u = u.sibling;
                  return I(
                    It,
                    It.current & 1 | 2
                  ), ot && En(n, i.treeForkCount), n.child;
                }
                l = l.sibling;
              }
            i.tail !== null && bl() > Tt && (n.flags |= 128, s = !0, hf(i, !1), n.lanes = 4194304);
          }
        else {
          if (!s)
            if (l = nf(r), l !== null) {
              if (n.flags |= 128, s = !0, l = l.updateQueue, n.updateQueue = l, ua(n, l), hf(i, !0), i.tail === null && i.tailMode === "hidden" && !r.alternate && !ot)
                return je(n), null;
            } else
              2 * bl() - i.renderingStartTime > Tt && u !== 536870912 && (n.flags |= 128, s = !0, hf(i, !1), n.lanes = 4194304);
          i.isBackwards ? (r.sibling = n.child, n.child = r) : (l = i.last, l !== null ? l.sibling = r : n.child = r, i.last = r);
        }
        return i.tail !== null ? (l = i.tail, i.rendering = l, i.tail = l.sibling, i.renderingStartTime = bl(), l.sibling = null, u = It.current, I(
          It,
          s ? u & 1 | 2 : u & 1
        ), ot && En(n, i.treeForkCount), l) : (je(n), null);
      case 22:
      case 23:
        return va(n), lf(), i = n.memoizedState !== null, l !== null ? l.memoizedState !== null !== i && (n.flags |= 8192) : i && (n.flags |= 8192), i ? (u & 536870912) !== 0 && (n.flags & 128) === 0 && (je(n), n.subtreeFlags & 6 && (n.flags |= 8192)) : je(n), u = n.updateQueue, u !== null && ua(n, u.retryQueue), u = null, l !== null && l.memoizedState !== null && l.memoizedState.cachePool !== null && (u = l.memoizedState.cachePool.pool), i = null, n.memoizedState !== null && n.memoizedState.cachePool !== null && (i = n.memoizedState.cachePool.pool), i !== u && (n.flags |= 2048), l !== null && H(ka), null;
      case 24:
        return u = null, l !== null && (u = l.memoizedState.cache), n.memoizedState.cache !== u && (n.flags |= 2048), Qn(yl), je(n), null;
      case 25:
        return null;
      case 30:
        return null;
    }
    throw Error(U(156, n.tag));
  }
  function ig(l, n) {
    switch (Cd(n), n.tag) {
      case 1:
        return l = n.flags, l & 65536 ? (n.flags = l & -65537 | 128, n) : null;
      case 3:
        return Qn(yl), gt(), l = n.flags, (l & 65536) !== 0 && (l & 128) === 0 ? (n.flags = l & -65537 | 128, n) : null;
      case 26:
      case 27:
      case 5:
        return oe(n), null;
      case 31:
        if (n.memoizedState !== null) {
          if (va(n), n.alternate === null)
            throw Error(U(340));
          Qc();
        }
        return l = n.flags, l & 65536 ? (n.flags = l & -65537 | 128, n) : null;
      case 13:
        if (va(n), l = n.memoizedState, l !== null && l.dehydrated !== null) {
          if (n.alternate === null)
            throw Error(U(340));
          Qc();
        }
        return l = n.flags, l & 65536 ? (n.flags = l & -65537 | 128, n) : null;
      case 19:
        return H(It), null;
      case 4:
        return gt(), null;
      case 10:
        return Qn(n.type), null;
      case 22:
      case 23:
        return va(n), lf(), l !== null && H(ka), l = n.flags, l & 65536 ? (n.flags = l & -65537 | 128, n) : null;
      case 24:
        return Qn(yl), null;
      case 25:
        return null;
      default:
        return null;
    }
  }
  function og(l, n) {
    switch (Cd(n), n.tag) {
      case 3:
        Qn(yl), gt();
        break;
      case 26:
      case 27:
      case 5:
        oe(n);
        break;
      case 4:
        gt();
        break;
      case 31:
        n.memoizedState !== null && va(n);
        break;
      case 13:
        va(n);
        break;
      case 19:
        H(It);
        break;
      case 10:
        Qn(n.type);
        break;
      case 22:
      case 23:
        va(n), lf(), l !== null && H(ka);
        break;
      case 24:
        Qn(yl);
    }
  }
  function On(l, n) {
    try {
      var u = n.updateQueue, i = u !== null ? u.lastEffect : null;
      if (i !== null) {
        var s = i.next;
        u = s;
        do {
          if ((u.tag & l) === l) {
            i = void 0;
            var r = u.create, m = u.inst;
            i = r(), m.destroy = i;
          }
          u = u.next;
        } while (u !== s);
      }
    } catch (v) {
      Mt(n, n.return, v);
    }
  }
  function ln(l, n, u) {
    try {
      var i = n.updateQueue, s = i !== null ? i.lastEffect : null;
      if (s !== null) {
        var r = s.next;
        i = r;
        do {
          if ((i.tag & l) === l) {
            var m = i.inst, v = m.destroy;
            if (v !== void 0) {
              m.destroy = void 0, s = n;
              var A = u, j = v;
              try {
                j();
              } catch (V) {
                Mt(
                  s,
                  A,
                  V
                );
              }
            }
          }
          i = i.next;
        } while (i !== r);
      }
    } catch (V) {
      Mt(n, n.return, V);
    }
  }
  function oh(l) {
    var n = l.updateQueue;
    if (n !== null) {
      var u = l.stateNode;
      try {
        Ic(n, u);
      } catch (i) {
        Mt(l, l.return, i);
      }
    }
  }
  function ui(l, n, u) {
    u.props = ti(
      l.type,
      l.memoizedProps
    ), u.state = l.memoizedState;
    try {
      u.componentWillUnmount();
    } catch (i) {
      Mt(l, n, i);
    }
  }
  function Cu(l, n) {
    try {
      var u = l.ref;
      if (u !== null) {
        switch (l.tag) {
          case 26:
          case 27:
          case 5:
            var i = l.stateNode;
            break;
          case 30:
            i = l.stateNode;
            break;
          default:
            i = l.stateNode;
        }
        typeof u == "function" ? l.refCleanup = u(i) : u.current = i;
      }
    } catch (s) {
      Mt(l, n, s);
    }
  }
  function Kn(l, n) {
    var u = l.ref, i = l.refCleanup;
    if (u !== null)
      if (typeof i == "function")
        try {
          i();
        } catch (s) {
          Mt(l, n, s);
        } finally {
          l.refCleanup = null, l = l.alternate, l != null && (l.refCleanup = null);
        }
      else if (typeof u == "function")
        try {
          u(null);
        } catch (s) {
          Mt(l, n, s);
        }
      else u.current = null;
  }
  function Ly(l) {
    var n = l.type, u = l.memoizedProps, i = l.stateNode;
    try {
      e: switch (n) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          u.autoFocus && i.focus();
          break e;
        case "img":
          u.src ? i.src = u.src : u.srcSet && (i.srcset = u.srcSet);
      }
    } catch (s) {
      Mt(l, l.return, s);
    }
  }
  function fh(l, n, u) {
    try {
      var i = l.stateNode;
      h0(i, l.type, u, n), i[ra] = n;
    } catch (s) {
      Mt(l, l.return, s);
    }
  }
  function Qy(l) {
    return l.tag === 5 || l.tag === 3 || l.tag === 26 || l.tag === 27 && In(l.type) || l.tag === 4;
  }
  function mf(l) {
    e: for (; ; ) {
      for (; l.sibling === null; ) {
        if (l.return === null || Qy(l.return)) return null;
        l = l.return;
      }
      for (l.sibling.return = l.return, l = l.sibling; l.tag !== 5 && l.tag !== 6 && l.tag !== 18; ) {
        if (l.tag === 27 && In(l.type) || l.flags & 2 || l.child === null || l.tag === 4) continue e;
        l.child.return = l, l = l.child;
      }
      if (!(l.flags & 2)) return l.stateNode;
    }
  }
  function yf(l, n, u) {
    var i = l.tag;
    if (i === 5 || i === 6)
      l = l.stateNode, n ? (u.nodeType === 9 ? u.body : u.nodeName === "HTML" ? u.ownerDocument.body : u).insertBefore(l, n) : (n = u.nodeType === 9 ? u.body : u.nodeName === "HTML" ? u.ownerDocument.body : u, n.appendChild(l), u = u._reactRootContainer, u != null || n.onclick !== null || (n.onclick = Nn));
    else if (i !== 4 && (i === 27 && In(l.type) && (u = l.stateNode, n = null), l = l.child, l !== null))
      for (yf(l, n, u), l = l.sibling; l !== null; )
        yf(l, n, u), l = l.sibling;
  }
  function pf(l, n, u) {
    var i = l.tag;
    if (i === 5 || i === 6)
      l = l.stateNode, n ? u.insertBefore(l, n) : u.appendChild(l);
    else if (i !== 4 && (i === 27 && In(l.type) && (u = l.stateNode), l = l.child, l !== null))
      for (pf(l, n, u), l = l.sibling; l !== null; )
        pf(l, n, u), l = l.sibling;
  }
  function Vy(l) {
    var n = l.stateNode, u = l.memoizedProps;
    try {
      for (var i = l.type, s = n.attributes; s.length; )
        n.removeAttributeNode(s[0]);
      Wl(n, i, u), n[Ut] = l, n[ra] = u;
    } catch (r) {
      Mt(l, l.return, r);
    }
  }
  var mc = !1, Tl = !1, sh = !1, Zy = typeof WeakSet == "function" ? WeakSet : Set, Gl = null;
  function gf(l, n) {
    if (l = l.containerInfo, Ch = Ml, l = Gc(l), Ds(l)) {
      if ("selectionStart" in l)
        var u = {
          start: l.selectionStart,
          end: l.selectionEnd
        };
      else
        e: {
          u = (u = l.ownerDocument) && u.defaultView || window;
          var i = u.getSelection && u.getSelection();
          if (i && i.rangeCount !== 0) {
            u = i.anchorNode;
            var s = i.anchorOffset, r = i.focusNode;
            i = i.focusOffset;
            try {
              u.nodeType, r.nodeType;
            } catch {
              u = null;
              break e;
            }
            var m = 0, v = -1, A = -1, j = 0, V = 0, $ = l, B = null;
            t: for (; ; ) {
              for (var X; $ !== u || s !== 0 && $.nodeType !== 3 || (v = m + s), $ !== r || i !== 0 && $.nodeType !== 3 || (A = m + i), $.nodeType === 3 && (m += $.nodeValue.length), (X = $.firstChild) !== null; )
                B = $, $ = X;
              for (; ; ) {
                if ($ === l) break t;
                if (B === u && ++j === s && (v = m), B === r && ++V === i && (A = m), (X = $.nextSibling) !== null) break;
                $ = B, B = $.parentNode;
              }
              $ = X;
            }
            u = v === -1 || A === -1 ? null : { start: v, end: A };
          } else u = null;
        }
      u = u || { start: 0, end: 0 };
    } else u = null;
    for (Uh = { focusedElem: l, selectionRange: u }, Ml = !1, Gl = n; Gl !== null; )
      if (n = Gl, l = n.child, (n.subtreeFlags & 1028) !== 0 && l !== null)
        l.return = n, Gl = l;
      else
        for (; Gl !== null; ) {
          switch (n = Gl, r = n.alternate, l = n.flags, n.tag) {
            case 0:
              if ((l & 4) !== 0 && (l = n.updateQueue, l = l !== null ? l.events : null, l !== null))
                for (u = 0; u < l.length; u++)
                  s = l[u], s.ref.impl = s.nextImpl;
              break;
            case 11:
            case 15:
              break;
            case 1:
              if ((l & 1024) !== 0 && r !== null) {
                l = void 0, u = n, s = r.memoizedProps, r = r.memoizedState, i = u.stateNode;
                try {
                  var re = ti(
                    u.type,
                    s
                  );
                  l = i.getSnapshotBeforeUpdate(
                    re,
                    r
                  ), i.__reactInternalSnapshotBeforeUpdate = l;
                } catch (_e) {
                  Mt(
                    u,
                    u.return,
                    _e
                  );
                }
              }
              break;
            case 3:
              if ((l & 1024) !== 0) {
                if (l = n.stateNode.containerInfo, u = l.nodeType, u === 9)
                  Ar(l);
                else if (u === 1)
                  switch (l.nodeName) {
                    case "HEAD":
                    case "HTML":
                    case "BODY":
                      Ar(l);
                      break;
                    default:
                      l.textContent = "";
                  }
              }
              break;
            case 5:
            case 26:
            case 27:
            case 6:
            case 4:
            case 17:
              break;
            default:
              if ((l & 1024) !== 0) throw Error(U(163));
          }
          if (l = n.sibling, l !== null) {
            l.return = n.return, Gl = l;
            break;
          }
          Gl = n.return;
        }
  }
  function cr(l, n, u) {
    var i = u.flags;
    switch (u.tag) {
      case 0:
      case 11:
      case 15:
        yc(l, u), i & 4 && On(5, u);
        break;
      case 1:
        if (yc(l, u), i & 4)
          if (l = u.stateNode, n === null)
            try {
              l.componentDidMount();
            } catch (m) {
              Mt(u, u.return, m);
            }
          else {
            var s = ti(
              u.type,
              n.memoizedProps
            );
            n = n.memoizedState;
            try {
              l.componentDidUpdate(
                s,
                n,
                l.__reactInternalSnapshotBeforeUpdate
              );
            } catch (m) {
              Mt(
                u,
                u.return,
                m
              );
            }
          }
        i & 64 && oh(u), i & 512 && Cu(u, u.return);
        break;
      case 3:
        if (yc(l, u), i & 64 && (l = u.updateQueue, l !== null)) {
          if (n = null, u.child !== null)
            switch (u.child.tag) {
              case 27:
              case 5:
                n = u.child.stateNode;
                break;
              case 1:
                n = u.child.stateNode;
            }
          try {
            Ic(l, n);
          } catch (m) {
            Mt(u, u.return, m);
          }
        }
        break;
      case 27:
        n === null && i & 4 && Vy(u);
      case 26:
      case 5:
        yc(l, u), n === null && i & 4 && Ly(u), i & 512 && Cu(u, u.return);
        break;
      case 12:
        yc(l, u);
        break;
      case 31:
        yc(l, u), i & 4 && fg(l, u);
        break;
      case 13:
        yc(l, u), i & 4 && $y(l, u), i & 64 && (l = u.memoizedState, l !== null && (l = l.dehydrated, l !== null && (u = an.bind(
          null,
          u
        ), Uf(l, u))));
        break;
      case 22:
        if (i = u.memoizedState !== null || mc, !i) {
          n = n !== null && n.memoizedState !== null || Tl, s = mc;
          var r = Tl;
          mc = i, (Tl = n) && !r ? $n(
            l,
            u,
            (u.subtreeFlags & 8772) !== 0
          ) : yc(l, u), mc = s, Tl = r;
        }
        break;
      case 30:
        break;
      default:
        yc(l, u);
    }
  }
  function Jy(l) {
    var n = l.alternate;
    n !== null && (l.alternate = null, Jy(n)), l.child = null, l.deletions = null, l.sibling = null, l.tag === 5 && (n = l.stateNode, n !== null && cd(n)), l.stateNode = null, l.return = null, l.dependencies = null, l.memoizedProps = null, l.memoizedState = null, l.pendingProps = null, l.stateNode = null, l.updateQueue = null;
  }
  var Qt = null, Ea = !1;
  function Uu(l, n, u) {
    for (u = u.child; u !== null; )
      Ky(l, n, u), u = u.sibling;
  }
  function Ky(l, n, u) {
    if (zl && typeof zl.onCommitFiberUnmount == "function")
      try {
        zl.onCommitFiberUnmount(hn, u);
      } catch {
      }
    switch (u.tag) {
      case 26:
        Tl || Kn(u, n), Uu(
          l,
          n,
          u
        ), u.memoizedState ? u.memoizedState.count-- : u.stateNode && (u = u.stateNode, u.parentNode.removeChild(u));
        break;
      case 27:
        Tl || Kn(u, n);
        var i = Qt, s = Ea;
        In(u.type) && (Qt = u.stateNode, Ea = !1), Uu(
          l,
          n,
          u
        ), fo(u.stateNode), Qt = i, Ea = s;
        break;
      case 5:
        Tl || Kn(u, n);
      case 6:
        if (i = Qt, s = Ea, Qt = null, Uu(
          l,
          n,
          u
        ), Qt = i, Ea = s, Qt !== null)
          if (Ea)
            try {
              (Qt.nodeType === 9 ? Qt.body : Qt.nodeName === "HTML" ? Qt.ownerDocument.body : Qt).removeChild(u.stateNode);
            } catch (r) {
              Mt(
                u,
                n,
                r
              );
            }
          else
            try {
              Qt.removeChild(u.stateNode);
            } catch (r) {
              Mt(
                u,
                n,
                r
              );
            }
        break;
      case 18:
        Qt !== null && (Ea ? (l = Qt, g0(
          l.nodeType === 9 ? l.body : l.nodeName === "HTML" ? l.ownerDocument.body : l,
          u.stateNode
        ), Lf(l)) : g0(Qt, u.stateNode));
        break;
      case 4:
        i = Qt, s = Ea, Qt = u.stateNode.containerInfo, Ea = !0, Uu(
          l,
          n,
          u
        ), Qt = i, Ea = s;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        ln(2, u, n), Tl || ln(4, u, n), Uu(
          l,
          n,
          u
        );
        break;
      case 1:
        Tl || (Kn(u, n), i = u.stateNode, typeof i.componentWillUnmount == "function" && ui(
          u,
          n,
          i
        )), Uu(
          l,
          n,
          u
        );
        break;
      case 21:
        Uu(
          l,
          n,
          u
        );
        break;
      case 22:
        Tl = (i = Tl) || u.memoizedState !== null, Uu(
          l,
          n,
          u
        ), Tl = i;
        break;
      default:
        Uu(
          l,
          n,
          u
        );
    }
  }
  function fg(l, n) {
    if (n.memoizedState === null && (l = n.alternate, l !== null && (l = l.memoizedState, l !== null))) {
      l = l.dehydrated;
      try {
        Lf(l);
      } catch (u) {
        Mt(n, n.return, u);
      }
    }
  }
  function $y(l, n) {
    if (n.memoizedState === null && (l = n.alternate, l !== null && (l = l.memoizedState, l !== null && (l = l.dehydrated, l !== null))))
      try {
        Lf(l);
      } catch (u) {
        Mt(n, n.return, u);
      }
  }
  function ir(l) {
    switch (l.tag) {
      case 31:
      case 13:
      case 19:
        var n = l.stateNode;
        return n === null && (n = l.stateNode = new Zy()), n;
      case 22:
        return l = l.stateNode, n = l._retryCache, n === null && (n = l._retryCache = new Zy()), n;
      default:
        throw Error(U(435, l.tag));
    }
  }
  function or(l, n) {
    var u = ir(l);
    n.forEach(function(i) {
      if (!u.has(i)) {
        u.add(i);
        var s = Cg.bind(null, l, i);
        i.then(s, s);
      }
    });
  }
  function Ta(l, n) {
    var u = n.deletions;
    if (u !== null)
      for (var i = 0; i < u.length; i++) {
        var s = u[i], r = l, m = n, v = m;
        e: for (; v !== null; ) {
          switch (v.tag) {
            case 27:
              if (In(v.type)) {
                Qt = v.stateNode, Ea = !1;
                break e;
              }
              break;
            case 5:
              Qt = v.stateNode, Ea = !1;
              break e;
            case 3:
            case 4:
              Qt = v.stateNode.containerInfo, Ea = !0;
              break e;
          }
          v = v.return;
        }
        if (Qt === null) throw Error(U(160));
        Ky(r, m, s), Qt = null, Ea = !1, r = s.alternate, r !== null && (r.return = null), s.return = null;
      }
    if (n.subtreeFlags & 13886)
      for (n = n.child; n !== null; )
        rh(n, l), n = n.sibling;
  }
  var ke = null;
  function rh(l, n) {
    var u = l.alternate, i = l.flags;
    switch (l.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        Ta(n, l), Ca(l), i & 4 && (ln(3, l, l.return), On(3, l), ln(5, l, l.return));
        break;
      case 1:
        Ta(n, l), Ca(l), i & 512 && (Tl || u === null || Kn(u, u.return)), i & 64 && mc && (l = l.updateQueue, l !== null && (i = l.callbacks, i !== null && (u = l.shared.hiddenCallbacks, l.shared.hiddenCallbacks = u === null ? i : u.concat(i))));
        break;
      case 26:
        var s = ke;
        if (Ta(n, l), Ca(l), i & 512 && (Tl || u === null || Kn(u, u.return)), i & 4) {
          var r = u !== null ? u.memoizedState : null;
          if (i = l.memoizedState, u === null)
            if (i === null)
              if (l.stateNode === null) {
                e: {
                  i = l.type, u = l.memoizedProps, s = s.ownerDocument || s;
                  t: switch (i) {
                    case "title":
                      r = s.getElementsByTagName("title")[0], (!r || r[su] || r[Ut] || r.namespaceURI === "http://www.w3.org/2000/svg" || r.hasAttribute("itemprop")) && (r = s.createElement(i), s.head.insertBefore(
                        r,
                        s.querySelector("head > title")
                      )), Wl(r, i, u), r[Ut] = l, zt(r), i = r;
                      break e;
                    case "link":
                      var m = E0(
                        "link",
                        "href",
                        s
                      ).get(i + (u.href || ""));
                      if (m) {
                        for (var v = 0; v < m.length; v++)
                          if (r = m[v], r.getAttribute("href") === (u.href == null || u.href === "" ? null : u.href) && r.getAttribute("rel") === (u.rel == null ? null : u.rel) && r.getAttribute("title") === (u.title == null ? null : u.title) && r.getAttribute("crossorigin") === (u.crossOrigin == null ? null : u.crossOrigin)) {
                            m.splice(v, 1);
                            break t;
                          }
                      }
                      r = s.createElement(i), Wl(r, i, u), s.head.appendChild(r);
                      break;
                    case "meta":
                      if (m = E0(
                        "meta",
                        "content",
                        s
                      ).get(i + (u.content || ""))) {
                        for (v = 0; v < m.length; v++)
                          if (r = m[v], r.getAttribute("content") === (u.content == null ? null : "" + u.content) && r.getAttribute("name") === (u.name == null ? null : u.name) && r.getAttribute("property") === (u.property == null ? null : u.property) && r.getAttribute("http-equiv") === (u.httpEquiv == null ? null : u.httpEquiv) && r.getAttribute("charset") === (u.charSet == null ? null : u.charSet)) {
                            m.splice(v, 1);
                            break t;
                          }
                      }
                      r = s.createElement(i), Wl(r, i, u), s.head.appendChild(r);
                      break;
                    default:
                      throw Error(U(468, i));
                  }
                  r[Ut] = l, zt(r), i = r;
                }
                l.stateNode = i;
              } else
                Bh(
                  s,
                  l.type,
                  l.stateNode
                );
            else
              l.stateNode = b0(
                s,
                i,
                l.memoizedProps
              );
          else
            r !== i ? (r === null ? u.stateNode !== null && (u = u.stateNode, u.parentNode.removeChild(u)) : r.count--, i === null ? Bh(
              s,
              l.type,
              l.stateNode
            ) : b0(
              s,
              i,
              l.memoizedProps
            )) : i === null && l.stateNode !== null && fh(
              l,
              l.memoizedProps,
              u.memoizedProps
            );
        }
        break;
      case 27:
        Ta(n, l), Ca(l), i & 512 && (Tl || u === null || Kn(u, u.return)), u !== null && i & 4 && fh(
          l,
          l.memoizedProps,
          u.memoizedProps
        );
        break;
      case 5:
        if (Ta(n, l), Ca(l), i & 512 && (Tl || u === null || Kn(u, u.return)), l.flags & 32) {
          s = l.stateNode;
          try {
            du(s, "");
          } catch (re) {
            Mt(l, l.return, re);
          }
        }
        i & 4 && l.stateNode != null && (s = l.memoizedProps, fh(
          l,
          s,
          u !== null ? u.memoizedProps : s
        )), i & 1024 && (sh = !0);
        break;
      case 6:
        if (Ta(n, l), Ca(l), i & 4) {
          if (l.stateNode === null)
            throw Error(U(162));
          i = l.memoizedProps, u = l.stateNode;
          try {
            u.nodeValue = i;
          } catch (re) {
            Mt(l, l.return, re);
          }
        }
        break;
      case 3:
        if (Yf = null, s = ke, ke = ca(n.containerInfo), Ta(n, l), ke = s, Ca(l), i & 4 && u !== null && u.memoizedState.isDehydrated)
          try {
            Lf(n.containerInfo);
          } catch (re) {
            Mt(l, l.return, re);
          }
        sh && (sh = !1, ky(l));
        break;
      case 4:
        i = ke, ke = ca(
          l.stateNode.containerInfo
        ), Ta(n, l), Ca(l), ke = i;
        break;
      case 12:
        Ta(n, l), Ca(l);
        break;
      case 31:
        Ta(n, l), Ca(l), i & 4 && (i = l.updateQueue, i !== null && (l.updateQueue = null, or(l, i)));
        break;
      case 13:
        Ta(n, l), Ca(l), l.child.flags & 8192 && l.memoizedState !== null != (u !== null && u.memoizedState !== null) && (Fn = bl()), i & 4 && (i = l.updateQueue, i !== null && (l.updateQueue = null, or(l, i)));
        break;
      case 22:
        s = l.memoizedState !== null;
        var A = u !== null && u.memoizedState !== null, j = mc, V = Tl;
        if (mc = j || s, Tl = V || A, Ta(n, l), Tl = V, mc = j, Ca(l), i & 8192)
          e: for (n = l.stateNode, n._visibility = s ? n._visibility & -2 : n._visibility | 1, s && (u === null || A || mc || Tl || lo(l)), u = null, n = l; ; ) {
            if (n.tag === 5 || n.tag === 26) {
              if (u === null) {
                A = u = n;
                try {
                  if (r = A.stateNode, s)
                    m = r.style, typeof m.setProperty == "function" ? m.setProperty("display", "none", "important") : m.display = "none";
                  else {
                    v = A.stateNode;
                    var $ = A.memoizedProps.style, B = $ != null && $.hasOwnProperty("display") ? $.display : null;
                    v.style.display = B == null || typeof B == "boolean" ? "" : ("" + B).trim();
                  }
                } catch (re) {
                  Mt(A, A.return, re);
                }
              }
            } else if (n.tag === 6) {
              if (u === null) {
                A = n;
                try {
                  A.stateNode.nodeValue = s ? "" : A.memoizedProps;
                } catch (re) {
                  Mt(A, A.return, re);
                }
              }
            } else if (n.tag === 18) {
              if (u === null) {
                A = n;
                try {
                  var X = A.stateNode;
                  s ? vl(X, !0) : vl(A.stateNode, !1);
                } catch (re) {
                  Mt(A, A.return, re);
                }
              }
            } else if ((n.tag !== 22 && n.tag !== 23 || n.memoizedState === null || n === l) && n.child !== null) {
              n.child.return = n, n = n.child;
              continue;
            }
            if (n === l) break e;
            for (; n.sibling === null; ) {
              if (n.return === null || n.return === l) break e;
              u === n && (u = null), n = n.return;
            }
            u === n && (u = null), n.sibling.return = n.return, n = n.sibling;
          }
        i & 4 && (i = l.updateQueue, i !== null && (u = i.retryQueue, u !== null && (i.retryQueue = null, or(l, u))));
        break;
      case 19:
        Ta(n, l), Ca(l), i & 4 && (i = l.updateQueue, i !== null && (l.updateQueue = null, or(l, i)));
        break;
      case 30:
        break;
      case 21:
        break;
      default:
        Ta(n, l), Ca(l);
    }
  }
  function Ca(l) {
    var n = l.flags;
    if (n & 2) {
      try {
        for (var u, i = l.return; i !== null; ) {
          if (Qy(i)) {
            u = i;
            break;
          }
          i = i.return;
        }
        if (u == null) throw Error(U(160));
        switch (u.tag) {
          case 27:
            var s = u.stateNode, r = mf(l);
            pf(l, r, s);
            break;
          case 5:
            var m = u.stateNode;
            u.flags & 32 && (du(m, ""), u.flags &= -33);
            var v = mf(l);
            pf(l, v, m);
            break;
          case 3:
          case 4:
            var A = u.stateNode.containerInfo, j = mf(l);
            yf(
              l,
              j,
              A
            );
            break;
          default:
            throw Error(U(161));
        }
      } catch (V) {
        Mt(l, l.return, V);
      }
      l.flags &= -3;
    }
    n & 4096 && (l.flags &= -4097);
  }
  function ky(l) {
    if (l.subtreeFlags & 1024)
      for (l = l.child; l !== null; ) {
        var n = l;
        ky(n), n.tag === 5 && n.flags & 1024 && n.stateNode.reset(), l = l.sibling;
      }
  }
  function yc(l, n) {
    if (n.subtreeFlags & 8772)
      for (n = n.child; n !== null; )
        cr(l, n.alternate, n), n = n.sibling;
  }
  function lo(l) {
    for (l = l.child; l !== null; ) {
      var n = l;
      switch (n.tag) {
        case 0:
        case 11:
        case 14:
        case 15:
          ln(4, n, n.return), lo(n);
          break;
        case 1:
          Kn(n, n.return);
          var u = n.stateNode;
          typeof u.componentWillUnmount == "function" && ui(
            n,
            n.return,
            u
          ), lo(n);
          break;
        case 27:
          fo(n.stateNode);
        case 26:
        case 5:
          Kn(n, n.return), lo(n);
          break;
        case 22:
          n.memoizedState === null && lo(n);
          break;
        case 30:
          lo(n);
          break;
        default:
          lo(n);
      }
      l = l.sibling;
    }
  }
  function $n(l, n, u) {
    for (u = u && (n.subtreeFlags & 8772) !== 0, n = n.child; n !== null; ) {
      var i = n.alternate, s = l, r = n, m = r.flags;
      switch (r.tag) {
        case 0:
        case 11:
        case 15:
          $n(
            s,
            r,
            u
          ), On(4, r);
          break;
        case 1:
          if ($n(
            s,
            r,
            u
          ), i = r, s = i.stateNode, typeof s.componentDidMount == "function")
            try {
              s.componentDidMount();
            } catch (j) {
              Mt(i, i.return, j);
            }
          if (i = r, s = i.updateQueue, s !== null) {
            var v = i.stateNode;
            try {
              var A = s.shared.hiddenCallbacks;
              if (A !== null)
                for (s.shared.hiddenCallbacks = null, s = 0; s < A.length; s++)
                  Bd(A[s], v);
            } catch (j) {
              Mt(i, i.return, j);
            }
          }
          u && m & 64 && oh(r), Cu(r, r.return);
          break;
        case 27:
          Vy(r);
        case 26:
        case 5:
          $n(
            s,
            r,
            u
          ), u && i === null && m & 4 && Ly(r), Cu(r, r.return);
          break;
        case 12:
          $n(
            s,
            r,
            u
          );
          break;
        case 31:
          $n(
            s,
            r,
            u
          ), u && m & 4 && fg(s, r);
          break;
        case 13:
          $n(
            s,
            r,
            u
          ), u && m & 4 && $y(s, r);
          break;
        case 22:
          r.memoizedState === null && $n(
            s,
            r,
            u
          ), Cu(r, r.return);
          break;
        case 30:
          break;
        default:
          $n(
            s,
            r,
            u
          );
      }
      n = n.sibling;
    }
  }
  function dh(l, n) {
    var u = null;
    l !== null && l.memoizedState !== null && l.memoizedState.cachePool !== null && (u = l.memoizedState.cachePool.pool), l = null, n.memoizedState !== null && n.memoizedState.cachePool !== null && (l = n.memoizedState.cachePool.pool), l !== u && (l != null && l.refCount++, u != null && Bs(u));
  }
  function hh(l, n) {
    l = null, n.alternate !== null && (l = n.alternate.memoizedState.cache), n = n.memoizedState.cache, n !== l && (n.refCount++, l != null && Bs(l));
  }
  function zn(l, n, u, i) {
    if (n.subtreeFlags & 10256)
      for (n = n.child; n !== null; )
        vf(
          l,
          n,
          u,
          i
        ), n = n.sibling;
  }
  function vf(l, n, u, i) {
    var s = n.flags;
    switch (n.tag) {
      case 0:
      case 11:
      case 15:
        zn(
          l,
          n,
          u,
          i
        ), s & 2048 && On(9, n);
        break;
      case 1:
        zn(
          l,
          n,
          u,
          i
        );
        break;
      case 3:
        zn(
          l,
          n,
          u,
          i
        ), s & 2048 && (l = null, n.alternate !== null && (l = n.alternate.memoizedState.cache), n = n.memoizedState.cache, n !== l && (n.refCount++, l != null && Bs(l)));
        break;
      case 12:
        if (s & 2048) {
          zn(
            l,
            n,
            u,
            i
          ), l = n.stateNode;
          try {
            var r = n.memoizedProps, m = r.id, v = r.onPostCommit;
            typeof v == "function" && v(
              m,
              n.alternate === null ? "mount" : "update",
              l.passiveEffectDuration,
              -0
            );
          } catch (A) {
            Mt(n, n.return, A);
          }
        } else
          zn(
            l,
            n,
            u,
            i
          );
        break;
      case 31:
        zn(
          l,
          n,
          u,
          i
        );
        break;
      case 13:
        zn(
          l,
          n,
          u,
          i
        );
        break;
      case 23:
        break;
      case 22:
        r = n.stateNode, m = n.alternate, n.memoizedState !== null ? r._visibility & 2 ? zn(
          l,
          n,
          u,
          i
        ) : fr(l, n) : r._visibility & 2 ? zn(
          l,
          n,
          u,
          i
        ) : (r._visibility |= 2, Sf(
          l,
          n,
          u,
          i,
          (n.subtreeFlags & 10256) !== 0 || !1
        )), s & 2048 && dh(m, n);
        break;
      case 24:
        zn(
          l,
          n,
          u,
          i
        ), s & 2048 && hh(n.alternate, n);
        break;
      default:
        zn(
          l,
          n,
          u,
          i
        );
    }
  }
  function Sf(l, n, u, i, s) {
    for (s = s && ((n.subtreeFlags & 10256) !== 0 || !1), n = n.child; n !== null; ) {
      var r = l, m = n, v = u, A = i, j = m.flags;
      switch (m.tag) {
        case 0:
        case 11:
        case 15:
          Sf(
            r,
            m,
            v,
            A,
            s
          ), On(8, m);
          break;
        case 23:
          break;
        case 22:
          var V = m.stateNode;
          m.memoizedState !== null ? V._visibility & 2 ? Sf(
            r,
            m,
            v,
            A,
            s
          ) : fr(
            r,
            m
          ) : (V._visibility |= 2, Sf(
            r,
            m,
            v,
            A,
            s
          )), s && j & 2048 && dh(
            m.alternate,
            m
          );
          break;
        case 24:
          Sf(
            r,
            m,
            v,
            A,
            s
          ), s && j & 2048 && hh(m.alternate, m);
          break;
        default:
          Sf(
            r,
            m,
            v,
            A,
            s
          );
      }
      n = n.sibling;
    }
  }
  function fr(l, n) {
    if (n.subtreeFlags & 10256)
      for (n = n.child; n !== null; ) {
        var u = l, i = n, s = i.flags;
        switch (i.tag) {
          case 22:
            fr(u, i), s & 2048 && dh(
              i.alternate,
              i
            );
            break;
          case 24:
            fr(u, i), s & 2048 && hh(i.alternate, i);
            break;
          default:
            fr(u, i);
        }
        n = n.sibling;
      }
  }
  var Ua = 8192;
  function xu(l, n, u) {
    if (l.subtreeFlags & Ua)
      for (l = l.child; l !== null; )
        sg(
          l,
          n,
          u
        ), l = l.sibling;
  }
  function sg(l, n, u) {
    switch (l.tag) {
      case 26:
        xu(
          l,
          n,
          u
        ), l.flags & Ua && l.memoizedState !== null && Yu(
          u,
          ke,
          l.memoizedState,
          l.memoizedProps
        );
        break;
      case 5:
        xu(
          l,
          n,
          u
        );
        break;
      case 3:
      case 4:
        var i = ke;
        ke = ca(l.stateNode.containerInfo), xu(
          l,
          n,
          u
        ), ke = i;
        break;
      case 22:
        l.memoizedState === null && (i = l.alternate, i !== null && i.memoizedState !== null ? (i = Ua, Ua = 16777216, xu(
          l,
          n,
          u
        ), Ua = i) : xu(
          l,
          n,
          u
        ));
        break;
      default:
        xu(
          l,
          n,
          u
        );
    }
  }
  function mh(l) {
    var n = l.alternate;
    if (n !== null && (l = n.child, l !== null)) {
      n.child = null;
      do
        n = l.sibling, l.sibling = null, l = n;
      while (l !== null);
    }
  }
  function bf(l) {
    var n = l.deletions;
    if ((l.flags & 16) !== 0) {
      if (n !== null)
        for (var u = 0; u < n.length; u++) {
          var i = n[u];
          Gl = i, yh(
            i,
            l
          );
        }
      mh(l);
    }
    if (l.subtreeFlags & 10256)
      for (l = l.child; l !== null; )
        Wy(l), l = l.sibling;
  }
  function Wy(l) {
    switch (l.tag) {
      case 0:
      case 11:
      case 15:
        bf(l), l.flags & 2048 && ln(9, l, l.return);
        break;
      case 3:
        bf(l);
        break;
      case 12:
        bf(l);
        break;
      case 22:
        var n = l.stateNode;
        l.memoizedState !== null && n._visibility & 2 && (l.return === null || l.return.tag !== 13) ? (n._visibility &= -3, sr(l)) : bf(l);
        break;
      default:
        bf(l);
    }
  }
  function sr(l) {
    var n = l.deletions;
    if ((l.flags & 16) !== 0) {
      if (n !== null)
        for (var u = 0; u < n.length; u++) {
          var i = n[u];
          Gl = i, yh(
            i,
            l
          );
        }
      mh(l);
    }
    for (l = l.child; l !== null; ) {
      switch (n = l, n.tag) {
        case 0:
        case 11:
        case 15:
          ln(8, n, n.return), sr(n);
          break;
        case 22:
          u = n.stateNode, u._visibility & 2 && (u._visibility &= -3, sr(n));
          break;
        default:
          sr(n);
      }
      l = l.sibling;
    }
  }
  function yh(l, n) {
    for (; Gl !== null; ) {
      var u = Gl;
      switch (u.tag) {
        case 0:
        case 11:
        case 15:
          ln(8, u, n);
          break;
        case 23:
        case 22:
          if (u.memoizedState !== null && u.memoizedState.cachePool !== null) {
            var i = u.memoizedState.cachePool.pool;
            i != null && i.refCount++;
          }
          break;
        case 24:
          Bs(u.memoizedState.cache);
      }
      if (i = u.child, i !== null) i.return = u, Gl = i;
      else
        e: for (u = l; Gl !== null; ) {
          i = Gl;
          var s = i.sibling, r = i.return;
          if (Jy(i), i === u) {
            Gl = null;
            break e;
          }
          if (s !== null) {
            s.return = r, Gl = s;
            break e;
          }
          Gl = r;
        }
    }
  }
  var rg = {
    getCacheForType: function(l) {
      var n = k(yl), u = n.data.get(l);
      return u === void 0 && (u = l(), n.data.set(l, u)), u;
    },
    cacheSignal: function() {
      return k(yl).controller.signal;
    }
  }, Fy = typeof WeakMap == "function" ? WeakMap : Map, St = 0, Nt = null, ft = null, at = 0, _t = 0, xe = null, Nu = !1, ci = !1, ph = !1, kn = 0, Vt = 0, Wn = 0, ao = 0, gh = 0, Aa = 0, ul = 0, rr = null, cl = null, vh = !1, Fn = 0, Iy = 0, Tt = 1 / 0, Ef = null, Pt = null, _l = 0, pc = null, ii = null, Hu = 0, xa = 0, Sh = null, bh = null, Tf = 0, dr = null;
  function Na() {
    return (St & 2) !== 0 && at !== 0 ? at & -at : R.T !== null ? zh() : nd();
  }
  function dg() {
    if (Aa === 0)
      if ((at & 536870912) === 0 || ot) {
        var l = ae;
        ae <<= 1, (ae & 3932160) === 0 && (ae = 262144), Aa = l;
      } else Aa = 536870912;
    return l = ga.current, l !== null && (l.flags |= 32), Aa;
  }
  function Oa(l, n, u) {
    (l === Nt && (_t === 2 || _t === 9) || l.cancelPendingCommit !== null) && (ju(l, 0), gc(
      l,
      at,
      Aa,
      !1
    )), xc(l, u), ((St & 2) === 0 || l !== Nt) && (l === Nt && ((St & 2) === 0 && (ao |= u), Vt === 4 && gc(
      l,
      at,
      Aa,
      !1
    )), Bu(l));
  }
  function hg(l, n, u) {
    if ((St & 6) !== 0) throw Error(U(327));
    var i = !u && (n & 127) === 0 && (n & l.expiredLanes) === 0 || lt(l, n), s = i ? vg(l, n) : Th(l, n, !0), r = i;
    do {
      if (s === 0) {
        ci && !i && gc(l, n, 0, !1);
        break;
      } else {
        if (u = l.current.alternate, r && !mg(u)) {
          s = Th(l, n, !1), r = !1;
          continue;
        }
        if (s === 2) {
          if (r = n, l.errorRecoveryDisabledLanes & r)
            var m = 0;
          else
            m = l.pendingLanes & -536870913, m = m !== 0 ? m : m & 536870912 ? 536870912 : 0;
          if (m !== 0) {
            n = m;
            e: {
              var v = l;
              s = rr;
              var A = v.current.memoizedState.isDehydrated;
              if (A && (ju(v, m).flags |= 256), m = Th(
                v,
                m,
                !1
              ), m !== 2) {
                if (ph && !A) {
                  v.errorRecoveryDisabledLanes |= r, ao |= r, s = 4;
                  break e;
                }
                r = cl, cl = s, r !== null && (cl === null ? cl = r : cl.push.apply(
                  cl,
                  r
                ));
              }
              s = m;
            }
            if (r = !1, s !== 2) continue;
          }
        }
        if (s === 1) {
          ju(l, 0), gc(l, n, 0, !0);
          break;
        }
        e: {
          switch (i = l, r = s, r) {
            case 0:
            case 1:
              throw Error(U(345));
            case 4:
              if ((n & 4194048) !== n) break;
            case 6:
              gc(
                i,
                n,
                Aa,
                !Nu
              );
              break e;
            case 2:
              cl = null;
              break;
            case 3:
            case 5:
              break;
            default:
              throw Error(U(329));
          }
          if ((n & 62914560) === n && (s = Fn + 300 - bl(), 10 < s)) {
            if (gc(
              i,
              n,
              Aa,
              !Nu
            ), me(i, 0, !0) !== 0) break e;
            Hu = n, i.timeoutHandle = Tr(
              hr.bind(
                null,
                i,
                u,
                cl,
                Ef,
                vh,
                n,
                Aa,
                ao,
                ul,
                Nu,
                r,
                "Throttled",
                -0,
                0
              ),
              s
            );
            break e;
          }
          hr(
            i,
            u,
            cl,
            Ef,
            vh,
            n,
            Aa,
            ao,
            ul,
            Nu,
            r,
            null,
            -0,
            0
          );
        }
      }
      break;
    } while (!0);
    Bu(l);
  }
  function hr(l, n, u, i, s, r, m, v, A, j, V, $, B, X) {
    if (l.timeoutHandle = -1, $ = n.subtreeFlags, $ & 8192 || ($ & 16785408) === 16785408) {
      $ = {
        stylesheets: null,
        count: 0,
        imgCount: 0,
        imgBytes: 0,
        suspenseyImages: [],
        waitingForImages: !0,
        waitingForViewTransition: !1,
        unsuspend: Nn
      }, sg(
        n,
        r,
        $
      );
      var re = (r & 62914560) === r ? Fn - bl() : (r & 4194048) === r ? Iy - bl() : 0;
      if (re = A0(
        $,
        re
      ), re !== null) {
        Hu = r, l.cancelPendingCommit = re(
          Tg.bind(
            null,
            l,
            n,
            r,
            u,
            i,
            s,
            m,
            v,
            A,
            V,
            $,
            null,
            B,
            X
          )
        ), gc(l, r, m, !j);
        return;
      }
    }
    Tg(
      l,
      n,
      r,
      u,
      i,
      s,
      m,
      v,
      A
    );
  }
  function mg(l) {
    for (var n = l; ; ) {
      var u = n.tag;
      if ((u === 0 || u === 11 || u === 15) && n.flags & 16384 && (u = n.updateQueue, u !== null && (u = u.stores, u !== null)))
        for (var i = 0; i < u.length; i++) {
          var s = u[i], r = s.getSnapshot;
          s = s.value;
          try {
            if (!na(r(), s)) return !1;
          } catch {
            return !1;
          }
        }
      if (u = n.child, n.subtreeFlags & 16384 && u !== null)
        u.return = n, n = u;
      else {
        if (n === l) break;
        for (; n.sibling === null; ) {
          if (n.return === null || n.return === l) return !0;
          n = n.return;
        }
        n.sibling.return = n.return, n = n.sibling;
      }
    }
    return !0;
  }
  function gc(l, n, u, i) {
    n &= ~gh, n &= ~ao, l.suspendedLanes |= n, l.pingedLanes &= ~n, i && (l.warmLanes |= n), i = l.expirationTimes;
    for (var s = n; 0 < s; ) {
      var r = 31 - Nl(s), m = 1 << r;
      i[r] = -1, s &= ~m;
    }
    u !== 0 && ys(l, u, n);
  }
  function Af() {
    return (St & 6) === 0 ? (Sc(0), !1) : !0;
  }
  function Py() {
    if (ft !== null) {
      if (_t === 0)
        var l = ft.return;
      else
        l = ft, Ln = cc = null, Js(l), $c = null, Zi = 0, l = ft;
      for (; l !== null; )
        og(l.alternate, l), l = l.return;
      ft = null;
    }
  }
  function ju(l, n) {
    var u = l.timeoutHandle;
    u !== -1 && (l.timeoutHandle = -1, qg(u)), u = l.cancelPendingCommit, u !== null && (l.cancelPendingCommit = null, u()), Hu = 0, Py(), Nt = l, ft = u = nc(l.current, null), at = n, _t = 0, xe = null, Nu = !1, ci = lt(l, n), ph = !1, ul = Aa = gh = ao = Wn = Vt = 0, cl = rr = null, vh = !1, (n & 8) !== 0 && (n |= n & 32);
    var i = l.entangledLanes;
    if (i !== 0)
      for (l = l.entanglements, i &= n; 0 < i; ) {
        var s = 31 - Nl(i), r = 1 << s;
        n |= l[s], i &= ~r;
      }
    return kn = n, Za(), u;
  }
  function Of(l, n) {
    Ke = null, R.H = er, n === Zc || n === ef ? (n = oy(), _t = 3) : n === Qi ? (n = oy(), _t = 4) : _t = n === ah ? 8 : n !== null && typeof n == "object" && typeof n.then == "function" ? 6 : 1, xe = n, ft === null && (Vt = 1, df(
      l,
      Ka(n, l.current)
    ));
  }
  function yg() {
    var l = ga.current;
    return l === null ? !0 : (at & 4194048) === at ? Ia === null : (at & 62914560) === at || (at & 536870912) !== 0 ? l === Ia : !1;
  }
  function pg() {
    var l = R.H;
    return R.H = er, l === null ? er : l;
  }
  function gg() {
    var l = R.A;
    return R.A = rg, l;
  }
  function Eh() {
    Vt = 4, Nu || (at & 4194048) !== at && ga.current !== null || (ci = !0), (Wn & 134217727) === 0 && (ao & 134217727) === 0 || Nt === null || gc(
      Nt,
      at,
      Aa,
      !1
    );
  }
  function Th(l, n, u) {
    var i = St;
    St |= 2;
    var s = pg(), r = gg();
    (Nt !== l || at !== n) && (Ef = null, ju(l, n)), n = !1;
    var m = Vt;
    e: do
      try {
        if (_t !== 0 && ft !== null) {
          var v = ft, A = xe;
          switch (_t) {
            case 8:
              Py(), m = 6;
              break e;
            case 3:
            case 2:
            case 9:
            case 6:
              ga.current === null && (n = !0);
              var j = _t;
              if (_t = 0, xe = null, no(l, v, A, j), u && ci) {
                m = 0;
                break e;
              }
              break;
            default:
              j = _t, _t = 0, xe = null, no(l, v, A, j);
          }
        }
        o1(), m = Vt;
        break;
      } catch (V) {
        Of(l, V);
      }
    while (!0);
    return n && l.shellSuspendCounter++, Ln = cc = null, St = i, R.H = s, R.A = r, ft === null && (Nt = null, at = 0, Za()), m;
  }
  function o1() {
    for (; ft !== null; ) Sg(ft);
  }
  function vg(l, n) {
    var u = St;
    St |= 2;
    var i = pg(), s = gg();
    Nt !== l || at !== n ? (Ef = null, Tt = bl() + 500, ju(l, n)) : ci = lt(
      l,
      n
    );
    e: do
      try {
        if (_t !== 0 && ft !== null) {
          n = ft;
          var r = xe;
          t: switch (_t) {
            case 1:
              _t = 0, xe = null, no(l, n, r, 1);
              break;
            case 2:
            case 9:
              if (cy(r)) {
                _t = 0, xe = null, bg(n);
                break;
              }
              n = function() {
                _t !== 2 && _t !== 9 || Nt !== l || (_t = 7), Bu(l);
              }, r.then(n, n);
              break e;
            case 3:
              _t = 7;
              break e;
            case 4:
              _t = 5;
              break e;
            case 7:
              cy(r) ? (_t = 0, xe = null, bg(n)) : (_t = 0, xe = null, no(l, n, r, 7));
              break;
            case 5:
              var m = null;
              switch (ft.tag) {
                case 26:
                  m = ft.memoizedState;
                case 5:
                case 27:
                  var v = ft;
                  if (m ? ja(m) : v.stateNode.complete) {
                    _t = 0, xe = null;
                    var A = v.sibling;
                    if (A !== null) ft = A;
                    else {
                      var j = v.return;
                      j !== null ? (ft = j, mr(j)) : ft = null;
                    }
                    break t;
                  }
              }
              _t = 0, xe = null, no(l, n, r, 5);
              break;
            case 6:
              _t = 0, xe = null, no(l, n, r, 6);
              break;
            case 8:
              Py(), Vt = 6;
              break e;
            default:
              throw Error(U(462));
          }
        }
        oi();
        break;
      } catch (V) {
        Of(l, V);
      }
    while (!0);
    return Ln = cc = null, R.H = i, R.A = s, St = u, ft !== null ? 0 : (Nt = null, at = 0, Za(), Vt);
  }
  function oi() {
    for (; ft !== null && !ou(); )
      Sg(ft);
  }
  function Sg(l) {
    var n = wy(l.alternate, l, kn);
    l.memoizedProps = l.pendingProps, n === null ? mr(l) : ft = n;
  }
  function bg(l) {
    var n = l, u = n.alternate;
    switch (n.tag) {
      case 15:
      case 0:
        n = ai(
          u,
          n,
          n.pendingProps,
          n.type,
          void 0,
          at
        );
        break;
      case 11:
        n = ai(
          u,
          n,
          n.pendingProps,
          n.type.render,
          n.ref,
          at
        );
        break;
      case 5:
        Js(n);
      default:
        og(u, n), n = ft = Pm(n, kn), n = wy(u, n, kn);
    }
    l.memoizedProps = l.pendingProps, n === null ? mr(l) : ft = n;
  }
  function no(l, n, u, i) {
    Ln = cc = null, Js(n), $c = null, Zi = 0;
    var s = n.return;
    try {
      if (i1(
        l,
        s,
        n,
        u,
        at
      )) {
        Vt = 1, df(
          l,
          Ka(u, l.current)
        ), ft = null;
        return;
      }
    } catch (r) {
      if (s !== null) throw ft = s, r;
      Vt = 1, df(
        l,
        Ka(u, l.current)
      ), ft = null;
      return;
    }
    n.flags & 32768 ? (ot || i === 1 ? l = !0 : ci || (at & 536870912) !== 0 ? l = !1 : (Nu = l = !0, (i === 2 || i === 9 || i === 3 || i === 6) && (i = ga.current, i !== null && i.tag === 13 && (i.flags |= 16384))), Eg(n, l)) : mr(n);
  }
  function mr(l) {
    var n = l;
    do {
      if ((n.flags & 32768) !== 0) {
        Eg(
          n,
          Nu
        );
        return;
      }
      l = n.return;
      var u = cg(
        n.alternate,
        n,
        kn
      );
      if (u !== null) {
        ft = u;
        return;
      }
      if (n = n.sibling, n !== null) {
        ft = n;
        return;
      }
      ft = n = l;
    } while (n !== null);
    Vt === 0 && (Vt = 5);
  }
  function Eg(l, n) {
    do {
      var u = ig(l.alternate, l);
      if (u !== null) {
        u.flags &= 32767, ft = u;
        return;
      }
      if (u = l.return, u !== null && (u.flags |= 32768, u.subtreeFlags = 0, u.deletions = null), !n && (l = l.sibling, l !== null)) {
        ft = l;
        return;
      }
      ft = l = u;
    } while (l !== null);
    Vt = 6, ft = null;
  }
  function Tg(l, n, u, i, s, r, m, v, A) {
    l.cancelPendingCommit = null;
    do
      zf();
    while (_l !== 0);
    if ((St & 6) !== 0) throw Error(U(327));
    if (n !== null) {
      if (n === l.current) throw Error(U(177));
      if (r = n.lanes | n.childLanes, r |= Sn, Ho(
        l,
        u,
        r,
        m,
        v,
        A
      ), l === Nt && (ft = Nt = null, at = 0), ii = n, pc = l, Hu = u, xa = r, Sh = s, bh = i, (n.subtreeFlags & 10256) !== 0 || (n.flags & 10256) !== 0 ? (l.callbackNode = null, l.callbackPriority = 0, Ug(Un, function() {
        return Rg(), null;
      })) : (l.callbackNode = null, l.callbackPriority = 0), i = (n.flags & 13878) !== 0, (n.subtreeFlags & 13878) !== 0 || i) {
        i = R.T, R.T = null, s = Z.p, Z.p = 2, m = St, St |= 4;
        try {
          gf(l, n, u);
        } finally {
          St = m, Z.p = s, R.T = i;
        }
      }
      _l = 1, Ag(), Og(), zg();
    }
  }
  function Ag() {
    if (_l === 1) {
      _l = 0;
      var l = pc, n = ii, u = (n.flags & 13878) !== 0;
      if ((n.subtreeFlags & 13878) !== 0 || u) {
        u = R.T, R.T = null;
        var i = Z.p;
        Z.p = 2;
        var s = St;
        St |= 4;
        try {
          rh(n, l);
          var r = Uh, m = Gc(l.containerInfo), v = r.focusedElem, A = r.selectionRange;
          if (m !== v && v && v.ownerDocument && ji(
            v.ownerDocument.documentElement,
            v
          )) {
            if (A !== null && Ds(v)) {
              var j = A.start, V = A.end;
              if (V === void 0 && (V = j), "selectionStart" in v)
                v.selectionStart = j, v.selectionEnd = Math.min(
                  V,
                  v.value.length
                );
              else {
                var $ = v.ownerDocument || document, B = $ && $.defaultView || window;
                if (B.getSelection) {
                  var X = B.getSelection(), re = v.textContent.length, _e = Math.min(A.start, re), jt = A.end === void 0 ? _e : Math.min(A.end, re);
                  !X.extend && _e > jt && (m = jt, jt = _e, _e = m);
                  var C = Fm(
                    v,
                    _e
                  ), D = Fm(
                    v,
                    jt
                  );
                  if (C && D && (X.rangeCount !== 1 || X.anchorNode !== C.node || X.anchorOffset !== C.offset || X.focusNode !== D.node || X.focusOffset !== D.offset)) {
                    var N = $.createRange();
                    N.setStart(C.node, C.offset), X.removeAllRanges(), _e > jt ? (X.addRange(N), X.extend(D.node, D.offset)) : (N.setEnd(D.node, D.offset), X.addRange(N));
                  }
                }
              }
            }
            for ($ = [], X = v; X = X.parentNode; )
              X.nodeType === 1 && $.push({
                element: X,
                left: X.scrollLeft,
                top: X.scrollTop
              });
            for (typeof v.focus == "function" && v.focus(), v = 0; v < $.length; v++) {
              var K = $[v];
              K.element.scrollLeft = K.left, K.element.scrollTop = K.top;
            }
          }
          Ml = !!Ch, Uh = Ch = null;
        } finally {
          St = s, Z.p = i, R.T = u;
        }
      }
      l.current = n, _l = 2;
    }
  }
  function Og() {
    if (_l === 2) {
      _l = 0;
      var l = pc, n = ii, u = (n.flags & 8772) !== 0;
      if ((n.subtreeFlags & 8772) !== 0 || u) {
        u = R.T, R.T = null;
        var i = Z.p;
        Z.p = 2;
        var s = St;
        St |= 4;
        try {
          cr(l, n.alternate, n);
        } finally {
          St = s, Z.p = i, R.T = u;
        }
      }
      _l = 3;
    }
  }
  function zg() {
    if (_l === 4 || _l === 3) {
      _l = 0, bi();
      var l = pc, n = ii, u = Hu, i = bh;
      (n.subtreeFlags & 10256) !== 0 || (n.flags & 10256) !== 0 ? _l = 5 : (_l = 0, ii = pc = null, Dg(l, l.pendingLanes));
      var s = l.pendingLanes;
      if (s === 0 && (Pt = null), zm(u), n = n.stateNode, zl && typeof zl.onCommitFiberRoot == "function")
        try {
          zl.onCommitFiberRoot(
            hn,
            n,
            void 0,
            (n.current.flags & 128) === 128
          );
        } catch {
        }
      if (i !== null) {
        n = R.T, s = Z.p, Z.p = 2, R.T = null;
        try {
          for (var r = l.onRecoverableError, m = 0; m < i.length; m++) {
            var v = i[m];
            r(v.value, {
              componentStack: v.stack
            });
          }
        } finally {
          R.T = n, Z.p = s;
        }
      }
      (Hu & 3) !== 0 && zf(), Bu(l), s = l.pendingLanes, (u & 261930) !== 0 && (s & 42) !== 0 ? l === dr ? Tf++ : (Tf = 0, dr = l) : Tf = 0, Sc(0);
    }
  }
  function Dg(l, n) {
    (l.pooledCacheLanes &= n) === 0 && (n = l.pooledCache, n != null && (l.pooledCache = null, Bs(n)));
  }
  function zf() {
    return Ag(), Og(), zg(), Rg();
  }
  function Rg() {
    if (_l !== 5) return !1;
    var l = pc, n = xa;
    xa = 0;
    var u = zm(Hu), i = R.T, s = Z.p;
    try {
      Z.p = 32 > u ? 32 : u, R.T = null, u = Sh, Sh = null;
      var r = pc, m = Hu;
      if (_l = 0, ii = pc = null, Hu = 0, (St & 6) !== 0) throw Error(U(331));
      var v = St;
      if (St |= 4, Wy(r.current), vf(
        r,
        r.current,
        m,
        u
      ), St = v, Sc(0, !1), zl && typeof zl.onPostCommitFiberRoot == "function")
        try {
          zl.onPostCommitFiberRoot(hn, r);
        } catch {
        }
      return !0;
    } finally {
      Z.p = s, R.T = i, Dg(l, n);
    }
  }
  function _g(l, n, u) {
    n = Ka(u, n), n = Cy(l.stateNode, n, 2), l = Fa(l, n, 2), l !== null && (xc(l, 2), Bu(l));
  }
  function Mt(l, n, u) {
    if (l.tag === 3)
      _g(l, l, u);
    else
      for (; n !== null; ) {
        if (n.tag === 3) {
          _g(
            n,
            l,
            u
          );
          break;
        } else if (n.tag === 1) {
          var i = n.stateNode;
          if (typeof n.type.getDerivedStateFromError == "function" || typeof i.componentDidCatch == "function" && (Pt === null || !Pt.has(i))) {
            l = Ka(u, l), u = Uy(2), i = Fa(n, u, 2), i !== null && (xy(
              u,
              i,
              n,
              l
            ), xc(i, 2), Bu(i));
            break;
          }
        }
        n = n.return;
      }
  }
  function yr(l, n, u) {
    var i = l.pingCache;
    if (i === null) {
      i = l.pingCache = new Fy();
      var s = /* @__PURE__ */ new Set();
      i.set(n, s);
    } else
      s = i.get(n), s === void 0 && (s = /* @__PURE__ */ new Set(), i.set(n, s));
    s.has(u) || (ph = !0, s.add(u), l = e0.bind(null, l, n, u), n.then(l, l));
  }
  function e0(l, n, u) {
    var i = l.pingCache;
    i !== null && i.delete(n), l.pingedLanes |= l.suspendedLanes & u, l.warmLanes &= ~u, Nt === l && (at & u) === u && (Vt === 4 || Vt === 3 && (at & 62914560) === at && 300 > bl() - Fn ? (St & 2) === 0 && ju(l, 0) : gh |= u, ul === at && (ul = 0)), Bu(l);
  }
  function Mg(l, n) {
    n === 0 && (n = la()), l = ac(l, n), l !== null && (xc(l, n), Bu(l));
  }
  function an(l) {
    var n = l.memoizedState, u = 0;
    n !== null && (u = n.retryLane), Mg(l, u);
  }
  function Cg(l, n) {
    var u = 0;
    switch (l.tag) {
      case 31:
      case 13:
        var i = l.stateNode, s = l.memoizedState;
        s !== null && (u = s.retryLane);
        break;
      case 19:
        i = l.stateNode;
        break;
      case 22:
        i = l.stateNode._retryCache;
        break;
      default:
        throw Error(U(314));
    }
    i !== null && i.delete(n), Mg(l, u);
  }
  function Ug(l, n) {
    return de(l, n);
  }
  var Df = null, uo = null, t0 = !1, Ah = !1, l0 = !1, vc = 0;
  function Bu(l) {
    l !== uo && l.next === null && (uo === null ? Df = uo = l : uo = uo.next = l), Ah = !0, t0 || (t0 = !0, gr());
  }
  function Sc(l, n) {
    if (!l0 && Ah) {
      l0 = !0;
      do
        for (var u = !1, i = Df; i !== null; ) {
          if (l !== 0) {
            var s = i.pendingLanes;
            if (s === 0) var r = 0;
            else {
              var m = i.suspendedLanes, v = i.pingedLanes;
              r = (1 << 31 - Nl(42 | l) + 1) - 1, r &= s & ~(m & ~v), r = r & 201326741 ? r & 201326741 | 1 : r ? r | 2 : 0;
            }
            r !== 0 && (u = !0, co(i, r));
          } else
            r = at, r = me(
              i,
              i === Nt ? r : 0,
              i.cancelPendingCommit !== null || i.timeoutHandle !== -1
            ), (r & 3) === 0 || lt(i, r) || (u = !0, co(i, r));
          i = i.next;
        }
      while (u);
      l0 = !1;
    }
  }
  function Oh() {
    a0();
  }
  function a0() {
    Ah = t0 = !1;
    var l = 0;
    vc !== 0 && f1() && (l = vc);
    for (var n = bl(), u = null, i = Df; i !== null; ) {
      var s = i.next, r = n0(i, n);
      r === 0 ? (i.next = null, u === null ? Df = s : u.next = s, s === null && (uo = u)) : (u = i, (l !== 0 || (r & 3) !== 0) && (Ah = !0)), i = s;
    }
    _l !== 0 && _l !== 5 || Sc(l), vc !== 0 && (vc = 0);
  }
  function n0(l, n) {
    for (var u = l.suspendedLanes, i = l.pingedLanes, s = l.expirationTimes, r = l.pendingLanes & -62914561; 0 < r; ) {
      var m = 31 - Nl(r), v = 1 << m, A = s[m];
      A === -1 ? ((v & u) === 0 || (v & i) !== 0) && (s[m] = Qe(v, n)) : A <= n && (l.expiredLanes |= v), r &= ~v;
    }
    if (n = Nt, u = at, u = me(
      l,
      l === n ? u : 0,
      l.cancelPendingCommit !== null || l.timeoutHandle !== -1
    ), i = l.callbackNode, u === 0 || l === n && (_t === 2 || _t === 9) || l.cancelPendingCommit !== null)
      return i !== null && i !== null && Cc(i), l.callbackNode = null, l.callbackPriority = 0;
    if ((u & 3) === 0 || lt(l, u)) {
      if (n = u & -u, n === l.callbackPriority) return n;
      switch (i !== null && Cc(i), zm(u)) {
        case 2:
        case 8:
          u = xo;
          break;
        case 32:
          u = Un;
          break;
        case 268435456:
          u = No;
          break;
        default:
          u = Un;
      }
      return i = pr.bind(null, l), u = de(u, i), l.callbackPriority = n, l.callbackNode = u, n;
    }
    return i !== null && i !== null && Cc(i), l.callbackPriority = 2, l.callbackNode = null, 2;
  }
  function pr(l, n) {
    if (_l !== 0 && _l !== 5)
      return l.callbackNode = null, l.callbackPriority = 0, null;
    var u = l.callbackNode;
    if (zf() && l.callbackNode !== u)
      return null;
    var i = at;
    return i = me(
      l,
      l === Nt ? i : 0,
      l.cancelPendingCommit !== null || l.timeoutHandle !== -1
    ), i === 0 ? null : (hg(l, i, n), n0(l, bl()), l.callbackNode != null && l.callbackNode === u ? pr.bind(null, l) : null);
  }
  function co(l, n) {
    if (zf()) return null;
    hg(l, n, !0);
  }
  function gr() {
    wg(function() {
      (St & 6) !== 0 ? de(
        Uo,
        Oh
      ) : a0();
    });
  }
  function zh() {
    if (vc === 0) {
      var l = Vc;
      l === 0 && (l = P, P <<= 1, (P & 261888) === 0 && (P = 256)), vc = l;
    }
    return vc;
  }
  function xg(l) {
    return l == null || typeof l == "symbol" || typeof l == "boolean" ? null : typeof l == "function" ? l : yn("" + l);
  }
  function io(l, n) {
    var u = n.ownerDocument.createElement("input");
    return u.name = n.name, u.value = n.value, l.id && u.setAttribute("form", l.id), n.parentNode.insertBefore(u, n), l = new FormData(l), u.parentNode.removeChild(u), l;
  }
  function vr(l, n, u, i, s) {
    if (n === "submit" && u && u.stateNode === s) {
      var r = xg(
        (s[ra] || null).action
      ), m = i.submitter;
      m && (n = (n = m[ra] || null) ? xg(n.formAction) : m.getAttribute("formAction"), n !== null && (r = n, m = null));
      var v = new As(
        "action",
        "action",
        null,
        i,
        s
      );
      l.push({
        event: v,
        listeners: [
          {
            instance: null,
            listener: function() {
              if (i.defaultPrevented) {
                if (vc !== 0) {
                  var A = m ? io(s, m) : new FormData(s);
                  sf(
                    u,
                    {
                      pending: !0,
                      data: A,
                      method: s.method,
                      action: r
                    },
                    null,
                    A
                  );
                }
              } else
                typeof r == "function" && (v.preventDefault(), A = m ? io(s, m) : new FormData(s), sf(
                  u,
                  {
                    pending: !0,
                    data: A,
                    method: s.method,
                    action: r
                  },
                  r,
                  A
                ));
            },
            currentTarget: s
          }
        ]
      });
    }
  }
  for (var Dh = 0; Dh < $o.length; Dh++) {
    var Rf = $o[Dh], u0 = Rf.toLowerCase(), c0 = Rf[0].toUpperCase() + Rf.slice(1);
    ha(
      u0,
      "on" + c0
    );
  }
  ha(_s, "onAnimationEnd"), ha(Im, "onAnimationIteration"), ha(Dd, "onAnimationStart"), ha("dblclick", "onDoubleClick"), ha("focusin", "onFocus"), ha("focusout", "onBlur"), ha(Bi, "onTransitionRun"), ha(Ms, "onTransitionStart"), ha(pu, "onTransitionCancel"), ha(Qp, "onTransitionEnd"), ru("onMouseEnter", ["mouseout", "mouseover"]), ru("onMouseLeave", ["mouseout", "mouseover"]), ru("onPointerEnter", ["pointerout", "pointerover"]), ru("onPointerLeave", ["pointerout", "pointerover"]), jc(
    "onChange",
    "change click focusin focusout input keydown keyup selectionchange".split(" ")
  ), jc(
    "onSelect",
    "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(
      " "
    )
  ), jc("onBeforeInput", [
    "compositionend",
    "keypress",
    "textInput",
    "paste"
  ]), jc(
    "onCompositionEnd",
    "compositionend focusout keydown keypress keyup mousedown".split(" ")
  ), jc(
    "onCompositionStart",
    "compositionstart focusout keydown keypress keyup mousedown".split(" ")
  ), jc(
    "onCompositionUpdate",
    "compositionupdate focusout keydown keypress keyup mousedown".split(" ")
  );
  var _f = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(
    " "
  ), Ng = new Set(
    "beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(_f)
  );
  function Hg(l, n) {
    n = (n & 4) !== 0;
    for (var u = 0; u < l.length; u++) {
      var i = l[u], s = i.event;
      i = i.listeners;
      e: {
        var r = void 0;
        if (n)
          for (var m = i.length - 1; 0 <= m; m--) {
            var v = i[m], A = v.instance, j = v.currentTarget;
            if (v = v.listener, A !== r && s.isPropagationStopped())
              break e;
            r = v, s.currentTarget = j;
            try {
              r(s);
            } catch (V) {
              Yi(V);
            }
            s.currentTarget = null, r = A;
          }
        else
          for (m = 0; m < i.length; m++) {
            if (v = i[m], A = v.instance, j = v.currentTarget, v = v.listener, A !== r && s.isPropagationStopped())
              break e;
            r = v, s.currentTarget = j;
            try {
              r(s);
            } catch (V) {
              Yi(V);
            }
            s.currentTarget = null, r = A;
          }
      }
    }
  }
  function ct(l, n) {
    var u = n[ud];
    u === void 0 && (u = n[ud] = /* @__PURE__ */ new Set());
    var i = l + "__bubble";
    u.has(i) || (Sr(n, l, 2, !1), u.add(i));
  }
  function i0(l, n, u) {
    var i = 0;
    n && (i |= 4), Sr(
      u,
      l,
      i,
      n
    );
  }
  var Rh = "_reactListening" + Math.random().toString(36).slice(2);
  function Mf(l) {
    if (!l[Rh]) {
      l[Rh] = !0, zi.forEach(function(u) {
        u !== "selectionchange" && (Ng.has(u) || i0(u, !1, l), i0(u, !0, l));
      });
      var n = l.nodeType === 9 ? l : l.ownerDocument;
      n === null || n[Rh] || (n[Rh] = !0, i0("selectionchange", !1, n));
    }
  }
  function Sr(l, n, u, i) {
    switch (_r(n)) {
      case 2:
        var s = qu;
        break;
      case 8:
        s = wu;
        break;
      default:
        s = Fl;
    }
    u = s.bind(
      null,
      n,
      u,
      l
    ), s = void 0, !Es || n !== "touchstart" && n !== "touchmove" && n !== "wheel" || (s = !0), i ? s !== void 0 ? l.addEventListener(n, u, {
      capture: !0,
      passive: s
    }) : l.addEventListener(n, u, !0) : s !== void 0 ? l.addEventListener(n, u, {
      passive: s
    }) : l.addEventListener(n, u, !1);
  }
  function o0(l, n, u, i, s) {
    var r = i;
    if ((n & 1) === 0 && (n & 2) === 0 && i !== null)
      e: for (; ; ) {
        if (i === null) return;
        var m = i.tag;
        if (m === 3 || m === 4) {
          var v = i.stateNode.containerInfo;
          if (v === s) break;
          if (m === 4)
            for (m = i.return; m !== null; ) {
              var A = m.tag;
              if ((A === 3 || A === 4) && m.stateNode.containerInfo === s)
                return;
              m = m.return;
            }
          for (; v !== null; ) {
            if (m = Ti(v), m === null) return;
            if (A = m.tag, A === 5 || A === 6 || A === 26 || A === 27) {
              i = r = m;
              continue e;
            }
            v = v.parentNode;
          }
        }
        i = i.return;
      }
    Hm(function() {
      var j = r, V = hd(u), $ = [];
      e: {
        var B = gu.get(l);
        if (B !== void 0) {
          var X = As, re = l;
          switch (l) {
            case "keypress":
              if (yd(u) === 0) break e;
            case "keydown":
            case "keyup":
              X = Sd;
              break;
            case "focusin":
              re = "focus", X = gd;
              break;
            case "focusout":
              re = "blur", X = gd;
              break;
            case "beforeblur":
            case "afterblur":
              X = gd;
              break;
            case "click":
              if (u.button === 2) break e;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              X = Qo;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              X = Up;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              X = Bp;
              break;
            case _s:
            case Im:
            case Dd:
              X = Np;
              break;
            case Qp:
              X = a1;
              break;
            case "scroll":
            case "scrollend":
              X = t1;
              break;
            case "wheel":
              X = n1;
              break;
            case "copy":
            case "cut":
            case "paste":
              X = Mi;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              X = Bn;
              break;
            case "toggle":
            case "beforetoggle":
              X = Qm;
          }
          var _e = (n & 4) !== 0, jt = !_e && (l === "scroll" || l === "scrollend"), C = _e ? B !== null ? B + "Capture" : null : B;
          _e = [];
          for (var D = j, N; D !== null; ) {
            var K = D;
            if (N = K.stateNode, K = K.tag, K !== 5 && K !== 26 && K !== 27 || N === null || C === null || (K = Hl(D, C), K != null && _e.push(
              br(D, K, N)
            )), jt) break;
            D = D.return;
          }
          0 < _e.length && (B = new X(
            B,
            re,
            null,
            u,
            V
          ), $.push({ event: B, listeners: _e }));
        }
      }
      if ((n & 7) === 0) {
        e: {
          if (B = l === "mouseover" || l === "pointerover", X = l === "mouseout" || l === "pointerout", B && u !== dd && (re = u.relatedTarget || u.fromElement) && (Ti(re) || re[Nc]))
            break e;
          if ((X || B) && (B = V.window === V ? V : (B = V.ownerDocument) ? B.defaultView || B.parentWindow : window, X ? (re = u.relatedTarget || u.toElement, X = j, re = re ? Ti(re) : null, re !== null && (jt = Se(re), _e = re.tag, re !== jt || _e !== 5 && _e !== 27 && _e !== 6) && (re = null)) : (X = null, re = j), X !== re)) {
            if (_e = Qo, K = "onMouseLeave", C = "onMouseEnter", D = "mouse", (l === "pointerout" || l === "pointerover") && (_e = Bn, K = "onPointerLeave", C = "onPointerEnter", D = "pointer"), jt = X == null ? B : jo(X), N = re == null ? B : jo(re), B = new _e(
              K,
              D + "leave",
              X,
              u,
              V
            ), B.target = jt, B.relatedTarget = N, K = null, Ti(V) === j && (_e = new _e(
              C,
              D + "enter",
              re,
              u,
              V
            ), _e.target = N, _e.relatedTarget = jt, K = _e), jt = K, X && re)
              t: {
                for (_e = jg, C = X, D = re, N = 0, K = C; K; K = _e(K))
                  N++;
                K = 0;
                for (var Ee = D; Ee; Ee = _e(Ee))
                  K++;
                for (; 0 < N - K; )
                  C = _e(C), N--;
                for (; 0 < K - N; )
                  D = _e(D), K--;
                for (; N--; ) {
                  if (C === D || D !== null && C === D.alternate) {
                    _e = C;
                    break t;
                  }
                  C = _e(C), D = _e(D);
                }
                _e = null;
              }
            else _e = null;
            X !== null && _h(
              $,
              B,
              X,
              _e,
              !1
            ), re !== null && jt !== null && _h(
              $,
              jt,
              re,
              _e,
              !0
            );
          }
        }
        e: {
          if (B = j ? jo(j) : window, X = B.nodeName && B.nodeName.toLowerCase(), X === "select" || X === "input" && B.type === "file")
            var yt = $m;
          else if (yu(B))
            if (Td)
              yt = Hi;
            else {
              yt = Xp;
              var ye = Gp;
            }
          else
            X = B.nodeName, !X || X.toLowerCase() !== "input" || B.type !== "checkbox" && B.type !== "radio" ? j && Nm(j.elementType) && (yt = $m) : yt = wc;
          if (yt && (yt = yt(l, j))) {
            Km(
              $,
              yt,
              u,
              V
            );
            break e;
          }
          ye && ye(l, B, j), l === "focusout" && j && B.type === "number" && j.memoizedProps.value != null && Di(B, "number", B.value);
        }
        switch (ye = j ? jo(j) : window, l) {
          case "focusin":
            (yu(ye) || ye.contentEditable === "true") && (Xc = ye, Jo = j, vn = null);
            break;
          case "focusout":
            vn = Jo = Xc = null;
            break;
          case "mousedown":
            qn = !0;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            qn = !1, zd($, u, V);
            break;
          case "selectionchange":
            if (Rs) break;
          case "keydown":
          case "keyup":
            zd($, u, V);
        }
        var Ve;
        if (Vo)
          e: {
            switch (l) {
              case "compositionstart":
                var We = "onCompositionStart";
                break e;
              case "compositionend":
                We = "onCompositionEnd";
                break e;
              case "compositionupdate":
                We = "onCompositionUpdate";
                break e;
            }
            We = void 0;
          }
        else
          Ui ? Ed(l, u) && (We = "onCompositionEnd") : l === "keydown" && u.keyCode === 229 && (We = "onCompositionStart");
        We && (Vm && u.locale !== "ko" && (Ui || We !== "onCompositionStart" ? We === "onCompositionEnd" && Ui && (Ve = Bm()) : (tc = V, jm = "value" in tc ? tc.value : tc.textContent, Ui = !0)), ye = Er(j, We), 0 < ye.length && (We = new Hp(
          We,
          l,
          null,
          u,
          V
        ), $.push({ event: We, listeners: ye }), Ve ? We.data = Ve : (Ve = Zm(u), Ve !== null && (We.data = Ve)))), (Ve = aa ? wp(l, u) : u1(l, u)) && (We = Er(j, "onBeforeInput"), 0 < We.length && (ye = new Hp(
          "onBeforeInput",
          "beforeinput",
          null,
          u,
          V
        ), $.push({
          event: ye,
          listeners: We
        }), ye.data = Ve)), vr(
          $,
          l,
          j,
          u,
          V
        );
      }
      Hg($, n);
    });
  }
  function br(l, n, u) {
    return {
      instance: l,
      listener: n,
      currentTarget: u
    };
  }
  function Er(l, n) {
    for (var u = n + "Capture", i = []; l !== null; ) {
      var s = l, r = s.stateNode;
      if (s = s.tag, s !== 5 && s !== 26 && s !== 27 || r === null || (s = Hl(l, u), s != null && i.unshift(
        br(l, s, r)
      ), s = Hl(l, n), s != null && i.push(
        br(l, s, r)
      )), l.tag === 3) return i;
      l = l.return;
    }
    return [];
  }
  function jg(l) {
    if (l === null) return null;
    do
      l = l.return;
    while (l && l.tag !== 5 && l.tag !== 27);
    return l || null;
  }
  function _h(l, n, u, i, s) {
    for (var r = n._reactName, m = []; u !== null && u !== i; ) {
      var v = u, A = v.alternate, j = v.stateNode;
      if (v = v.tag, A !== null && A === i) break;
      v !== 5 && v !== 26 && v !== 27 || j === null || (A = j, s ? (j = Hl(u, r), j != null && m.unshift(
        br(u, j, A)
      )) : s || (j = Hl(u, r), j != null && m.push(
        br(u, j, A)
      ))), u = u.return;
    }
    m.length !== 0 && l.push({ event: n, listeners: m });
  }
  var Bg = /\r\n?/g, f0 = /\u0000|\uFFFD/g;
  function s0(l) {
    return (typeof l == "string" ? l : "" + l).replace(Bg, `
`).replace(f0, "");
  }
  function r0(l, n) {
    return n = s0(n), s0(l) === n;
  }
  function Ht(l, n, u, i, s, r) {
    switch (u) {
      case "children":
        typeof i == "string" ? n === "body" || n === "textarea" && i === "" || du(l, i) : (typeof i == "number" || typeof i == "bigint") && n !== "body" && du(l, "" + i);
        break;
      case "className":
        fd(l, "class", i);
        break;
      case "tabIndex":
        fd(l, "tabindex", i);
        break;
      case "dir":
      case "role":
      case "viewBox":
      case "width":
      case "height":
        fd(l, u, i);
        break;
      case "style":
        _p(l, i, r);
        break;
      case "data":
        if (n !== "object") {
          fd(l, "data", i);
          break;
        }
      case "src":
      case "href":
        if (i === "" && (n !== "a" || u !== "href")) {
          l.removeAttribute(u);
          break;
        }
        if (i == null || typeof i == "function" || typeof i == "symbol" || typeof i == "boolean") {
          l.removeAttribute(u);
          break;
        }
        i = yn("" + i), l.setAttribute(u, i);
        break;
      case "action":
      case "formAction":
        if (typeof i == "function") {
          l.setAttribute(
            u,
            "javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')"
          );
          break;
        } else
          typeof r == "function" && (u === "formAction" ? (n !== "input" && Ht(l, n, "name", s.name, s, null), Ht(
            l,
            n,
            "formEncType",
            s.formEncType,
            s,
            null
          ), Ht(
            l,
            n,
            "formMethod",
            s.formMethod,
            s,
            null
          ), Ht(
            l,
            n,
            "formTarget",
            s.formTarget,
            s,
            null
          )) : (Ht(l, n, "encType", s.encType, s, null), Ht(l, n, "method", s.method, s, null), Ht(l, n, "target", s.target, s, null)));
        if (i == null || typeof i == "symbol" || typeof i == "boolean") {
          l.removeAttribute(u);
          break;
        }
        i = yn("" + i), l.setAttribute(u, i);
        break;
      case "onClick":
        i != null && (l.onclick = Nn);
        break;
      case "onScroll":
        i != null && ct("scroll", l);
        break;
      case "onScrollEnd":
        i != null && ct("scrollend", l);
        break;
      case "dangerouslySetInnerHTML":
        if (i != null) {
          if (typeof i != "object" || !("__html" in i))
            throw Error(U(61));
          if (u = i.__html, u != null) {
            if (s.children != null) throw Error(U(60));
            l.innerHTML = u;
          }
        }
        break;
      case "multiple":
        l.multiple = i && typeof i != "function" && typeof i != "symbol";
        break;
      case "muted":
        l.muted = i && typeof i != "function" && typeof i != "symbol";
        break;
      case "suppressContentEditableWarning":
      case "suppressHydrationWarning":
      case "defaultValue":
      case "defaultChecked":
      case "innerHTML":
      case "ref":
        break;
      case "autoFocus":
        break;
      case "xlinkHref":
        if (i == null || typeof i == "function" || typeof i == "boolean" || typeof i == "symbol") {
          l.removeAttribute("xlink:href");
          break;
        }
        u = yn("" + i), l.setAttributeNS(
          "http://www.w3.org/1999/xlink",
          "xlink:href",
          u
        );
        break;
      case "contentEditable":
      case "spellCheck":
      case "draggable":
      case "value":
      case "autoReverse":
      case "externalResourcesRequired":
      case "focusable":
      case "preserveAlpha":
        i != null && typeof i != "function" && typeof i != "symbol" ? l.setAttribute(u, "" + i) : l.removeAttribute(u);
        break;
      case "inert":
      case "allowFullScreen":
      case "async":
      case "autoPlay":
      case "controls":
      case "default":
      case "defer":
      case "disabled":
      case "disablePictureInPicture":
      case "disableRemotePlayback":
      case "formNoValidate":
      case "hidden":
      case "loop":
      case "noModule":
      case "noValidate":
      case "open":
      case "playsInline":
      case "readOnly":
      case "required":
      case "reversed":
      case "scoped":
      case "seamless":
      case "itemScope":
        i && typeof i != "function" && typeof i != "symbol" ? l.setAttribute(u, "") : l.removeAttribute(u);
        break;
      case "capture":
      case "download":
        i === !0 ? l.setAttribute(u, "") : i !== !1 && i != null && typeof i != "function" && typeof i != "symbol" ? l.setAttribute(u, i) : l.removeAttribute(u);
        break;
      case "cols":
      case "rows":
      case "size":
      case "span":
        i != null && typeof i != "function" && typeof i != "symbol" && !isNaN(i) && 1 <= i ? l.setAttribute(u, i) : l.removeAttribute(u);
        break;
      case "rowSpan":
      case "start":
        i == null || typeof i == "function" || typeof i == "symbol" || isNaN(i) ? l.removeAttribute(u) : l.setAttribute(u, i);
        break;
      case "popover":
        ct("beforetoggle", l), ct("toggle", l), qo(l, "popover", i);
        break;
      case "xlinkActuate":
        Pu(
          l,
          "http://www.w3.org/1999/xlink",
          "xlink:actuate",
          i
        );
        break;
      case "xlinkArcrole":
        Pu(
          l,
          "http://www.w3.org/1999/xlink",
          "xlink:arcrole",
          i
        );
        break;
      case "xlinkRole":
        Pu(
          l,
          "http://www.w3.org/1999/xlink",
          "xlink:role",
          i
        );
        break;
      case "xlinkShow":
        Pu(
          l,
          "http://www.w3.org/1999/xlink",
          "xlink:show",
          i
        );
        break;
      case "xlinkTitle":
        Pu(
          l,
          "http://www.w3.org/1999/xlink",
          "xlink:title",
          i
        );
        break;
      case "xlinkType":
        Pu(
          l,
          "http://www.w3.org/1999/xlink",
          "xlink:type",
          i
        );
        break;
      case "xmlBase":
        Pu(
          l,
          "http://www.w3.org/XML/1998/namespace",
          "xml:base",
          i
        );
        break;
      case "xmlLang":
        Pu(
          l,
          "http://www.w3.org/XML/1998/namespace",
          "xml:lang",
          i
        );
        break;
      case "xmlSpace":
        Pu(
          l,
          "http://www.w3.org/XML/1998/namespace",
          "xml:space",
          i
        );
        break;
      case "is":
        qo(l, "is", i);
        break;
      case "innerText":
      case "textContent":
        break;
      default:
        (!(2 < u.length) || u[0] !== "o" && u[0] !== "O" || u[1] !== "n" && u[1] !== "N") && (u = e1.get(u) || u, qo(l, u, i));
    }
  }
  function d0(l, n, u, i, s, r) {
    switch (u) {
      case "style":
        _p(l, i, r);
        break;
      case "dangerouslySetInnerHTML":
        if (i != null) {
          if (typeof i != "object" || !("__html" in i))
            throw Error(U(61));
          if (u = i.__html, u != null) {
            if (s.children != null) throw Error(U(60));
            l.innerHTML = u;
          }
        }
        break;
      case "children":
        typeof i == "string" ? du(l, i) : (typeof i == "number" || typeof i == "bigint") && du(l, "" + i);
        break;
      case "onScroll":
        i != null && ct("scroll", l);
        break;
      case "onScrollEnd":
        i != null && ct("scrollend", l);
        break;
      case "onClick":
        i != null && (l.onclick = Nn);
        break;
      case "suppressContentEditableWarning":
      case "suppressHydrationWarning":
      case "innerHTML":
      case "ref":
        break;
      case "innerText":
      case "textContent":
        break;
      default:
        if (!Hc.hasOwnProperty(u))
          e: {
            if (u[0] === "o" && u[1] === "n" && (s = u.endsWith("Capture"), n = u.slice(2, s ? u.length - 7 : void 0), r = l[ra] || null, r = r != null ? r[u] : null, typeof r == "function" && l.removeEventListener(n, r, s), typeof i == "function")) {
              typeof r != "function" && r !== null && (u in l ? l[u] = null : l.hasAttribute(u) && l.removeAttribute(u)), l.addEventListener(n, i, s);
              break e;
            }
            u in l ? l[u] = i : i === !0 ? l.setAttribute(u, "") : qo(l, u, i);
          }
    }
  }
  function Wl(l, n, u) {
    switch (n) {
      case "div":
      case "span":
      case "svg":
      case "path":
      case "a":
      case "g":
      case "p":
      case "li":
        break;
      case "img":
        ct("error", l), ct("load", l);
        var i = !1, s = !1, r;
        for (r in u)
          if (u.hasOwnProperty(r)) {
            var m = u[r];
            if (m != null)
              switch (r) {
                case "src":
                  i = !0;
                  break;
                case "srcSet":
                  s = !0;
                  break;
                case "children":
                case "dangerouslySetInnerHTML":
                  throw Error(U(137, n));
                default:
                  Ht(l, n, r, m, u, null);
              }
          }
        s && Ht(l, n, "srcSet", u.srcSet, u, null), i && Ht(l, n, "src", u.src, u, null);
        return;
      case "input":
        ct("invalid", l);
        var v = r = m = s = null, A = null, j = null;
        for (i in u)
          if (u.hasOwnProperty(i)) {
            var V = u[i];
            if (V != null)
              switch (i) {
                case "name":
                  s = V;
                  break;
                case "type":
                  m = V;
                  break;
                case "checked":
                  A = V;
                  break;
                case "defaultChecked":
                  j = V;
                  break;
                case "value":
                  r = V;
                  break;
                case "defaultValue":
                  v = V;
                  break;
                case "children":
                case "dangerouslySetInnerHTML":
                  if (V != null)
                    throw Error(U(137, n));
                  break;
                default:
                  Ht(l, n, i, V, u, null);
              }
          }
        vs(
          l,
          r,
          v,
          A,
          j,
          m,
          s,
          !1
        );
        return;
      case "select":
        ct("invalid", l), i = m = r = null;
        for (s in u)
          if (u.hasOwnProperty(s) && (v = u[s], v != null))
            switch (s) {
              case "value":
                r = v;
                break;
              case "defaultValue":
                m = v;
                break;
              case "multiple":
                i = v;
              default:
                Ht(l, n, s, v, u, null);
            }
        n = r, u = m, l.multiple = !!i, n != null ? wo(l, !!i, n, !1) : u != null && wo(l, !!i, u, !0);
        return;
      case "textarea":
        ct("invalid", l), r = s = i = null;
        for (m in u)
          if (u.hasOwnProperty(m) && (v = u[m], v != null))
            switch (m) {
              case "value":
                i = v;
                break;
              case "defaultValue":
                s = v;
                break;
              case "children":
                r = v;
                break;
              case "dangerouslySetInnerHTML":
                if (v != null) throw Error(U(91));
                break;
              default:
                Ht(l, n, m, v, u, null);
            }
        xm(l, i, s, r);
        return;
      case "option":
        for (A in u)
          u.hasOwnProperty(A) && (i = u[A], i != null) && (A === "selected" ? l.selected = i && typeof i != "function" && typeof i != "symbol" : Ht(l, n, A, i, u, null));
        return;
      case "dialog":
        ct("beforetoggle", l), ct("toggle", l), ct("cancel", l), ct("close", l);
        break;
      case "iframe":
      case "object":
        ct("load", l);
        break;
      case "video":
      case "audio":
        for (i = 0; i < _f.length; i++)
          ct(_f[i], l);
        break;
      case "image":
        ct("error", l), ct("load", l);
        break;
      case "details":
        ct("toggle", l);
        break;
      case "embed":
      case "source":
      case "link":
        ct("error", l), ct("load", l);
      case "area":
      case "base":
      case "br":
      case "col":
      case "hr":
      case "keygen":
      case "meta":
      case "param":
      case "track":
      case "wbr":
      case "menuitem":
        for (j in u)
          if (u.hasOwnProperty(j) && (i = u[j], i != null))
            switch (j) {
              case "children":
              case "dangerouslySetInnerHTML":
                throw Error(U(137, n));
              default:
                Ht(l, n, j, i, u, null);
            }
        return;
      default:
        if (Nm(n)) {
          for (V in u)
            u.hasOwnProperty(V) && (i = u[V], i !== void 0 && d0(
              l,
              n,
              V,
              i,
              u,
              void 0
            ));
          return;
        }
    }
    for (v in u)
      u.hasOwnProperty(v) && (i = u[v], i != null && Ht(l, n, v, i, u, null));
  }
  function h0(l, n, u, i) {
    switch (n) {
      case "div":
      case "span":
      case "svg":
      case "path":
      case "a":
      case "g":
      case "p":
      case "li":
        break;
      case "input":
        var s = null, r = null, m = null, v = null, A = null, j = null, V = null;
        for (X in u) {
          var $ = u[X];
          if (u.hasOwnProperty(X) && $ != null)
            switch (X) {
              case "checked":
                break;
              case "value":
                break;
              case "defaultValue":
                A = $;
              default:
                i.hasOwnProperty(X) || Ht(l, n, X, null, i, $);
            }
        }
        for (var B in i) {
          var X = i[B];
          if ($ = u[B], i.hasOwnProperty(B) && (X != null || $ != null))
            switch (B) {
              case "type":
                r = X;
                break;
              case "name":
                s = X;
                break;
              case "checked":
                j = X;
                break;
              case "defaultChecked":
                V = X;
                break;
              case "value":
                m = X;
                break;
              case "defaultValue":
                v = X;
                break;
              case "children":
              case "dangerouslySetInnerHTML":
                if (X != null)
                  throw Error(U(137, n));
                break;
              default:
                X !== $ && Ht(
                  l,
                  n,
                  B,
                  X,
                  i,
                  $
                );
            }
        }
        gs(
          l,
          m,
          v,
          A,
          j,
          V,
          r,
          s
        );
        return;
      case "select":
        X = m = v = B = null;
        for (r in u)
          if (A = u[r], u.hasOwnProperty(r) && A != null)
            switch (r) {
              case "value":
                break;
              case "multiple":
                X = A;
              default:
                i.hasOwnProperty(r) || Ht(
                  l,
                  n,
                  r,
                  null,
                  i,
                  A
                );
            }
        for (s in i)
          if (r = i[s], A = u[s], i.hasOwnProperty(s) && (r != null || A != null))
            switch (s) {
              case "value":
                B = r;
                break;
              case "defaultValue":
                v = r;
                break;
              case "multiple":
                m = r;
              default:
                r !== A && Ht(
                  l,
                  n,
                  s,
                  r,
                  i,
                  A
                );
            }
        n = v, u = m, i = X, B != null ? wo(l, !!u, B, !1) : !!i != !!u && (n != null ? wo(l, !!u, n, !0) : wo(l, !!u, u ? [] : "", !1));
        return;
      case "textarea":
        X = B = null;
        for (v in u)
          if (s = u[v], u.hasOwnProperty(v) && s != null && !i.hasOwnProperty(v))
            switch (v) {
              case "value":
                break;
              case "children":
                break;
              default:
                Ht(l, n, v, null, i, s);
            }
        for (m in i)
          if (s = i[m], r = u[m], i.hasOwnProperty(m) && (s != null || r != null))
            switch (m) {
              case "value":
                B = s;
                break;
              case "defaultValue":
                X = s;
                break;
              case "children":
                break;
              case "dangerouslySetInnerHTML":
                if (s != null) throw Error(U(91));
                break;
              default:
                s !== r && Ht(l, n, m, s, i, r);
            }
        Um(l, B, X);
        return;
      case "option":
        for (var re in u)
          B = u[re], u.hasOwnProperty(re) && B != null && !i.hasOwnProperty(re) && (re === "selected" ? l.selected = !1 : Ht(
            l,
            n,
            re,
            null,
            i,
            B
          ));
        for (A in i)
          B = i[A], X = u[A], i.hasOwnProperty(A) && B !== X && (B != null || X != null) && (A === "selected" ? l.selected = B && typeof B != "function" && typeof B != "symbol" : Ht(
            l,
            n,
            A,
            B,
            i,
            X
          ));
        return;
      case "img":
      case "link":
      case "area":
      case "base":
      case "br":
      case "col":
      case "embed":
      case "hr":
      case "keygen":
      case "meta":
      case "param":
      case "source":
      case "track":
      case "wbr":
      case "menuitem":
        for (var _e in u)
          B = u[_e], u.hasOwnProperty(_e) && B != null && !i.hasOwnProperty(_e) && Ht(l, n, _e, null, i, B);
        for (j in i)
          if (B = i[j], X = u[j], i.hasOwnProperty(j) && B !== X && (B != null || X != null))
            switch (j) {
              case "children":
              case "dangerouslySetInnerHTML":
                if (B != null)
                  throw Error(U(137, n));
                break;
              default:
                Ht(
                  l,
                  n,
                  j,
                  B,
                  i,
                  X
                );
            }
        return;
      default:
        if (Nm(n)) {
          for (var jt in u)
            B = u[jt], u.hasOwnProperty(jt) && B !== void 0 && !i.hasOwnProperty(jt) && d0(
              l,
              n,
              jt,
              void 0,
              i,
              B
            );
          for (V in i)
            B = i[V], X = u[V], !i.hasOwnProperty(V) || B === X || B === void 0 && X === void 0 || d0(
              l,
              n,
              V,
              B,
              i,
              X
            );
          return;
        }
    }
    for (var C in u)
      B = u[C], u.hasOwnProperty(C) && B != null && !i.hasOwnProperty(C) && Ht(l, n, C, null, i, B);
    for ($ in i)
      B = i[$], X = u[$], !i.hasOwnProperty($) || B === X || B == null && X == null || Ht(l, n, $, B, i, X);
  }
  function Mh(l) {
    switch (l) {
      case "css":
      case "script":
      case "font":
      case "img":
      case "image":
      case "input":
      case "link":
        return !0;
      default:
        return !1;
    }
  }
  function m0() {
    if (typeof performance.getEntriesByType == "function") {
      for (var l = 0, n = 0, u = performance.getEntriesByType("resource"), i = 0; i < u.length; i++) {
        var s = u[i], r = s.transferSize, m = s.initiatorType, v = s.duration;
        if (r && v && Mh(m)) {
          for (m = 0, v = s.responseEnd, i += 1; i < u.length; i++) {
            var A = u[i], j = A.startTime;
            if (j > v) break;
            var V = A.transferSize, $ = A.initiatorType;
            V && Mh($) && (A = A.responseEnd, m += V * (A < v ? 1 : (v - j) / (A - j)));
          }
          if (--i, n += 8 * (r + m) / (s.duration / 1e3), l++, 10 < l) break;
        }
      }
      if (0 < l) return n / l / 1e6;
    }
    return navigator.connection && (l = navigator.connection.downlink, typeof l == "number") ? l : 5;
  }
  var Ch = null, Uh = null;
  function fi(l) {
    return l.nodeType === 9 ? l : l.ownerDocument;
  }
  function Yg(l) {
    switch (l) {
      case "http://www.w3.org/2000/svg":
        return 1;
      case "http://www.w3.org/1998/Math/MathML":
        return 2;
      default:
        return 0;
    }
  }
  function y0(l, n) {
    if (l === 0)
      switch (n) {
        case "svg":
          return 1;
        case "math":
          return 2;
        default:
          return 0;
      }
    return l === 1 && n === "foreignObject" ? 0 : l;
  }
  function Cf(l, n) {
    return l === "textarea" || l === "noscript" || typeof n.children == "string" || typeof n.children == "number" || typeof n.children == "bigint" || typeof n.dangerouslySetInnerHTML == "object" && n.dangerouslySetInnerHTML !== null && n.dangerouslySetInnerHTML.__html != null;
  }
  var xh = null;
  function f1() {
    var l = window.event;
    return l && l.type === "popstate" ? l === xh ? !1 : (xh = l, !0) : (xh = null, !1);
  }
  var Tr = typeof setTimeout == "function" ? setTimeout : void 0, qg = typeof clearTimeout == "function" ? clearTimeout : void 0, oo = typeof Promise == "function" ? Promise : void 0, wg = typeof queueMicrotask == "function" ? queueMicrotask : typeof oo < "u" ? function(l) {
    return oo.resolve(null).then(l).catch(p0);
  } : Tr;
  function p0(l) {
    setTimeout(function() {
      throw l;
    });
  }
  function In(l) {
    return l === "head";
  }
  function g0(l, n) {
    var u = n, i = 0;
    do {
      var s = u.nextSibling;
      if (l.removeChild(u), s && s.nodeType === 8)
        if (u = s.data, u === "/$" || u === "/&") {
          if (i === 0) {
            l.removeChild(s), Lf(n);
            return;
          }
          i--;
        } else if (u === "$" || u === "$?" || u === "$~" || u === "$!" || u === "&")
          i++;
        else if (u === "html")
          fo(l.ownerDocument.documentElement);
        else if (u === "head") {
          u = l.ownerDocument.head, fo(u);
          for (var r = u.firstChild; r; ) {
            var m = r.nextSibling, v = r.nodeName;
            r[su] || v === "SCRIPT" || v === "STYLE" || v === "LINK" && r.rel.toLowerCase() === "stylesheet" || u.removeChild(r), r = m;
          }
        } else
          u === "body" && fo(l.ownerDocument.body);
      u = s;
    } while (u);
    Lf(n);
  }
  function vl(l, n) {
    var u = l;
    l = 0;
    do {
      var i = u.nextSibling;
      if (u.nodeType === 1 ? n ? (u._stashedDisplay = u.style.display, u.style.display = "none") : (u.style.display = u._stashedDisplay || "", u.getAttribute("style") === "" && u.removeAttribute("style")) : u.nodeType === 3 && (n ? (u._stashedText = u.nodeValue, u.nodeValue = "") : u.nodeValue = u._stashedText || ""), i && i.nodeType === 8)
        if (u = i.data, u === "/$") {
          if (l === 0) break;
          l--;
        } else
          u !== "$" && u !== "$?" && u !== "$~" && u !== "$!" || l++;
      u = i;
    } while (u);
  }
  function Ar(l) {
    var n = l.firstChild;
    for (n && n.nodeType === 10 && (n = n.nextSibling); n; ) {
      var u = n;
      switch (n = n.nextSibling, u.nodeName) {
        case "HTML":
        case "HEAD":
        case "BODY":
          Ar(u), cd(u);
          continue;
        case "SCRIPT":
        case "STYLE":
          continue;
        case "LINK":
          if (u.rel.toLowerCase() === "stylesheet") continue;
      }
      l.removeChild(u);
    }
  }
  function s1(l, n, u, i) {
    for (; l.nodeType === 1; ) {
      var s = u;
      if (l.nodeName.toLowerCase() !== n.toLowerCase()) {
        if (!i && (l.nodeName !== "INPUT" || l.type !== "hidden"))
          break;
      } else if (i) {
        if (!l[su])
          switch (n) {
            case "meta":
              if (!l.hasAttribute("itemprop")) break;
              return l;
            case "link":
              if (r = l.getAttribute("rel"), r === "stylesheet" && l.hasAttribute("data-precedence"))
                break;
              if (r !== s.rel || l.getAttribute("href") !== (s.href == null || s.href === "" ? null : s.href) || l.getAttribute("crossorigin") !== (s.crossOrigin == null ? null : s.crossOrigin) || l.getAttribute("title") !== (s.title == null ? null : s.title))
                break;
              return l;
            case "style":
              if (l.hasAttribute("data-precedence")) break;
              return l;
            case "script":
              if (r = l.getAttribute("src"), (r !== (s.src == null ? null : s.src) || l.getAttribute("type") !== (s.type == null ? null : s.type) || l.getAttribute("crossorigin") !== (s.crossOrigin == null ? null : s.crossOrigin)) && r && l.hasAttribute("async") && !l.hasAttribute("itemprop"))
                break;
              return l;
            default:
              return l;
          }
      } else if (n === "input" && l.type === "hidden") {
        var r = s.name == null ? null : "" + s.name;
        if (s.type === "hidden" && l.getAttribute("name") === r)
          return l;
      } else return l;
      if (l = za(l.nextSibling), l === null) break;
    }
    return null;
  }
  function Ie(l, n, u) {
    if (n === "") return null;
    for (; l.nodeType !== 3; )
      if ((l.nodeType !== 1 || l.nodeName !== "INPUT" || l.type !== "hidden") && !u || (l = za(l.nextSibling), l === null)) return null;
    return l;
  }
  function Gg(l, n) {
    for (; l.nodeType !== 8; )
      if ((l.nodeType !== 1 || l.nodeName !== "INPUT" || l.type !== "hidden") && !n || (l = za(l.nextSibling), l === null)) return null;
    return l;
  }
  function Dn(l) {
    return l.data === "$?" || l.data === "$~";
  }
  function si(l) {
    return l.data === "$!" || l.data === "$?" && l.ownerDocument.readyState !== "loading";
  }
  function Uf(l, n) {
    var u = l.ownerDocument;
    if (l.data === "$~") l._reactRetry = n;
    else if (l.data !== "$?" || u.readyState !== "loading")
      n();
    else {
      var i = function() {
        n(), u.removeEventListener("DOMContentLoaded", i);
      };
      u.addEventListener("DOMContentLoaded", i), l._reactRetry = i;
    }
  }
  function za(l) {
    for (; l != null; l = l.nextSibling) {
      var n = l.nodeType;
      if (n === 1 || n === 3) break;
      if (n === 8) {
        if (n = l.data, n === "$" || n === "$!" || n === "$?" || n === "$~" || n === "&" || n === "F!" || n === "F")
          break;
        if (n === "/$" || n === "/&") return null;
      }
    }
    return l;
  }
  var Or = null;
  function Nh(l) {
    l = l.nextSibling;
    for (var n = 0; l; ) {
      if (l.nodeType === 8) {
        var u = l.data;
        if (u === "/$" || u === "/&") {
          if (n === 0)
            return za(l.nextSibling);
          n--;
        } else
          u !== "$" && u !== "$!" && u !== "$?" && u !== "$~" && u !== "&" || n++;
      }
      l = l.nextSibling;
    }
    return null;
  }
  function Pn(l) {
    l = l.previousSibling;
    for (var n = 0; l; ) {
      if (l.nodeType === 8) {
        var u = l.data;
        if (u === "$" || u === "$!" || u === "$?" || u === "$~" || u === "&") {
          if (n === 0) return l;
          n--;
        } else u !== "/$" && u !== "/&" || n++;
      }
      l = l.previousSibling;
    }
    return null;
  }
  function xf(l, n, u) {
    switch (n = fi(u), l) {
      case "html":
        if (l = n.documentElement, !l) throw Error(U(452));
        return l;
      case "head":
        if (l = n.head, !l) throw Error(U(453));
        return l;
      case "body":
        if (l = n.body, !l) throw Error(U(454));
        return l;
      default:
        throw Error(U(451));
    }
  }
  function fo(l) {
    for (var n = l.attributes; n.length; )
      l.removeAttributeNode(n[0]);
    cd(l);
  }
  var Ha = /* @__PURE__ */ new Map(), zr = /* @__PURE__ */ new Set();
  function ca(l) {
    return typeof l.getRootNode == "function" ? l.getRootNode() : l.nodeType === 9 ? l : l.ownerDocument;
  }
  var eu = Z.d;
  Z.d = {
    f: r1,
    r: Xg,
    D: G,
    C: At,
    L: d1,
    m: v0,
    X: bc,
    S: S0,
    M: ri
  };
  function r1() {
    var l = eu.f(), n = Af();
    return l || n;
  }
  function Xg(l) {
    var n = Ai(l);
    n !== null && n.tag === 5 && n.type === "form" ? xt(n) : eu.r(l);
  }
  var Nf = typeof document > "u" ? null : document;
  function Al(l, n, u) {
    var i = Nf;
    if (i && typeof n == "string" && n) {
      var s = Va(n);
      s = 'link[rel="' + l + '"][href="' + s + '"]', typeof u == "string" && (s += '[crossorigin="' + u + '"]'), zr.has(s) || (zr.add(s), l = { rel: l, crossOrigin: u, href: n }, i.querySelector(s) === null && (n = i.createElement("link"), Wl(n, "link", l), zt(n), i.head.appendChild(n)));
    }
  }
  function G(l) {
    eu.D(l), Al("dns-prefetch", l, null);
  }
  function At(l, n) {
    eu.C(l, n), Al("preconnect", l, n);
  }
  function d1(l, n, u) {
    eu.L(l, n, u);
    var i = Nf;
    if (i && l && n) {
      var s = 'link[rel="preload"][as="' + Va(n) + '"]';
      n === "image" && u && u.imageSrcSet ? (s += '[imagesrcset="' + Va(
        u.imageSrcSet
      ) + '"]', typeof u.imageSizes == "string" && (s += '[imagesizes="' + Va(
        u.imageSizes
      ) + '"]')) : s += '[href="' + Va(l) + '"]';
      var r = s;
      switch (n) {
        case "style":
          r = nn(l);
          break;
        case "script":
          r = so(l);
      }
      Ha.has(r) || (l = w(
        {
          rel: "preload",
          href: n === "image" && u && u.imageSrcSet ? void 0 : l,
          as: n
        },
        u
      ), Ha.set(r, l), i.querySelector(s) !== null || n === "style" && i.querySelector(di(r)) || n === "script" && i.querySelector(Bf(r)) || (n = i.createElement("link"), Wl(n, "link", l), zt(n), i.head.appendChild(n)));
    }
  }
  function v0(l, n) {
    eu.m(l, n);
    var u = Nf;
    if (u && l) {
      var i = n && typeof n.as == "string" ? n.as : "script", s = 'link[rel="modulepreload"][as="' + Va(i) + '"][href="' + Va(l) + '"]', r = s;
      switch (i) {
        case "audioworklet":
        case "paintworklet":
        case "serviceworker":
        case "sharedworker":
        case "worker":
        case "script":
          r = so(l);
      }
      if (!Ha.has(r) && (l = w({ rel: "modulepreload", href: l }, n), Ha.set(r, l), u.querySelector(s) === null)) {
        switch (i) {
          case "audioworklet":
          case "paintworklet":
          case "serviceworker":
          case "sharedworker":
          case "worker":
          case "script":
            if (u.querySelector(Bf(r)))
              return;
        }
        i = u.createElement("link"), Wl(i, "link", l), zt(i), u.head.appendChild(i);
      }
    }
  }
  function S0(l, n, u) {
    eu.S(l, n, u);
    var i = Nf;
    if (i && l) {
      var s = Oi(i).hoistableStyles, r = nn(l);
      n = n || "default";
      var m = s.get(r);
      if (!m) {
        var v = { loading: 0, preload: null };
        if (m = i.querySelector(
          di(r)
        ))
          v.loading = 5;
        else {
          l = w(
            { rel: "stylesheet", href: l, "data-precedence": n },
            u
          ), (u = Ha.get(r)) && Hh(l, u);
          var A = m = i.createElement("link");
          zt(A), Wl(A, "link", l), A._p = new Promise(function(j, V) {
            A.onload = j, A.onerror = V;
          }), A.addEventListener("load", function() {
            v.loading |= 1;
          }), A.addEventListener("error", function() {
            v.loading |= 2;
          }), v.loading |= 4, Dr(m, n, i);
        }
        m = {
          type: "stylesheet",
          instance: m,
          count: 1,
          state: v
        }, s.set(r, m);
      }
    }
  }
  function bc(l, n) {
    eu.X(l, n);
    var u = Nf;
    if (u && l) {
      var i = Oi(u).hoistableScripts, s = so(l), r = i.get(s);
      r || (r = u.querySelector(Bf(s)), r || (l = w({ src: l, async: !0 }, n), (n = Ha.get(s)) && jh(l, n), r = u.createElement("script"), zt(r), Wl(r, "link", l), u.head.appendChild(r)), r = {
        type: "script",
        instance: r,
        count: 1,
        state: null
      }, i.set(s, r));
    }
  }
  function ri(l, n) {
    eu.M(l, n);
    var u = Nf;
    if (u && l) {
      var i = Oi(u).hoistableScripts, s = so(l), r = i.get(s);
      r || (r = u.querySelector(Bf(s)), r || (l = w({ src: l, async: !0, type: "module" }, n), (n = Ha.get(s)) && jh(l, n), r = u.createElement("script"), zt(r), Wl(r, "link", l), u.head.appendChild(r)), r = {
        type: "script",
        instance: r,
        count: 1,
        state: null
      }, i.set(s, r));
    }
  }
  function Hf(l, n, u, i) {
    var s = (s = Le.current) ? ca(s) : null;
    if (!s) throw Error(U(446));
    switch (l) {
      case "meta":
      case "title":
        return null;
      case "style":
        return typeof u.precedence == "string" && typeof u.href == "string" ? (n = nn(u.href), u = Oi(
          s
        ).hoistableStyles, i = u.get(n), i || (i = {
          type: "style",
          instance: null,
          count: 0,
          state: null
        }, u.set(n, i)), i) : { type: "void", instance: null, count: 0, state: null };
      case "link":
        if (u.rel === "stylesheet" && typeof u.href == "string" && typeof u.precedence == "string") {
          l = nn(u.href);
          var r = Oi(
            s
          ).hoistableStyles, m = r.get(l);
          if (m || (s = s.ownerDocument || s, m = {
            type: "stylesheet",
            instance: null,
            count: 0,
            state: { loading: 0, preload: null }
          }, r.set(l, m), (r = s.querySelector(
            di(l)
          )) && !r._p && (m.instance = r, m.state.loading = 5), Ha.has(l) || (u = {
            rel: "preload",
            as: "style",
            href: u.href,
            crossOrigin: u.crossOrigin,
            integrity: u.integrity,
            media: u.media,
            hrefLang: u.hrefLang,
            referrerPolicy: u.referrerPolicy
          }, Ha.set(l, u), r || Lg(
            s,
            l,
            u,
            m.state
          ))), n && i === null)
            throw Error(U(528, ""));
          return m;
        }
        if (n && i !== null)
          throw Error(U(529, ""));
        return null;
      case "script":
        return n = u.async, u = u.src, typeof u == "string" && n && typeof n != "function" && typeof n != "symbol" ? (n = so(u), u = Oi(
          s
        ).hoistableScripts, i = u.get(n), i || (i = {
          type: "script",
          instance: null,
          count: 0,
          state: null
        }, u.set(n, i)), i) : { type: "void", instance: null, count: 0, state: null };
      default:
        throw Error(U(444, l));
    }
  }
  function nn(l) {
    return 'href="' + Va(l) + '"';
  }
  function di(l) {
    return 'link[rel="stylesheet"][' + l + "]";
  }
  function jf(l) {
    return w({}, l, {
      "data-precedence": l.precedence,
      precedence: null
    });
  }
  function Lg(l, n, u, i) {
    l.querySelector('link[rel="preload"][as="style"][' + n + "]") ? i.loading = 1 : (n = l.createElement("link"), i.preload = n, n.addEventListener("load", function() {
      return i.loading |= 1;
    }), n.addEventListener("error", function() {
      return i.loading |= 2;
    }), Wl(n, "link", u), zt(n), l.head.appendChild(n));
  }
  function so(l) {
    return '[src="' + Va(l) + '"]';
  }
  function Bf(l) {
    return "script[async]" + l;
  }
  function b0(l, n, u) {
    if (n.count++, n.instance === null)
      switch (n.type) {
        case "style":
          var i = l.querySelector(
            'style[data-href~="' + Va(u.href) + '"]'
          );
          if (i)
            return n.instance = i, zt(i), i;
          var s = w({}, u, {
            "data-href": u.href,
            "data-precedence": u.precedence,
            href: null,
            precedence: null
          });
          return i = (l.ownerDocument || l).createElement(
            "style"
          ), zt(i), Wl(i, "style", s), Dr(i, u.precedence, l), n.instance = i;
        case "stylesheet":
          s = nn(u.href);
          var r = l.querySelector(
            di(s)
          );
          if (r)
            return n.state.loading |= 4, n.instance = r, zt(r), r;
          i = jf(u), (s = Ha.get(s)) && Hh(i, s), r = (l.ownerDocument || l).createElement("link"), zt(r);
          var m = r;
          return m._p = new Promise(function(v, A) {
            m.onload = v, m.onerror = A;
          }), Wl(r, "link", i), n.state.loading |= 4, Dr(r, u.precedence, l), n.instance = r;
        case "script":
          return r = so(u.src), (s = l.querySelector(
            Bf(r)
          )) ? (n.instance = s, zt(s), s) : (i = u, (s = Ha.get(r)) && (i = w({}, u), jh(i, s)), l = l.ownerDocument || l, s = l.createElement("script"), zt(s), Wl(s, "link", i), l.head.appendChild(s), n.instance = s);
        case "void":
          return null;
        default:
          throw Error(U(443, n.type));
      }
    else
      n.type === "stylesheet" && (n.state.loading & 4) === 0 && (i = n.instance, n.state.loading |= 4, Dr(i, u.precedence, l));
    return n.instance;
  }
  function Dr(l, n, u) {
    for (var i = u.querySelectorAll(
      'link[rel="stylesheet"][data-precedence],style[data-precedence]'
    ), s = i.length ? i[i.length - 1] : null, r = s, m = 0; m < i.length; m++) {
      var v = i[m];
      if (v.dataset.precedence === n) r = v;
      else if (r !== s) break;
    }
    r ? r.parentNode.insertBefore(l, r.nextSibling) : (n = u.nodeType === 9 ? u.head : u, n.insertBefore(l, n.firstChild));
  }
  function Hh(l, n) {
    l.crossOrigin == null && (l.crossOrigin = n.crossOrigin), l.referrerPolicy == null && (l.referrerPolicy = n.referrerPolicy), l.title == null && (l.title = n.title);
  }
  function jh(l, n) {
    l.crossOrigin == null && (l.crossOrigin = n.crossOrigin), l.referrerPolicy == null && (l.referrerPolicy = n.referrerPolicy), l.integrity == null && (l.integrity = n.integrity);
  }
  var Yf = null;
  function E0(l, n, u) {
    if (Yf === null) {
      var i = /* @__PURE__ */ new Map(), s = Yf = /* @__PURE__ */ new Map();
      s.set(u, i);
    } else
      s = Yf, i = s.get(u), i || (i = /* @__PURE__ */ new Map(), s.set(u, i));
    if (i.has(l)) return i;
    for (i.set(l, null), u = u.getElementsByTagName(l), s = 0; s < u.length; s++) {
      var r = u[s];
      if (!(r[su] || r[Ut] || l === "link" && r.getAttribute("rel") === "stylesheet") && r.namespaceURI !== "http://www.w3.org/2000/svg") {
        var m = r.getAttribute(n) || "";
        m = l + m;
        var v = i.get(m);
        v ? v.push(r) : i.set(m, [r]);
      }
    }
    return i;
  }
  function Bh(l, n, u) {
    l = l.ownerDocument || l, l.head.insertBefore(
      u,
      n === "title" ? l.querySelector("head > title") : null
    );
  }
  function T0(l, n, u) {
    if (u === 1 || n.itemProp != null) return !1;
    switch (l) {
      case "meta":
      case "title":
        return !0;
      case "style":
        if (typeof n.precedence != "string" || typeof n.href != "string" || n.href === "")
          break;
        return !0;
      case "link":
        if (typeof n.rel != "string" || typeof n.href != "string" || n.href === "" || n.onLoad || n.onError)
          break;
        return n.rel === "stylesheet" ? (l = n.disabled, typeof n.precedence == "string" && l == null) : !0;
      case "script":
        if (n.async && typeof n.async != "function" && typeof n.async != "symbol" && !n.onLoad && !n.onError && n.src && typeof n.src == "string")
          return !0;
    }
    return !1;
  }
  function ja(l) {
    return !(l.type === "stylesheet" && (l.state.loading & 3) === 0);
  }
  function Yu(l, n, u, i) {
    if (u.type === "stylesheet" && (typeof i.media != "string" || matchMedia(i.media).matches !== !1) && (u.state.loading & 4) === 0) {
      if (u.instance === null) {
        var s = nn(i.href), r = n.querySelector(
          di(s)
        );
        if (r) {
          n = r._p, n !== null && typeof n == "object" && typeof n.then == "function" && (l.count++, l = Yh.bind(l), n.then(l, l)), u.state.loading |= 4, u.instance = r, zt(r);
          return;
        }
        r = n.ownerDocument || n, i = jf(i), (s = Ha.get(s)) && Hh(i, s), r = r.createElement("link"), zt(r);
        var m = r;
        m._p = new Promise(function(v, A) {
          m.onload = v, m.onerror = A;
        }), Wl(r, "link", i), u.instance = r;
      }
      l.stylesheets === null && (l.stylesheets = /* @__PURE__ */ new Map()), l.stylesheets.set(u, n), (n = u.state.preload) && (u.state.loading & 3) === 0 && (l.count++, u = Yh.bind(l), n.addEventListener("load", u), n.addEventListener("error", u));
    }
  }
  var un = 0;
  function A0(l, n) {
    return l.stylesheets && l.count === 0 && wh(l, l.stylesheets), 0 < l.count || 0 < l.imgCount ? function(u) {
      var i = setTimeout(function() {
        if (l.stylesheets && wh(l, l.stylesheets), l.unsuspend) {
          var r = l.unsuspend;
          l.unsuspend = null, r();
        }
      }, 6e4 + n);
      0 < l.imgBytes && un === 0 && (un = 62500 * m0());
      var s = setTimeout(
        function() {
          if (l.waitingForImages = !1, l.count === 0 && (l.stylesheets && wh(l, l.stylesheets), l.unsuspend)) {
            var r = l.unsuspend;
            l.unsuspend = null, r();
          }
        },
        (l.imgBytes > un ? 50 : 800) + n
      );
      return l.unsuspend = u, function() {
        l.unsuspend = null, clearTimeout(i), clearTimeout(s);
      };
    } : null;
  }
  function Yh() {
    if (this.count--, this.count === 0 && (this.imgCount === 0 || !this.waitingForImages)) {
      if (this.stylesheets) wh(this, this.stylesheets);
      else if (this.unsuspend) {
        var l = this.unsuspend;
        this.unsuspend = null, l();
      }
    }
  }
  var qh = null;
  function wh(l, n) {
    l.stylesheets = null, l.unsuspend !== null && (l.count++, qh = /* @__PURE__ */ new Map(), n.forEach(Xl, l), qh = null, Yh.call(l));
  }
  function Xl(l, n) {
    if (!(n.state.loading & 4)) {
      var u = qh.get(l);
      if (u) var i = u.get(null);
      else {
        u = /* @__PURE__ */ new Map(), qh.set(l, u);
        for (var s = l.querySelectorAll(
          "link[data-precedence],style[data-precedence]"
        ), r = 0; r < s.length; r++) {
          var m = s[r];
          (m.nodeName === "LINK" || m.getAttribute("media") !== "not all") && (u.set(m.dataset.precedence, m), i = m);
        }
        i && u.set(null, i);
      }
      s = n.instance, m = s.getAttribute("data-precedence"), r = u.get(m) || i, r === i && u.set(null, s), u.set(m, s), this.count++, i = Yh.bind(this), s.addEventListener("load", i), s.addEventListener("error", i), r ? r.parentNode.insertBefore(s, r.nextSibling) : (l = l.nodeType === 9 ? l.head : l, l.insertBefore(s, l.firstChild)), n.state.loading |= 4;
    }
  }
  var Rr = {
    $$typeof: Ot,
    Provider: null,
    Consumer: null,
    _currentValue: ee,
    _currentValue2: ee,
    _threadCount: 0
  };
  function O0(l, n, u, i, s, r, m, v, A) {
    this.tag = 1, this.containerInfo = l, this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.next = this.pendingContext = this.context = this.cancelPendingCommit = null, this.callbackPriority = 0, this.expirationTimes = mn(-1), this.entangledLanes = this.shellSuspendCounter = this.errorRecoveryDisabledLanes = this.expiredLanes = this.warmLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = mn(0), this.hiddenUpdates = mn(null), this.identifierPrefix = i, this.onUncaughtError = s, this.onCaughtError = r, this.onRecoverableError = m, this.pooledCache = null, this.pooledCacheLanes = 0, this.formState = A, this.incompleteTransitions = /* @__PURE__ */ new Map();
  }
  function Gh(l, n, u, i, s, r, m, v, A, j, V, $) {
    return l = new O0(
      l,
      n,
      u,
      m,
      A,
      j,
      V,
      $,
      v
    ), n = 1, r === !0 && (n |= 24), r = ol(3, null, null, n), l.current = r, r.stateNode = l, n = js(), n.refCount++, l.pooledCache = n, n.refCount++, r.memoizedState = {
      element: i,
      isDehydrated: u,
      cache: n
    }, Ls(r), l;
  }
  function ro(l) {
    return l ? (l = ma, l) : ma;
  }
  function Qg(l, n, u, i, s, r) {
    s = ro(s), i.context === null ? i.context = s : i.pendingContext = s, i = sc(n), i.payload = { element: u }, r = r === void 0 ? null : r, r !== null && (i.callback = r), u = Fa(l, i, n), u !== null && (Oa(u, l, n), Wc(u, l, n));
  }
  function Xh(l, n) {
    if (l = l.memoizedState, l !== null && l.dehydrated !== null) {
      var u = l.retryLane;
      l.retryLane = u !== 0 && u < n ? u : n;
    }
  }
  function z0(l, n) {
    Xh(l, n), (l = l.alternate) && Xh(l, n);
  }
  function Vg(l) {
    if (l.tag === 13 || l.tag === 31) {
      var n = ac(l, 67108864);
      n !== null && Oa(n, l, 67108864), z0(l, 67108864);
    }
  }
  function ho(l) {
    if (l.tag === 13 || l.tag === 31) {
      var n = Na();
      n = ad(n);
      var u = ac(l, n);
      u !== null && Oa(u, l, n), z0(l, n);
    }
  }
  var Ml = !0;
  function qu(l, n, u, i) {
    var s = R.T;
    R.T = null;
    var r = Z.p;
    try {
      Z.p = 2, Fl(l, n, u, i);
    } finally {
      Z.p = r, R.T = s;
    }
  }
  function wu(l, n, u, i) {
    var s = R.T;
    R.T = null;
    var r = Z.p;
    try {
      Z.p = 8, Fl(l, n, u, i);
    } finally {
      Z.p = r, R.T = s;
    }
  }
  function Fl(l, n, u, i) {
    if (Ml) {
      var s = D0(i);
      if (s === null)
        o0(
          l,
          n,
          i,
          Lh,
          u
        ), Ec(l, i);
      else if (h1(
        s,
        l,
        n,
        u,
        i
      ))
        i.stopPropagation();
      else if (Ec(l, i), n & 4 && -1 < Da.indexOf(l)) {
        for (; s !== null; ) {
          var r = Ai(s);
          if (r !== null)
            switch (r.tag) {
              case 3:
                if (r = r.stateNode, r.current.memoizedState.isDehydrated) {
                  var m = Ce(r.pendingLanes);
                  if (m !== 0) {
                    var v = r;
                    for (v.pendingLanes |= 2, v.entangledLanes |= 2; m; ) {
                      var A = 1 << 31 - Nl(m);
                      v.entanglements[1] |= A, m &= ~A;
                    }
                    Bu(r), (St & 6) === 0 && (Tt = bl() + 500, Sc(0));
                  }
                }
                break;
              case 31:
              case 13:
                v = ac(r, 2), v !== null && Oa(v, r, 2), Af(), z0(r, 2);
            }
          if (r = D0(i), r === null && o0(
            l,
            n,
            i,
            Lh,
            u
          ), r === s) break;
          s = r;
        }
        s !== null && i.stopPropagation();
      } else
        o0(
          l,
          n,
          i,
          null,
          u
        );
    }
  }
  function D0(l) {
    return l = hd(l), qf(l);
  }
  var Lh = null;
  function qf(l) {
    if (Lh = null, l = Ti(l), l !== null) {
      var n = Se(l);
      if (n === null) l = null;
      else {
        var u = n.tag;
        if (u === 13) {
          if (l = mt(n), l !== null) return l;
          l = null;
        } else if (u === 31) {
          if (l = le(n), l !== null) return l;
          l = null;
        } else if (u === 3) {
          if (n.stateNode.current.memoizedState.isDehydrated)
            return n.tag === 3 ? n.stateNode.containerInfo : null;
          l = null;
        } else n !== l && (l = null);
      }
    }
    return Lh = l, null;
  }
  function _r(l) {
    switch (l) {
      case "beforetoggle":
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "toggle":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 2;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 8;
      case "message":
        switch (td()) {
          case Uo:
            return 2;
          case xo:
            return 8;
          case Un:
          case ld:
            return 32;
          case No:
            return 268435456;
          default:
            return 32;
        }
      default:
        return 32;
    }
  }
  var wf = !1, Cl = null, Il = null, ia = null, hi = /* @__PURE__ */ new Map(), Rn = /* @__PURE__ */ new Map(), el = [], Da = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(
    " "
  );
  function Ec(l, n) {
    switch (l) {
      case "focusin":
      case "focusout":
        Cl = null;
        break;
      case "dragenter":
      case "dragleave":
        Il = null;
        break;
      case "mouseover":
      case "mouseout":
        ia = null;
        break;
      case "pointerover":
      case "pointerout":
        hi.delete(n.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        Rn.delete(n.pointerId);
    }
  }
  function mo(l, n, u, i, s, r) {
    return l === null || l.nativeEvent !== r ? (l = {
      blockedOn: n,
      domEventName: u,
      eventSystemFlags: i,
      nativeEvent: r,
      targetContainers: [s]
    }, n !== null && (n = Ai(n), n !== null && Vg(n)), l) : (l.eventSystemFlags |= i, n = l.targetContainers, s !== null && n.indexOf(s) === -1 && n.push(s), l);
  }
  function h1(l, n, u, i, s) {
    switch (n) {
      case "focusin":
        return Cl = mo(
          Cl,
          l,
          n,
          u,
          i,
          s
        ), !0;
      case "dragenter":
        return Il = mo(
          Il,
          l,
          n,
          u,
          i,
          s
        ), !0;
      case "mouseover":
        return ia = mo(
          ia,
          l,
          n,
          u,
          i,
          s
        ), !0;
      case "pointerover":
        var r = s.pointerId;
        return hi.set(
          r,
          mo(
            hi.get(r) || null,
            l,
            n,
            u,
            i,
            s
          )
        ), !0;
      case "gotpointercapture":
        return r = s.pointerId, Rn.set(
          r,
          mo(
            Rn.get(r) || null,
            l,
            n,
            u,
            i,
            s
          )
        ), !0;
    }
    return !1;
  }
  function Zg(l) {
    var n = Ti(l.target);
    if (n !== null) {
      var u = Se(n);
      if (u !== null) {
        if (n = u.tag, n === 13) {
          if (n = mt(u), n !== null) {
            l.blockedOn = n, Dm(l.priority, function() {
              ho(u);
            });
            return;
          }
        } else if (n === 31) {
          if (n = le(u), n !== null) {
            l.blockedOn = n, Dm(l.priority, function() {
              ho(u);
            });
            return;
          }
        } else if (n === 3 && u.stateNode.current.memoizedState.isDehydrated) {
          l.blockedOn = u.tag === 3 ? u.stateNode.containerInfo : null;
          return;
        }
      }
    }
    l.blockedOn = null;
  }
  function Mr(l) {
    if (l.blockedOn !== null) return !1;
    for (var n = l.targetContainers; 0 < n.length; ) {
      var u = D0(l.nativeEvent);
      if (u === null) {
        u = l.nativeEvent;
        var i = new u.constructor(
          u.type,
          u
        );
        dd = i, u.target.dispatchEvent(i), dd = null;
      } else
        return n = Ai(u), n !== null && Vg(n), l.blockedOn = u, !1;
      n.shift();
    }
    return !0;
  }
  function Gf(l, n, u) {
    Mr(l) && u.delete(n);
  }
  function Jg() {
    wf = !1, Cl !== null && Mr(Cl) && (Cl = null), Il !== null && Mr(Il) && (Il = null), ia !== null && Mr(ia) && (ia = null), hi.forEach(Gf), Rn.forEach(Gf);
  }
  function Gu(l, n) {
    l.blockedOn === n && (l.blockedOn = null, wf || (wf = !0, Q.unstable_scheduleCallback(
      Q.unstable_NormalPriority,
      Jg
    )));
  }
  var Xf = null;
  function Kg(l) {
    Xf !== l && (Xf = l, Q.unstable_scheduleCallback(
      Q.unstable_NormalPriority,
      function() {
        Xf === l && (Xf = null);
        for (var n = 0; n < l.length; n += 3) {
          var u = l[n], i = l[n + 1], s = l[n + 2];
          if (typeof i != "function") {
            if (qf(i || u) === null)
              continue;
            break;
          }
          var r = Ai(u);
          r !== null && (l.splice(n, 3), n -= 3, sf(
            r,
            {
              pending: !0,
              data: s,
              method: u.method,
              action: i
            },
            i,
            s
          ));
        }
      }
    ));
  }
  function Lf(l) {
    function n(A) {
      return Gu(A, l);
    }
    Cl !== null && Gu(Cl, l), Il !== null && Gu(Il, l), ia !== null && Gu(ia, l), hi.forEach(n), Rn.forEach(n);
    for (var u = 0; u < el.length; u++) {
      var i = el[u];
      i.blockedOn === l && (i.blockedOn = null);
    }
    for (; 0 < el.length && (u = el[0], u.blockedOn === null); )
      Zg(u), u.blockedOn === null && el.shift();
    if (u = (l.ownerDocument || l).$$reactFormReplay, u != null)
      for (i = 0; i < u.length; i += 3) {
        var s = u[i], r = u[i + 1], m = s[ra] || null;
        if (typeof r == "function")
          m || Kg(u);
        else if (m) {
          var v = null;
          if (r && r.hasAttribute("formAction")) {
            if (s = r, m = r[ra] || null)
              v = m.formAction;
            else if (qf(s) !== null) continue;
          } else v = m.action;
          typeof v == "function" ? u[i + 1] = v : (u.splice(i, 3), i -= 3), Kg(u);
        }
      }
  }
  function R0() {
    function l(r) {
      r.canIntercept && r.info === "react-transition" && r.intercept({
        handler: function() {
          return new Promise(function(m) {
            return s = m;
          });
        },
        focusReset: "manual",
        scroll: "manual"
      });
    }
    function n() {
      s !== null && (s(), s = null), i || setTimeout(u, 20);
    }
    function u() {
      if (!i && !navigation.transition) {
        var r = navigation.currentEntry;
        r && r.url != null && navigation.navigate(r.url, {
          state: r.getState(),
          info: "react-transition",
          history: "replace"
        });
      }
    }
    if (typeof navigation == "object") {
      var i = !1, s = null;
      return navigation.addEventListener("navigate", l), navigation.addEventListener("navigatesuccess", n), navigation.addEventListener("navigateerror", n), setTimeout(u, 100), function() {
        i = !0, navigation.removeEventListener("navigate", l), navigation.removeEventListener("navigatesuccess", n), navigation.removeEventListener("navigateerror", n), s !== null && (s(), s = null);
      };
    }
  }
  function Qh(l) {
    this._internalRoot = l;
  }
  Vh.prototype.render = Qh.prototype.render = function(l) {
    var n = this._internalRoot;
    if (n === null) throw Error(U(409));
    var u = n.current, i = Na();
    Qg(u, i, l, n, null, null);
  }, Vh.prototype.unmount = Qh.prototype.unmount = function() {
    var l = this._internalRoot;
    if (l !== null) {
      this._internalRoot = null;
      var n = l.containerInfo;
      Qg(l.current, 2, null, l, null, null), Af(), n[Nc] = null;
    }
  };
  function Vh(l) {
    this._internalRoot = l;
  }
  Vh.prototype.unstable_scheduleHydration = function(l) {
    if (l) {
      var n = nd();
      l = { blockedOn: null, target: l, priority: n };
      for (var u = 0; u < el.length && n !== 0 && n < el[u].priority; u++) ;
      el.splice(u, 0, l), u === 0 && Zg(l);
    }
  };
  var _0 = te.version;
  if (_0 !== "19.2.4")
    throw Error(
      U(
        527,
        _0,
        "19.2.4"
      )
    );
  Z.findDOMNode = function(l) {
    var n = l._reactInternals;
    if (n === void 0)
      throw typeof l.render == "function" ? Error(U(188)) : (l = Object.keys(l).join(","), Error(U(268, l)));
    return l = W(n), l = l !== null ? Ne(l) : null, l = l === null ? null : l.stateNode, l;
  };
  var $g = {
    bundleType: 0,
    version: "19.2.4",
    rendererPackageName: "react-dom",
    currentDispatcherRef: R,
    reconcilerVersion: "19.2.4"
  };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
    var Cr = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!Cr.isDisabled && Cr.supportsFiber)
      try {
        hn = Cr.inject(
          $g
        ), zl = Cr;
      } catch {
      }
  }
  return Tp.createRoot = function(l, n) {
    if (!Re(l)) throw Error(U(299));
    var u = !1, i = "", s = th, r = My, m = lh;
    return n != null && (n.unstable_strictMode === !0 && (u = !0), n.identifierPrefix !== void 0 && (i = n.identifierPrefix), n.onUncaughtError !== void 0 && (s = n.onUncaughtError), n.onCaughtError !== void 0 && (r = n.onCaughtError), n.onRecoverableError !== void 0 && (m = n.onRecoverableError)), n = Gh(
      l,
      1,
      !1,
      null,
      null,
      u,
      i,
      null,
      s,
      r,
      m,
      R0
    ), l[Nc] = n.current, Mf(l), new Qh(n);
  }, Tp.hydrateRoot = function(l, n, u) {
    if (!Re(l)) throw Error(U(299));
    var i = !1, s = "", r = th, m = My, v = lh, A = null;
    return u != null && (u.unstable_strictMode === !0 && (i = !0), u.identifierPrefix !== void 0 && (s = u.identifierPrefix), u.onUncaughtError !== void 0 && (r = u.onUncaughtError), u.onCaughtError !== void 0 && (m = u.onCaughtError), u.onRecoverableError !== void 0 && (v = u.onRecoverableError), u.formState !== void 0 && (A = u.formState)), n = Gh(
      l,
      1,
      !0,
      n,
      u ?? null,
      i,
      s,
      A,
      r,
      m,
      v,
      R0
    ), n.context = ro(null), u = n.current, i = Na(), i = ad(i), s = sc(i), s.callback = null, Fa(u, s, i), u = i, n.current.lanes = u, xc(n, u), Bu(n), l[Nc] = n.current, Mf(l), new Vh(n);
  }, Tp.version = "19.2.4", Tp;
}
var Ap = {};
var P2;
function YT() {
  return P2 || (P2 = 1, process.env.NODE_ENV !== "production" && (function() {
    function Q(e, t) {
      for (e = e.memoizedState; e !== null && 0 < t; )
        e = e.next, t--;
      return e;
    }
    function te(e, t, a, c) {
      if (a >= t.length) return c;
      var o = t[a], f = Al(e) ? e.slice() : Ie({}, e);
      return f[o] = te(e[o], t, a + 1, c), f;
    }
    function Be(e, t, a) {
      if (t.length !== a.length)
        console.warn("copyWithRename() expects paths of the same length");
      else {
        for (var c = 0; c < a.length - 1; c++)
          if (t[c] !== a[c]) {
            console.warn(
              "copyWithRename() expects paths to be the same except for the deepest key"
            );
            return;
          }
        return U(e, t, a, 0);
      }
    }
    function U(e, t, a, c) {
      var o = t[c], f = Al(e) ? e.slice() : Ie({}, e);
      return c + 1 === t.length ? (f[a[c]] = f[o], Al(f) ? f.splice(o, 1) : delete f[o]) : f[o] = U(
        e[o],
        t,
        a,
        c + 1
      ), f;
    }
    function Re(e, t, a) {
      var c = t[a], o = Al(e) ? e.slice() : Ie({}, e);
      return a + 1 === t.length ? (Al(o) ? o.splice(c, 1) : delete o[c], o) : (o[c] = Re(e[c], t, a + 1), o);
    }
    function Se() {
      return !1;
    }
    function mt() {
      return null;
    }
    function le() {
      console.error(
        "Do not call Hooks inside useEffect(...), useMemo(...), or other built-in Hooks. You can only call Hooks at the top level of your React function. For more information, see https://react.dev/link/rules-of-hooks"
      );
    }
    function ne() {
      console.error(
        "Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo()."
      );
    }
    function W() {
    }
    function Ne() {
    }
    function w(e) {
      var t = [];
      return e.forEach(function(a) {
        t.push(a);
      }), t.sort().join(", ");
    }
    function x(e, t, a, c) {
      return new u1(e, t, a, c);
    }
    function ce(e, t) {
      e.context === Jf && (_h(e.current, 2, t, e, null, null), ln());
    }
    function Ge(e, t) {
      if (Qu !== null) {
        var a = t.staleFamilies;
        t = t.updatedFamilies, ir(), wp(
          e.current,
          t,
          a
        ), ln();
      }
    }
    function it(e) {
      Qu = e;
    }
    function ut(e) {
      return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
    }
    function Ze(e) {
      var t = e, a = e;
      if (e.alternate) for (; t.return; ) t = t.return;
      else {
        e = t;
        do
          t = e, (t.flags & 4098) !== 0 && (a = t.return), e = t.return;
        while (e);
      }
      return t.tag === 3 ? a : null;
    }
    function qt(e) {
      if (e.tag === 13) {
        var t = e.memoizedState;
        if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null) return t.dehydrated;
      }
      return null;
    }
    function Ot(e) {
      if (e.tag === 31) {
        var t = e.memoizedState;
        if (t === null && (e = e.alternate, e !== null && (t = e.memoizedState)), t !== null) return t.dehydrated;
      }
      return null;
    }
    function Ct(e) {
      if (Ze(e) !== e)
        throw Error("Unable to find node on an unmounted component.");
    }
    function wt(e) {
      var t = e.alternate;
      if (!t) {
        if (t = Ze(e), t === null)
          throw Error("Unable to find node on an unmounted component.");
        return t !== e ? null : e;
      }
      for (var a = e, c = t; ; ) {
        var o = a.return;
        if (o === null) break;
        var f = o.alternate;
        if (f === null) {
          if (c = o.return, c !== null) {
            a = c;
            continue;
          }
          break;
        }
        if (o.child === f.child) {
          for (f = o.child; f; ) {
            if (f === a) return Ct(o), e;
            if (f === c) return Ct(o), t;
            f = f.sibling;
          }
          throw Error("Unable to find node on an unmounted component.");
        }
        if (a.return !== c.return) a = o, c = f;
        else {
          for (var d = !1, h = o.child; h; ) {
            if (h === a) {
              d = !0, a = o, c = f;
              break;
            }
            if (h === c) {
              d = !0, c = o, a = f;
              break;
            }
            h = h.sibling;
          }
          if (!d) {
            for (h = f.child; h; ) {
              if (h === a) {
                d = !0, a = f, c = o;
                break;
              }
              if (h === c) {
                d = !0, c = f, a = o;
                break;
              }
              h = h.sibling;
            }
            if (!d)
              throw Error(
                "Child was not found in either parent set. This indicates a bug in React related to the return pointer. Please file an issue."
              );
          }
        }
        if (a.alternate !== c)
          throw Error(
            "Return fibers should always be each others' alternates. This error is likely caused by a bug in React. Please file an issue."
          );
      }
      if (a.tag !== 3)
        throw Error("Unable to find node on an unmounted component.");
      return a.stateNode.current === a ? e : t;
    }
    function Gt(e) {
      var t = e.tag;
      if (t === 5 || t === 26 || t === 27 || t === 6) return e;
      for (e = e.child; e !== null; ) {
        if (t = Gt(e), t !== null) return t;
        e = e.sibling;
      }
      return null;
    }
    function Ae(e) {
      return e === null || typeof e != "object" ? null : (e = Xg && e[Xg] || e["@@iterator"], typeof e == "function" ? e : null);
    }
    function Je(e) {
      if (e == null) return null;
      if (typeof e == "function")
        return e.$$typeof === Nf ? null : e.displayName || e.name || null;
      if (typeof e == "string") return e;
      switch (e) {
        case Uf:
          return "Fragment";
        case Or:
          return "Profiler";
        case za:
          return "StrictMode";
        case fo:
          return "Suspense";
        case Ha:
          return "SuspenseList";
        case eu:
          return "Activity";
      }
      if (typeof e == "object")
        switch (typeof e.tag == "number" && console.error(
          "Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."
        ), e.$$typeof) {
          case si:
            return "Portal";
          case Pn:
            return e.displayName || "Context";
          case Nh:
            return (e._context.displayName || "Context") + ".Consumer";
          case xf:
            var t = e.render;
            return e = e.displayName, e || (e = t.displayName || t.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
          case zr:
            return t = e.displayName || null, t !== null ? t : Je(e.type) || "Memo";
          case ca:
            t = e._payload, e = e._init;
            try {
              return Je(e(t));
            } catch {
            }
        }
      return null;
    }
    function Me(e) {
      return typeof e.tag == "number" ? se(e) : typeof e.name == "string" ? e.name : null;
    }
    function se(e) {
      var t = e.type;
      switch (e.tag) {
        case 31:
          return "Activity";
        case 24:
          return "Cache";
        case 9:
          return (t._context.displayName || "Context") + ".Consumer";
        case 10:
          return t.displayName || "Context";
        case 18:
          return "DehydratedFragment";
        case 11:
          return e = t.render, e = e.displayName || e.name || "", t.displayName || (e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef");
        case 7:
          return "Fragment";
        case 26:
        case 27:
        case 5:
          return t;
        case 4:
          return "Portal";
        case 3:
          return "Root";
        case 6:
          return "Text";
        case 16:
          return Je(t);
        case 8:
          return t === za ? "StrictMode" : "Mode";
        case 22:
          return "Offscreen";
        case 12:
          return "Profiler";
        case 21:
          return "Scope";
        case 13:
          return "Suspense";
        case 19:
          return "SuspenseList";
        case 25:
          return "TracingMarker";
        case 1:
        case 0:
        case 14:
        case 15:
          if (typeof t == "function")
            return t.displayName || t.name || null;
          if (typeof t == "string") return t;
          break;
        case 29:
          if (t = e._debugInfo, t != null) {
            for (var a = t.length - 1; 0 <= a; a--)
              if (typeof t[a].name == "string") return t[a].name;
          }
          if (e.return !== null)
            return se(e.return);
      }
      return null;
    }
    function Yt(e) {
      return { current: e };
    }
    function pe(e, t) {
      0 > bc ? console.error("Unexpected pop.") : (t !== S0[bc] && console.error("Unexpected Fiber popped."), e.current = v0[bc], v0[bc] = null, S0[bc] = null, bc--);
    }
    function Xe(e, t, a) {
      bc++, v0[bc] = e.current, S0[bc] = a, e.current = t;
    }
    function Kt(e) {
      return e === null && console.error(
        "Expected host context to exist. This error is likely caused by a bug in React. Please file an issue."
      ), e;
    }
    function Xt(e, t) {
      Xe(nn, t, e), Xe(Hf, e, e), Xe(ri, null, e);
      var a = t.nodeType;
      switch (a) {
        case 9:
        case 11:
          a = a === 9 ? "#document" : "#fragment", t = (t = t.documentElement) && (t = t.namespaceURI) ? mg(t) : _o;
          break;
        default:
          if (a = t.tagName, t = t.namespaceURI)
            t = mg(t), t = gc(
              t,
              a
            );
          else
            switch (a) {
              case "svg":
                t = bm;
                break;
              case "math":
                t = wv;
                break;
              default:
                t = _o;
            }
      }
      a = a.toLowerCase(), a = Cm(null, a), a = {
        context: t,
        ancestorInfo: a
      }, pe(ri, e), Xe(ri, a, e);
    }
    function R(e) {
      pe(ri, e), pe(Hf, e), pe(nn, e);
    }
    function Z() {
      return Kt(ri.current);
    }
    function ee(e) {
      e.memoizedState !== null && Xe(di, e, e);
      var t = Kt(ri.current), a = e.type, c = gc(t.context, a);
      a = Cm(t.ancestorInfo, a), c = { context: c, ancestorInfo: a }, t !== c && (Xe(Hf, e, e), Xe(ri, c, e));
    }
    function ge(e) {
      Hf.current === e && (pe(ri, e), pe(Hf, e)), di.current === e && (pe(di, e), gp._currentValue = Pr);
    }
    function De() {
    }
    function S() {
      if (jf === 0) {
        Lg = console.log, so = console.info, Bf = console.warn, b0 = console.error, Dr = console.group, Hh = console.groupCollapsed, jh = console.groupEnd;
        var e = {
          configurable: !0,
          enumerable: !0,
          value: De,
          writable: !0
        };
        Object.defineProperties(console, {
          info: e,
          log: e,
          warn: e,
          error: e,
          group: e,
          groupCollapsed: e,
          groupEnd: e
        });
      }
      jf++;
    }
    function H() {
      if (jf--, jf === 0) {
        var e = { configurable: !0, enumerable: !0, writable: !0 };
        Object.defineProperties(console, {
          log: Ie({}, e, { value: Lg }),
          info: Ie({}, e, { value: so }),
          warn: Ie({}, e, { value: Bf }),
          error: Ie({}, e, { value: b0 }),
          group: Ie({}, e, { value: Dr }),
          groupCollapsed: Ie({}, e, { value: Hh }),
          groupEnd: Ie({}, e, { value: jh })
        });
      }
      0 > jf && console.error(
        "disabledDepth fell below zero. This is a bug in React. Please file an issue."
      );
    }
    function I(e) {
      var t = Error.prepareStackTrace;
      if (Error.prepareStackTrace = void 0, e = e.stack, Error.prepareStackTrace = t, e.startsWith(`Error: react-stack-top-frame
`) && (e = e.slice(29)), t = e.indexOf(`
`), t !== -1 && (e = e.slice(t + 1)), t = e.indexOf("react_stack_bottom_frame"), t !== -1 && (t = e.lastIndexOf(
        `
`,
        t
      )), t !== -1)
        e = e.slice(0, t);
      else return "";
      return e;
    }
    function F(e) {
      if (Yf === void 0)
        try {
          throw Error();
        } catch (a) {
          var t = a.stack.trim().match(/\n( *(at )?)/);
          Yf = t && t[1] || "", E0 = -1 < a.stack.indexOf(`
    at`) ? " (<anonymous>)" : -1 < a.stack.indexOf("@") ? "@unknown:0:0" : "";
        }
      return `
` + Yf + e + E0;
    }
    function be(e, t) {
      if (!e || Bh) return "";
      var a = T0.get(e);
      if (a !== void 0) return a;
      Bh = !0, a = Error.prepareStackTrace, Error.prepareStackTrace = void 0;
      var c = null;
      c = G.H, G.H = null, S();
      try {
        var o = {
          DetermineComponentFrameRoot: function() {
            try {
              if (t) {
                var E = function() {
                  throw Error();
                };
                if (Object.defineProperty(E.prototype, "props", {
                  set: function() {
                    throw Error();
                  }
                }), typeof Reflect == "object" && Reflect.construct) {
                  try {
                    Reflect.construct(E, []);
                  } catch (ue) {
                    var Y = ue;
                  }
                  Reflect.construct(e, [], E);
                } else {
                  try {
                    E.call();
                  } catch (ue) {
                    Y = ue;
                  }
                  e.call(E.prototype);
                }
              } else {
                try {
                  throw Error();
                } catch (ue) {
                  Y = ue;
                }
                (E = e()) && typeof E.catch == "function" && E.catch(function() {
                });
              }
            } catch (ue) {
              if (ue && Y && typeof ue.stack == "string")
                return [ue.stack, Y.stack];
            }
            return [null, null];
          }
        };
        o.DetermineComponentFrameRoot.displayName = "DetermineComponentFrameRoot";
        var f = Object.getOwnPropertyDescriptor(
          o.DetermineComponentFrameRoot,
          "name"
        );
        f && f.configurable && Object.defineProperty(
          o.DetermineComponentFrameRoot,
          "name",
          { value: "DetermineComponentFrameRoot" }
        );
        var d = o.DetermineComponentFrameRoot(), h = d[0], y = d[1];
        if (h && y) {
          var p = h.split(`
`), z = y.split(`
`);
          for (d = f = 0; f < p.length && !p[f].includes(
            "DetermineComponentFrameRoot"
          ); )
            f++;
          for (; d < z.length && !z[d].includes(
            "DetermineComponentFrameRoot"
          ); )
            d++;
          if (f === p.length || d === z.length)
            for (f = p.length - 1, d = z.length - 1; 1 <= f && 0 <= d && p[f] !== z[d]; )
              d--;
          for (; 1 <= f && 0 <= d; f--, d--)
            if (p[f] !== z[d]) {
              if (f !== 1 || d !== 1)
                do
                  if (f--, d--, 0 > d || p[f] !== z[d]) {
                    var _ = `
` + p[f].replace(
                      " at new ",
                      " at "
                    );
                    return e.displayName && _.includes("<anonymous>") && (_ = _.replace("<anonymous>", e.displayName)), typeof e == "function" && T0.set(e, _), _;
                  }
                while (1 <= f && 0 <= d);
              break;
            }
        }
      } finally {
        Bh = !1, G.H = c, H(), Error.prepareStackTrace = a;
      }
      return p = (p = e ? e.displayName || e.name : "") ? F(p) : "", typeof e == "function" && T0.set(e, p), p;
    }
    function Le(e, t) {
      switch (e.tag) {
        case 26:
        case 27:
        case 5:
          return F(e.type);
        case 16:
          return F("Lazy");
        case 13:
          return e.child !== t && t !== null ? F("Suspense Fallback") : F("Suspense");
        case 19:
          return F("SuspenseList");
        case 0:
        case 15:
          return be(e.type, !1);
        case 11:
          return be(e.type.render, !1);
        case 1:
          return be(e.type, !0);
        case 31:
          return F("Activity");
        default:
          return "";
      }
    }
    function Oe(e) {
      try {
        var t = "", a = null;
        do {
          t += Le(e, a);
          var c = e._debugInfo;
          if (c)
            for (var o = c.length - 1; 0 <= o; o--) {
              var f = c[o];
              if (typeof f.name == "string") {
                var d = t;
                e: {
                  var h = f.name, y = f.env, p = f.debugLocation;
                  if (p != null) {
                    var z = I(p), _ = z.lastIndexOf(`
`), E = _ === -1 ? z : z.slice(_ + 1);
                    if (E.indexOf(h) !== -1) {
                      var Y = `
` + E;
                      break e;
                    }
                  }
                  Y = F(
                    h + (y ? " [" + y + "]" : "")
                  );
                }
                t = d + Y;
              }
            }
          a = e, e = e.return;
        } while (e);
        return t;
      } catch (ue) {
        return `
Error generating stack: ` + ue.message + `
` + ue.stack;
      }
    }
    function $t(e) {
      return (e = e ? e.displayName || e.name : "") ? F(e) : "";
    }
    function gt() {
      if (ja === null) return null;
      var e = ja._debugOwner;
      return e != null ? Me(e) : null;
    }
    function wa() {
      if (ja === null) return "";
      var e = ja;
      try {
        var t = "";
        switch (e.tag === 6 && (e = e.return), e.tag) {
          case 26:
          case 27:
          case 5:
            t += F(e.type);
            break;
          case 13:
            t += F("Suspense");
            break;
          case 19:
            t += F("SuspenseList");
            break;
          case 31:
            t += F("Activity");
            break;
          case 30:
          case 0:
          case 15:
          case 1:
            e._debugOwner || t !== "" || (t += $t(
              e.type
            ));
            break;
          case 11:
            e._debugOwner || t !== "" || (t += $t(
              e.type.render
            ));
        }
        for (; e; )
          if (typeof e.tag == "number") {
            var a = e;
            e = a._debugOwner;
            var c = a._debugStack;
            if (e && c) {
              var o = I(c);
              o !== "" && (t += `
` + o);
            }
          } else if (e.debugStack != null) {
            var f = e.debugStack;
            (e = e.owner) && f && (t += `
` + I(f));
          } else break;
        var d = t;
      } catch (h) {
        d = `
Error generating stack: ` + h.message + `
` + h.stack;
      }
      return d;
    }
    function oe(e, t, a, c, o, f, d) {
      var h = ja;
      _c(e);
      try {
        return e !== null && e._debugTask ? e._debugTask.run(
          t.bind(null, a, c, o, f, d)
        ) : t(a, c, o, f, d);
      } finally {
        _c(h);
      }
      throw Error(
        "runWithFiberInDEV should never be called in production. This is a bug in React."
      );
    }
    function _c(e) {
      G.getCurrentStack = e === null ? null : wa, Yu = !1, ja = e;
    }
    function Mc(e) {
      return typeof Symbol == "function" && Symbol.toStringTag && e[Symbol.toStringTag] || e.constructor.name || "Object";
    }
    function Ga(e) {
      try {
        return iu(e), !1;
      } catch {
        return !0;
      }
    }
    function iu(e) {
      return "" + e;
    }
    function vt(e, t) {
      if (Ga(e))
        return console.error(
          "The provided `%s` attribute is an unsupported type %s. This value must be coerced to a string before using it here.",
          t,
          Mc(e)
        ), iu(e);
    }
    function ta(e, t) {
      if (Ga(e))
        return console.error(
          "The provided `%s` CSS property is an unsupported type %s. This value must be coerced to a string before using it here.",
          t,
          Mc(e)
        ), iu(e);
    }
    function Si(e) {
      if (Ga(e))
        return console.error(
          "Form field values (value, checked, defaultValue, or defaultChecked props) must be strings, not %s. This value must be coerced to a string before using it here.",
          Mc(e)
        ), iu(e);
    }
    function hs(e) {
      if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u") return !1;
      var t = __REACT_DEVTOOLS_GLOBAL_HOOK__;
      if (t.isDisabled) return !0;
      if (!t.supportsFiber)
        return console.error(
          "The installed version of React DevTools is too old and will not work with the current version of React. Please update React DevTools. https://react.dev/link/react-devtools"
        ), !0;
      try {
        ho = t.inject(e), Ml = t;
      } catch (a) {
        console.error("React instrumentation encountered an error: %o.", a);
      }
      return !!t.checkDCE;
    }
    function de(e) {
      if (typeof z0 == "function" && Vg(e), Ml && typeof Ml.setStrictMode == "function")
        try {
          Ml.setStrictMode(ho, e);
        } catch (t) {
          qu || (qu = !0, console.error(
            "React instrumentation encountered an error: %o",
            t
          ));
        }
    }
    function Cc(e) {
      return e >>>= 0, e === 0 ? 32 : 31 - (D0(e) / Lh | 0) | 0;
    }
    function ou(e) {
      var t = e & 42;
      if (t !== 0) return t;
      switch (e & -e) {
        case 1:
          return 1;
        case 2:
          return 2;
        case 4:
          return 4;
        case 8:
          return 8;
        case 16:
          return 16;
        case 32:
          return 32;
        case 64:
          return 64;
        case 128:
          return 128;
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
          return e & 261888;
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
          return e & 3932160;
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
          return e & 62914560;
        case 67108864:
          return 67108864;
        case 134217728:
          return 134217728;
        case 268435456:
          return 268435456;
        case 536870912:
          return 536870912;
        case 1073741824:
          return 0;
        default:
          return console.error(
            "Should have found matching lanes. This is a bug in React."
          ), e;
      }
    }
    function bi(e, t, a) {
      var c = e.pendingLanes;
      if (c === 0) return 0;
      var o = 0, f = e.suspendedLanes, d = e.pingedLanes;
      e = e.warmLanes;
      var h = c & 134217727;
      return h !== 0 ? (c = h & ~f, c !== 0 ? o = ou(c) : (d &= h, d !== 0 ? o = ou(d) : a || (a = h & ~e, a !== 0 && (o = ou(a))))) : (h = c & ~f, h !== 0 ? o = ou(h) : d !== 0 ? o = ou(d) : a || (a = c & ~e, a !== 0 && (o = ou(a)))), o === 0 ? 0 : t !== 0 && t !== o && (t & f) === 0 && (f = o & -o, a = t & -t, f >= a || f === 32 && (a & 4194048) !== 0) ? t : o;
    }
    function bl(e, t) {
      return (e.pendingLanes & ~(e.suspendedLanes & ~e.pingedLanes) & t) === 0;
    }
    function td(e, t) {
      switch (e) {
        case 1:
        case 2:
        case 4:
        case 8:
        case 64:
          return t + 250;
        case 16:
        case 32:
        case 128:
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
          return t + 5e3;
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
          return -1;
        case 67108864:
        case 134217728:
        case 268435456:
        case 536870912:
        case 1073741824:
          return -1;
        default:
          return console.error(
            "Should have found matching lanes. This is a bug in React."
          ), -1;
      }
    }
    function Uo() {
      var e = wf;
      return wf <<= 1, (wf & 62914560) === 0 && (wf = 4194304), e;
    }
    function xo(e) {
      for (var t = [], a = 0; 31 > a; a++) t.push(e);
      return t;
    }
    function Un(e, t) {
      e.pendingLanes |= t, t !== 268435456 && (e.suspendedLanes = 0, e.pingedLanes = 0, e.warmLanes = 0);
    }
    function ld(e, t, a, c, o, f) {
      var d = e.pendingLanes;
      e.pendingLanes = a, e.suspendedLanes = 0, e.pingedLanes = 0, e.warmLanes = 0, e.expiredLanes &= a, e.entangledLanes &= a, e.errorRecoveryDisabledLanes &= a, e.shellSuspendCounter = 0;
      var h = e.entanglements, y = e.expirationTimes, p = e.hiddenUpdates;
      for (a = d & ~a; 0 < a; ) {
        var z = 31 - Fl(a), _ = 1 << z;
        h[z] = 0, y[z] = -1;
        var E = p[z];
        if (E !== null)
          for (p[z] = null, z = 0; z < E.length; z++) {
            var Y = E[z];
            Y !== null && (Y.lane &= -536870913);
          }
        a &= ~_;
      }
      c !== 0 && No(e, c, 0), f !== 0 && o === 0 && e.tag !== 0 && (e.suspendedLanes |= f & ~(d & ~t));
    }
    function No(e, t, a) {
      e.pendingLanes |= t, e.suspendedLanes &= ~t;
      var c = 31 - Fl(t);
      e.entangledLanes |= t, e.entanglements[c] = e.entanglements[c] | 1073741824 | a & 261930;
    }
    function ms(e, t) {
      var a = e.entangledLanes |= t;
      for (e = e.entanglements; a; ) {
        var c = 31 - Fl(a), o = 1 << c;
        o & t | e[c] & t && (e[c] |= t), a &= ~o;
      }
    }
    function Ei(e, t) {
      var a = t & -t;
      return a = (a & 42) !== 0 ? 1 : hn(a), (a & (e.suspendedLanes | t)) !== 0 ? 0 : a;
    }
    function hn(e) {
      switch (e) {
        case 2:
          e = 1;
          break;
        case 8:
          e = 4;
          break;
        case 32:
          e = 16;
          break;
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
          e = 128;
          break;
        case 268435456:
          e = 134217728;
          break;
        default:
          e = 0;
      }
      return e;
    }
    function zl(e, t, a) {
      if (wu)
        for (e = e.pendingUpdatersLaneMap; 0 < a; ) {
          var c = 31 - Fl(a), o = 1 << c;
          e[c].add(t), a &= ~o;
        }
    }
    function Xa(e, t) {
      if (wu)
        for (var a = e.pendingUpdatersLaneMap, c = e.memoizedUpdaters; 0 < t; ) {
          var o = 31 - Fl(t);
          e = 1 << o, o = a[o], 0 < o.size && (o.forEach(function(f) {
            var d = f.alternate;
            d !== null && c.has(d) || c.add(f);
          }), o.clear()), t &= ~e;
        }
    }
    function Nl(e) {
      return e &= -e, Cl < e ? Il < e ? (e & 134217727) !== 0 ? ia : hi : Il : Cl;
    }
    function Uc() {
      var e = At.p;
      return e !== 0 ? e : (e = window.event, e === void 0 ? ia : Ch(e.type));
    }
    function g(e, t) {
      var a = At.p;
      try {
        return At.p = e, t();
      } finally {
        At.p = a;
      }
    }
    function M(e) {
      delete e[el], delete e[Da], delete e[mo], delete e[h1], delete e[Zg];
    }
    function P(e) {
      var t = e[el];
      if (t) return t;
      for (var a = e.parentNode; a; ) {
        if (t = a[Ec] || a[el]) {
          if (a = t.alternate, t.child !== null || a !== null && a.child !== null)
            for (e = uo(e); e !== null; ) {
              if (a = e[el])
                return a;
              e = uo(e);
            }
          return t;
        }
        e = a, a = e.parentNode;
      }
      return null;
    }
    function ae(e) {
      if (e = e[el] || e[Ec]) {
        var t = e.tag;
        if (t === 5 || t === 6 || t === 13 || t === 31 || t === 26 || t === 27 || t === 3)
          return e;
      }
      return null;
    }
    function he(e) {
      var t = e.tag;
      if (t === 5 || t === 26 || t === 27 || t === 6)
        return e.stateNode;
      throw Error("getNodeFromInstance: Invalid argument.");
    }
    function Ce(e) {
      var t = e[Mr];
      return t || (t = e[Mr] = { hoistableStyles: /* @__PURE__ */ new Map(), hoistableScripts: /* @__PURE__ */ new Map() }), t;
    }
    function me(e) {
      e[Gf] = !0;
    }
    function lt(e, t) {
      Qe(e, t), Qe(e + "Capture", t);
    }
    function Qe(e, t) {
      Gu[e] && console.error(
        "EventRegistry: More than one plugin attempted to publish the same registration name, `%s`.",
        e
      ), Gu[e] = t;
      var a = e.toLowerCase();
      for (Xf[a] = e, e === "onDoubleClick" && (Xf.ondblclick = e), e = 0; e < t.length; e++)
        Jg.add(t[e]);
    }
    function la(e, t) {
      Kg[t.type] || t.onChange || t.onInput || t.readOnly || t.disabled || t.value == null || console.error(
        e === "select" ? "You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set `onChange`." : "You provided a `value` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultValue`. Otherwise, set either `onChange` or `readOnly`."
      ), t.onChange || t.readOnly || t.disabled || t.checked == null || console.error(
        "You provided a `checked` prop to a form field without an `onChange` handler. This will render a read-only field. If the field should be mutable use `defaultChecked`. Otherwise, set either `onChange` or `readOnly`."
      );
    }
    function mn(e) {
      return un.call(Qh, e) ? !0 : un.call(R0, e) ? !1 : Lf.test(e) ? Qh[e] = !0 : (R0[e] = !0, console.error("Invalid attribute name: `%s`", e), !1);
    }
    function xc(e, t, a) {
      if (mn(t)) {
        if (!e.hasAttribute(t)) {
          switch (typeof a) {
            case "symbol":
            case "object":
              return a;
            case "function":
              return a;
            case "boolean":
              if (a === !1) return a;
          }
          return a === void 0 ? void 0 : null;
        }
        return e = e.getAttribute(t), e === "" && a === !0 ? !0 : (vt(a, t), e === "" + a ? a : e);
      }
    }
    function Ho(e, t, a) {
      if (mn(t))
        if (a === null) e.removeAttribute(t);
        else {
          switch (typeof a) {
            case "undefined":
            case "function":
            case "symbol":
              e.removeAttribute(t);
              return;
            case "boolean":
              var c = t.toLowerCase().slice(0, 5);
              if (c !== "data-" && c !== "aria-") {
                e.removeAttribute(t);
                return;
              }
          }
          vt(a, t), e.setAttribute(t, "" + a);
        }
    }
    function ys(e, t, a) {
      if (a === null) e.removeAttribute(t);
      else {
        switch (typeof a) {
          case "undefined":
          case "function":
          case "symbol":
          case "boolean":
            e.removeAttribute(t);
            return;
        }
        vt(a, t), e.setAttribute(t, "" + a);
      }
    }
    function fu(e, t, a, c) {
      if (c === null) e.removeAttribute(a);
      else {
        switch (typeof c) {
          case "undefined":
          case "function":
          case "symbol":
          case "boolean":
            e.removeAttribute(a);
            return;
        }
        vt(c, a), e.setAttributeNS(t, a, "" + c);
      }
    }
    function La(e) {
      switch (typeof e) {
        case "bigint":
        case "boolean":
        case "number":
        case "string":
        case "undefined":
          return e;
        case "object":
          return Si(e), e;
        default:
          return "";
      }
    }
    function ad(e) {
      var t = e.type;
      return (e = e.nodeName) && e.toLowerCase() === "input" && (t === "checkbox" || t === "radio");
    }
    function zm(e, t, a) {
      var c = Object.getOwnPropertyDescriptor(
        e.constructor.prototype,
        t
      );
      if (!e.hasOwnProperty(t) && typeof c < "u" && typeof c.get == "function" && typeof c.set == "function") {
        var o = c.get, f = c.set;
        return Object.defineProperty(e, t, {
          configurable: !0,
          get: function() {
            return o.call(this);
          },
          set: function(d) {
            Si(d), a = "" + d, f.call(this, d);
          }
        }), Object.defineProperty(e, t, {
          enumerable: c.enumerable
        }), {
          getValue: function() {
            return a;
          },
          setValue: function(d) {
            Si(d), a = "" + d;
          },
          stopTracking: function() {
            e._valueTracker = null, delete e[t];
          }
        };
      }
    }
    function nd(e) {
      if (!e._valueTracker) {
        var t = ad(e) ? "checked" : "value";
        e._valueTracker = zm(
          e,
          t,
          "" + e[t]
        );
      }
    }
    function Dm(e) {
      if (!e) return !1;
      var t = e._valueTracker;
      if (!t) return !0;
      var a = t.getValue(), c = "";
      return e && (c = ad(e) ? e.checked ? "true" : "false" : e.value), e = c, e !== a ? (t.setValue(e), !0) : !1;
    }
    function xn(e) {
      if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u") return null;
      try {
        return e.activeElement || e.body;
      } catch {
        return e.body;
      }
    }
    function Ut(e) {
      return e.replace(
        Vh,
        function(t) {
          return "\\" + t.charCodeAt(0).toString(16) + " ";
        }
      );
    }
    function ra(e, t) {
      t.checked === void 0 || t.defaultChecked === void 0 || $g || (console.error(
        "%s contains an input of type %s with both checked and defaultChecked props. Input elements must be either controlled or uncontrolled (specify either the checked prop, or the defaultChecked prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://react.dev/link/controlled-components",
        gt() || "A component",
        t.type
      ), $g = !0), t.value === void 0 || t.defaultValue === void 0 || _0 || (console.error(
        "%s contains an input of type %s with both value and defaultValue props. Input elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled input element and remove one of these props. More info: https://react.dev/link/controlled-components",
        gt() || "A component",
        t.type
      ), _0 = !0);
    }
    function Nc(e, t, a, c, o, f, d, h) {
      e.name = "", d != null && typeof d != "function" && typeof d != "symbol" && typeof d != "boolean" ? (vt(d, "type"), e.type = d) : e.removeAttribute("type"), t != null ? d === "number" ? (t === 0 && e.value === "" || e.value != t) && (e.value = "" + La(t)) : e.value !== "" + La(t) && (e.value = "" + La(t)) : d !== "submit" && d !== "reset" || e.removeAttribute("value"), t != null ? Rm(e, d, La(t)) : a != null ? Rm(e, d, La(a)) : c != null && e.removeAttribute("value"), o == null && f != null && (e.defaultChecked = !!f), o != null && (e.checked = o && typeof o != "function" && typeof o != "symbol"), h != null && typeof h != "function" && typeof h != "symbol" && typeof h != "boolean" ? (vt(h, "name"), e.name = "" + La(h)) : e.removeAttribute("name");
    }
    function ud(e, t, a, c, o, f, d, h) {
      if (f != null && typeof f != "function" && typeof f != "symbol" && typeof f != "boolean" && (vt(f, "type"), e.type = f), t != null || a != null) {
        if (!(f !== "submit" && f !== "reset" || t != null)) {
          nd(e);
          return;
        }
        a = a != null ? "" + La(a) : "", t = t != null ? "" + La(t) : a, h || t === e.value || (e.value = t), e.defaultValue = t;
      }
      c = c ?? o, c = typeof c != "function" && typeof c != "symbol" && !!c, e.checked = h ? e.checked : !!c, e.defaultChecked = !!c, d != null && typeof d != "function" && typeof d != "symbol" && typeof d != "boolean" && (vt(d, "name"), e.name = d), nd(e);
    }
    function Rm(e, t, a) {
      t === "number" && xn(e.ownerDocument) === e || e.defaultValue === "" + a || (e.defaultValue = "" + a);
    }
    function zp(e, t) {
      t.value == null && (typeof t.children == "object" && t.children !== null ? Ar.Children.forEach(t.children, function(a) {
        a == null || typeof a == "string" || typeof a == "number" || typeof a == "bigint" || l || (l = !0, console.error(
          "Cannot infer the option value of complex children. Pass a `value` prop or use a plain string as children to <option>."
        ));
      }) : t.dangerouslySetInnerHTML == null || n || (n = !0, console.error(
        "Pass a `value` prop if you set dangerouslyInnerHTML so React knows which value should be selected."
      ))), t.selected == null || Cr || (console.error(
        "Use the `defaultValue` or `value` props on <select> instead of setting `selected` on <option>."
      ), Cr = !0);
    }
    function _m() {
      var e = gt();
      return e ? `

Check the render method of \`` + e + "`." : "";
    }
    function su(e, t, a, c) {
      if (e = e.options, t) {
        t = {};
        for (var o = 0; o < a.length; o++)
          t["$" + a[o]] = !0;
        for (a = 0; a < e.length; a++)
          o = t.hasOwnProperty("$" + e[a].value), e[a].selected !== o && (e[a].selected = o), o && c && (e[a].defaultSelected = !0);
      } else {
        for (a = "" + La(a), t = null, o = 0; o < e.length; o++) {
          if (e[o].value === a) {
            e[o].selected = !0, c && (e[o].defaultSelected = !0);
            return;
          }
          t !== null || e[o].disabled || (t = e[o]);
        }
        t !== null && (t.selected = !0);
      }
    }
    function cd(e, t) {
      for (e = 0; e < i.length; e++) {
        var a = i[e];
        if (t[a] != null) {
          var c = Al(t[a]);
          t.multiple && !c ? console.error(
            "The `%s` prop supplied to <select> must be an array if `multiple` is true.%s",
            a,
            _m()
          ) : !t.multiple && c && console.error(
            "The `%s` prop supplied to <select> must be a scalar value if `multiple` is false.%s",
            a,
            _m()
          );
        }
      }
      t.value === void 0 || t.defaultValue === void 0 || u || (console.error(
        "Select elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled select element and remove one of these props. More info: https://react.dev/link/controlled-components"
      ), u = !0);
    }
    function Ti(e, t) {
      t.value === void 0 || t.defaultValue === void 0 || s || (console.error(
        "%s contains a textarea with both value and defaultValue props. Textarea elements must be either controlled or uncontrolled (specify either the value prop, or the defaultValue prop, but not both). Decide between using a controlled or uncontrolled textarea and remove one of these props. More info: https://react.dev/link/controlled-components",
        gt() || "A component"
      ), s = !0), t.children != null && t.value == null && console.error(
        "Use the `defaultValue` or `value` props instead of setting children on <textarea>."
      );
    }
    function Ai(e, t, a) {
      if (t != null && (t = "" + La(t), t !== e.value && (e.value = t), a == null)) {
        e.defaultValue !== t && (e.defaultValue = t);
        return;
      }
      e.defaultValue = a != null ? "" + La(a) : "";
    }
    function jo(e, t, a, c) {
      if (t == null) {
        if (c != null) {
          if (a != null)
            throw Error(
              "If you supply `defaultValue` on a <textarea>, do not pass children."
            );
          if (Al(c)) {
            if (1 < c.length)
              throw Error("<textarea> can only have at most one child.");
            c = c[0];
          }
          a = c;
        }
        a == null && (a = ""), t = a;
      }
      a = La(t), e.defaultValue = a, c = e.textContent, c === a && c !== "" && c !== null && (e.value = c), nd(e);
    }
    function Oi(e, t) {
      return e.serverProps === void 0 && e.serverTail.length === 0 && e.children.length === 1 && 3 < e.distanceFromLeaf && e.distanceFromLeaf > 15 - t ? Oi(e.children[0], t) : e;
    }
    function zt(e) {
      return "  " + "  ".repeat(e);
    }
    function zi(e) {
      return "+ " + "  ".repeat(e);
    }
    function Hc(e) {
      return "- " + "  ".repeat(e);
    }
    function jc(e) {
      switch (e.tag) {
        case 26:
        case 27:
        case 5:
          return e.type;
        case 16:
          return "Lazy";
        case 31:
          return "Activity";
        case 13:
          return "Suspense";
        case 19:
          return "SuspenseList";
        case 0:
        case 15:
          return e = e.type, e.displayName || e.name || null;
        case 11:
          return e = e.type.render, e.displayName || e.name || null;
        case 1:
          return e = e.type, e.displayName || e.name || null;
        default:
          return null;
      }
    }
    function ru(e, t) {
      return r.test(e) ? (e = JSON.stringify(e), e.length > t - 2 ? 8 > t ? '{"..."}' : "{" + e.slice(0, t - 7) + '..."}' : "{" + e + "}") : e.length > t ? 5 > t ? '{"..."}' : e.slice(0, t - 3) + "..." : e;
    }
    function id(e, t, a) {
      var c = 120 - 2 * a;
      if (t === null)
        return zi(a) + ru(e, c) + `
`;
      if (typeof t == "string") {
        for (var o = 0; o < t.length && o < e.length && t.charCodeAt(o) === e.charCodeAt(o); o++) ;
        return o > c - 8 && 10 < o && (e = "..." + e.slice(o - 8), t = "..." + t.slice(o - 8)), zi(a) + ru(e, c) + `
` + Hc(a) + ru(t, c) + `
`;
      }
      return zt(a) + ru(e, c) + `
`;
    }
    function od(e) {
      return Object.prototype.toString.call(e).replace(/^\[object (.*)\]$/, function(t, a) {
        return a;
      });
    }
    function Bo(e, t) {
      switch (typeof e) {
        case "string":
          return e = JSON.stringify(e), e.length > t ? 5 > t ? '"..."' : e.slice(0, t - 4) + '..."' : e;
        case "object":
          if (e === null) return "null";
          if (Al(e)) return "[...]";
          if (e.$$typeof === Dn)
            return (t = Je(e.type)) ? "<" + t + ">" : "<...>";
          var a = od(e);
          if (a === "Object") {
            a = "", t -= 2;
            for (var c in e)
              if (e.hasOwnProperty(c)) {
                var o = JSON.stringify(c);
                if (o !== '"' + c + '"' && (c = o), t -= c.length - 2, o = Bo(
                  e[c],
                  15 > t ? t : 15
                ), t -= o.length, 0 > t) {
                  a += a === "" ? "..." : ", ...";
                  break;
                }
                a += (a === "" ? "" : ",") + c + ":" + o;
              }
            return "{" + a + "}";
          }
          return a;
        case "function":
          return (t = e.displayName || e.name) ? "function " + t : "function";
        default:
          return String(e);
      }
    }
    function Yo(e, t) {
      return typeof e != "string" || r.test(e) ? "{" + Bo(e, t - 2) + "}" : e.length > t - 2 ? 5 > t ? '"..."' : '"' + e.slice(0, t - 5) + '..."' : '"' + e + '"';
    }
    function qo(e, t, a) {
      var c = 120 - a.length - e.length, o = [], f;
      for (f in t)
        if (t.hasOwnProperty(f) && f !== "children") {
          var d = Yo(
            t[f],
            120 - a.length - f.length - 1
          );
          c -= f.length + d.length + 2, o.push(f + "=" + d);
        }
      return o.length === 0 ? a + "<" + e + `>
` : 0 < c ? a + "<" + e + " " + o.join(" ") + `>
` : a + "<" + e + `
` + a + "  " + o.join(`
` + a + "  ") + `
` + a + `>
`;
    }
    function fd(e, t, a) {
      var c = "", o = Ie({}, t), f;
      for (f in e)
        if (e.hasOwnProperty(f)) {
          delete o[f];
          var d = 120 - 2 * a - f.length - 2, h = Bo(e[f], d);
          t.hasOwnProperty(f) ? (d = Bo(t[f], d), c += zi(a) + f + ": " + h + `
`, c += Hc(a) + f + ": " + d + `
`) : c += zi(a) + f + ": " + h + `
`;
        }
      for (var y in o)
        o.hasOwnProperty(y) && (e = Bo(
          o[y],
          120 - 2 * a - y.length - 2
        ), c += Hc(a) + y + ": " + e + `
`);
      return c;
    }
    function Pu(e, t, a, c) {
      var o = "", f = /* @__PURE__ */ new Map();
      for (p in a)
        a.hasOwnProperty(p) && f.set(
          p.toLowerCase(),
          p
        );
      if (f.size === 1 && f.has("children"))
        o += qo(
          e,
          t,
          zt(c)
        );
      else {
        for (var d in t)
          if (t.hasOwnProperty(d) && d !== "children") {
            var h = 120 - 2 * (c + 1) - d.length - 1, y = f.get(d.toLowerCase());
            if (y !== void 0) {
              f.delete(d.toLowerCase());
              var p = t[d];
              y = a[y];
              var z = Yo(
                p,
                h
              );
              h = Yo(
                y,
                h
              ), typeof p == "object" && p !== null && typeof y == "object" && y !== null && od(p) === "Object" && od(y) === "Object" && (2 < Object.keys(p).length || 2 < Object.keys(y).length || -1 < z.indexOf("...") || -1 < h.indexOf("...")) ? o += zt(c + 1) + d + `={{
` + fd(
                p,
                y,
                c + 2
              ) + zt(c + 1) + `}}
` : (o += zi(c + 1) + d + "=" + z + `
`, o += Hc(c + 1) + d + "=" + h + `
`);
            } else
              o += zt(c + 1) + d + "=" + Yo(t[d], h) + `
`;
          }
        f.forEach(function(_) {
          if (_ !== "children") {
            var E = 120 - 2 * (c + 1) - _.length - 1;
            o += Hc(c + 1) + _ + "=" + Yo(a[_], E) + `
`;
          }
        }), o = o === "" ? zt(c) + "<" + e + `>
` : zt(c) + "<" + e + `
` + o + zt(c) + `>
`;
      }
      return e = a.children, t = t.children, typeof e == "string" || typeof e == "number" || typeof e == "bigint" ? (f = "", (typeof t == "string" || typeof t == "number" || typeof t == "bigint") && (f = "" + t), o += id(f, "" + e, c + 1)) : (typeof t == "string" || typeof t == "number" || typeof t == "bigint") && (o = e == null ? o + id("" + t, null, c + 1) : o + id("" + t, void 0, c + 1)), o;
    }
    function Qa(e, t) {
      var a = jc(e);
      if (a === null) {
        for (a = "", e = e.child; e; )
          a += Qa(e, t), e = e.sibling;
        return a;
      }
      return zt(t) + "<" + a + `>
`;
    }
    function sd(e, t) {
      var a = Oi(e, t);
      if (a !== e && (e.children.length !== 1 || e.children[0] !== a))
        return zt(t) + `...
` + sd(a, t + 1);
      a = "";
      var c = e.fiber._debugInfo;
      if (c)
        for (var o = 0; o < c.length; o++) {
          var f = c[o].name;
          typeof f == "string" && (a += zt(t) + "<" + f + `>
`, t++);
        }
      if (c = "", o = e.fiber.pendingProps, e.fiber.tag === 6)
        c = id(o, e.serverProps, t), t++;
      else if (f = jc(e.fiber), f !== null)
        if (e.serverProps === void 0) {
          c = t;
          var d = 120 - 2 * c - f.length - 2, h = "";
          for (p in o)
            if (o.hasOwnProperty(p) && p !== "children") {
              var y = Yo(o[p], 15);
              if (d -= p.length + y.length + 2, 0 > d) {
                h += " ...";
                break;
              }
              h += " " + p + "=" + y;
            }
          c = zt(c) + "<" + f + h + `>
`, t++;
        } else
          e.serverProps === null ? (c = qo(
            f,
            o,
            zi(t)
          ), t++) : typeof e.serverProps == "string" ? console.error(
            "Should not have matched a non HostText fiber to a Text node. This is a bug in React."
          ) : (c = Pu(
            f,
            o,
            e.serverProps,
            t
          ), t++);
      var p = "";
      for (o = e.fiber.child, f = 0; o && f < e.children.length; )
        d = e.children[f], d.fiber === o ? (p += sd(d, t), f++) : p += Qa(o, t), o = o.sibling;
      for (o && 0 < e.children.length && (p += zt(t) + `...
`), o = e.serverTail, e.serverProps === null && t--, e = 0; e < o.length; e++)
        f = o[e], p = typeof f == "string" ? p + (Hc(t) + ru(f, 120 - 2 * t) + `
`) : p + qo(
          f.type,
          f.props,
          Hc(t)
        );
      return a + c + p;
    }
    function Mm(e) {
      try {
        return `

` + sd(e, 0);
      } catch {
        return "";
      }
    }
    function rd(e, t, a) {
      for (var c = t, o = null, f = 0; c; )
        c === e && (f = 0), o = {
          fiber: c,
          children: o !== null ? [o] : [],
          serverProps: c === t ? a : c === e ? null : void 0,
          serverTail: [],
          distanceFromLeaf: f
        }, f++, c = c.return;
      return o !== null ? Mm(o).replaceAll(/^[+-]/gm, ">") : "";
    }
    function Cm(e, t) {
      var a = Ie({}, e || V), c = { tag: t };
      return v.indexOf(t) !== -1 && (a.aTagInScope = null, a.buttonTagInScope = null, a.nobrTagInScope = null), A.indexOf(t) !== -1 && (a.pTagInButtonScope = null), m.indexOf(t) !== -1 && t !== "address" && t !== "div" && t !== "p" && (a.listItemTagAutoclosing = null, a.dlItemTagAutoclosing = null), a.current = c, t === "form" && (a.formTag = c), t === "a" && (a.aTagInScope = c), t === "button" && (a.buttonTagInScope = c), t === "nobr" && (a.nobrTagInScope = c), t === "p" && (a.pTagInButtonScope = c), t === "li" && (a.listItemTagAutoclosing = c), (t === "dd" || t === "dt") && (a.dlItemTagAutoclosing = c), t === "#document" || t === "html" ? a.containerTagInScope = null : a.containerTagInScope || (a.containerTagInScope = c), e !== null || t !== "#document" && t !== "html" && t !== "body" ? a.implicitRootScope === !0 && (a.implicitRootScope = !1) : a.implicitRootScope = !0, a;
    }
    function ps(e, t, a) {
      switch (t) {
        case "select":
          return e === "hr" || e === "option" || e === "optgroup" || e === "script" || e === "template" || e === "#text";
        case "optgroup":
          return e === "option" || e === "#text";
        case "option":
          return e === "#text";
        case "tr":
          return e === "th" || e === "td" || e === "style" || e === "script" || e === "template";
        case "tbody":
        case "thead":
        case "tfoot":
          return e === "tr" || e === "style" || e === "script" || e === "template";
        case "colgroup":
          return e === "col" || e === "template";
        case "table":
          return e === "caption" || e === "colgroup" || e === "tbody" || e === "tfoot" || e === "thead" || e === "style" || e === "script" || e === "template";
        case "head":
          return e === "base" || e === "basefont" || e === "bgsound" || e === "link" || e === "meta" || e === "title" || e === "noscript" || e === "noframes" || e === "style" || e === "script" || e === "template";
        case "html":
          if (a) break;
          return e === "head" || e === "body" || e === "frameset";
        case "frameset":
          return e === "frame";
        case "#document":
          if (!a) return e === "html";
      }
      switch (e) {
        case "h1":
        case "h2":
        case "h3":
        case "h4":
        case "h5":
        case "h6":
          return t !== "h1" && t !== "h2" && t !== "h3" && t !== "h4" && t !== "h5" && t !== "h6";
        case "rp":
        case "rt":
          return j.indexOf(t) === -1;
        case "caption":
        case "col":
        case "colgroup":
        case "frameset":
        case "frame":
        case "tbody":
        case "td":
        case "tfoot":
        case "th":
        case "thead":
        case "tr":
          return t == null;
        case "head":
          return a || t === null;
        case "html":
          return a && t === "#document" || t === null;
        case "body":
          return a && (t === "#document" || t === "html") || t === null;
      }
      return !0;
    }
    function Pv(e, t) {
      switch (e) {
        case "address":
        case "article":
        case "aside":
        case "blockquote":
        case "center":
        case "details":
        case "dialog":
        case "dir":
        case "div":
        case "dl":
        case "fieldset":
        case "figcaption":
        case "figure":
        case "footer":
        case "header":
        case "hgroup":
        case "main":
        case "menu":
        case "nav":
        case "ol":
        case "p":
        case "section":
        case "summary":
        case "ul":
        case "pre":
        case "listing":
        case "table":
        case "hr":
        case "xmp":
        case "h1":
        case "h2":
        case "h3":
        case "h4":
        case "h5":
        case "h6":
          return t.pTagInButtonScope;
        case "form":
          return t.formTag || t.pTagInButtonScope;
        case "li":
          return t.listItemTagAutoclosing;
        case "dd":
        case "dt":
          return t.dlItemTagAutoclosing;
        case "button":
          return t.buttonTagInScope;
        case "a":
          return t.aTagInScope;
        case "nobr":
          return t.nobrTagInScope;
      }
      return null;
    }
    function Va(e, t) {
      for (; e; ) {
        switch (e.tag) {
          case 5:
          case 26:
          case 27:
            if (e.type === t) return e;
        }
        e = e.return;
      }
      return null;
    }
    function gs(e, t) {
      t = t || V;
      var a = t.current;
      if (t = (a = ps(
        e,
        a && a.tag,
        t.implicitRootScope
      ) ? null : a) ? null : Pv(e, t), t = a || t, !t) return !0;
      var c = t.tag;
      if (t = String(!!a) + "|" + e + "|" + c, $[t]) return !1;
      $[t] = !0;
      var o = (t = ja) ? Va(t.return, c) : null, f = t !== null && o !== null ? rd(o, t, null) : "", d = "<" + e + ">";
      return a ? (a = "", c === "table" && e === "tr" && (a += " Add a <tbody>, <thead> or <tfoot> to your code to match the DOM tree generated by the browser."), console.error(
        `In HTML, %s cannot be a child of <%s>.%s
This will cause a hydration error.%s`,
        d,
        c,
        a,
        f
      )) : console.error(
        `In HTML, %s cannot be a descendant of <%s>.
This will cause a hydration error.%s`,
        d,
        c,
        f
      ), t && (e = t.return, o === null || e === null || o === e && e._debugOwner === t._debugOwner || oe(o, function() {
        console.error(
          `<%s> cannot contain a nested %s.
See this log for the ancestor stack trace.`,
          c,
          d
        );
      })), !1;
    }
    function vs(e, t, a) {
      if (a || ps("#text", t, !1))
        return !0;
      if (a = "#text|" + t, $[a]) return !1;
      $[a] = !0;
      var c = (a = ja) ? Va(a, t) : null;
      return a = a !== null && c !== null ? rd(
        c,
        a,
        a.tag !== 6 ? { children: null } : null
      ) : "", /\S/.test(e) ? console.error(
        `In HTML, text nodes cannot be a child of <%s>.
This will cause a hydration error.%s`,
        t,
        a
      ) : console.error(
        `In HTML, whitespace text nodes cannot be a child of <%s>. Make sure you don't have any extra whitespace between tags on each line of your source code.
This will cause a hydration error.%s`,
        t,
        a
      ), !1;
    }
    function Di(e, t) {
      if (t) {
        var a = e.firstChild;
        if (a && a === e.lastChild && a.nodeType === 3) {
          a.nodeValue = t;
          return;
        }
      }
      e.textContent = t;
    }
    function wo(e) {
      return e.replace(C, function(t, a) {
        return a.toUpperCase();
      });
    }
    function Um(e, t, a) {
      var c = t.indexOf("--") === 0;
      c || (-1 < t.indexOf("-") ? N.hasOwnProperty(t) && N[t] || (N[t] = !0, console.error(
        "Unsupported style property %s. Did you mean %s?",
        t,
        wo(t.replace(jt, "ms-"))
      )) : _e.test(t) ? N.hasOwnProperty(t) && N[t] || (N[t] = !0, console.error(
        "Unsupported vendor-prefixed style property %s. Did you mean %s?",
        t,
        t.charAt(0).toUpperCase() + t.slice(1)
      )) : !D.test(a) || K.hasOwnProperty(a) && K[a] || (K[a] = !0, console.error(
        `Style property values shouldn't contain a semicolon. Try "%s: %s" instead.`,
        t,
        a.replace(D, "")
      )), typeof a == "number" && (isNaN(a) ? Ee || (Ee = !0, console.error(
        "`NaN` is an invalid value for the `%s` css style property.",
        t
      )) : isFinite(a) || yt || (yt = !0, console.error(
        "`Infinity` is an invalid value for the `%s` css style property.",
        t
      )))), a == null || typeof a == "boolean" || a === "" ? c ? e.setProperty(t, "") : t === "float" ? e.cssFloat = "" : e[t] = "" : c ? e.setProperty(t, a) : typeof a != "number" || a === 0 || ye.has(t) ? t === "float" ? e.cssFloat = a : (ta(a, t), e[t] = ("" + a).trim()) : e[t] = a + "px";
    }
    function xm(e, t, a) {
      if (t != null && typeof t != "object")
        throw Error(
          "The `style` prop expects a mapping from style properties to values, not a string. For example, style={{marginRight: spacing + 'em'}} when using JSX."
        );
      if (t && Object.freeze(t), e = e.style, a != null) {
        if (t) {
          var c = {};
          if (a) {
            for (var o in a)
              if (a.hasOwnProperty(o) && !t.hasOwnProperty(o))
                for (var f = B[o] || [o], d = 0; d < f.length; d++)
                  c[f[d]] = o;
          }
          for (var h in t)
            if (t.hasOwnProperty(h) && (!a || a[h] !== t[h]))
              for (o = B[h] || [h], f = 0; f < o.length; f++)
                c[o[f]] = h;
          h = {};
          for (var y in t)
            for (o = B[y] || [y], f = 0; f < o.length; f++)
              h[o[f]] = y;
          y = {};
          for (var p in c)
            if (o = c[p], (f = h[p]) && o !== f && (d = o + "," + f, !y[d])) {
              y[d] = !0, d = console;
              var z = t[o];
              d.error.call(
                d,
                "%s a style property during rerender (%s) when a conflicting property is set (%s) can lead to styling bugs. To avoid this, don't mix shorthand and non-shorthand properties for the same value; instead, replace the shorthand with separate values.",
                z == null || typeof z == "boolean" || z === "" ? "Removing" : "Updating",
                o,
                f
              );
            }
        }
        for (var _ in a)
          !a.hasOwnProperty(_) || t != null && t.hasOwnProperty(_) || (_.indexOf("--") === 0 ? e.setProperty(_, "") : _ === "float" ? e.cssFloat = "" : e[_] = "");
        for (var E in t)
          p = t[E], t.hasOwnProperty(E) && a[E] !== p && Um(e, E, p);
      } else
        for (c in t)
          t.hasOwnProperty(c) && Um(e, c, t[c]);
    }
    function du(e) {
      if (e.indexOf("-") === -1) return !1;
      switch (e) {
        case "annotation-xml":
        case "color-profile":
        case "font-face":
        case "font-face-src":
        case "font-face-uri":
        case "font-face-format":
        case "font-face-name":
        case "missing-glyph":
          return !1;
        default:
          return !0;
      }
    }
    function Dp(e) {
      return bt.get(e) || e;
    }
    function Rp(e, t) {
      if (un.call(Zh, t) && Zh[t])
        return !0;
      if (uE.test(t)) {
        if (e = "aria-" + t.slice(4).toLowerCase(), e = kg.hasOwnProperty(e) ? e : null, e == null)
          return console.error(
            "Invalid ARIA attribute `%s`. ARIA attributes follow the pattern aria-* and must be lowercase.",
            t
          ), Zh[t] = !0;
        if (t !== e)
          return console.error(
            "Invalid ARIA attribute `%s`. Did you mean `%s`?",
            t,
            e
          ), Zh[t] = !0;
      }
      if (nE.test(t)) {
        if (e = t.toLowerCase(), e = kg.hasOwnProperty(e) ? e : null, e == null) return Zh[t] = !0, !1;
        t !== e && (console.error(
          "Unknown ARIA attribute `%s`. Did you mean `%s`?",
          t,
          e
        ), Zh[t] = !0);
      }
      return !0;
    }
    function _p(e, t) {
      var a = [], c;
      for (c in t)
        Rp(e, c) || a.push(c);
      t = a.map(function(o) {
        return "`" + o + "`";
      }).join(", "), a.length === 1 ? console.error(
        "Invalid aria prop %s on <%s> tag. For details, see https://react.dev/link/invalid-aria-props",
        t,
        e
      ) : 1 < a.length && console.error(
        "Invalid aria props %s on <%s> tag. For details, see https://react.dev/link/invalid-aria-props",
        t,
        e
      );
    }
    function Nm(e, t, a, c) {
      if (un.call(cn, t) && cn[t])
        return !0;
      var o = t.toLowerCase();
      if (o === "onfocusin" || o === "onfocusout")
        return console.error(
          "React uses onFocus and onBlur instead of onFocusIn and onFocusOut. All React events are normalized to bubble, so onFocusIn and onFocusOut are not needed/supported by React."
        ), cn[t] = !0;
      if (typeof a == "function" && (e === "form" && t === "action" || e === "input" && t === "formAction" || e === "button" && t === "formAction"))
        return !0;
      if (c != null) {
        if (e = c.possibleRegistrationNames, c.registrationNameDependencies.hasOwnProperty(t))
          return !0;
        if (c = e.hasOwnProperty(o) ? e[o] : null, c != null)
          return console.error(
            "Invalid event handler property `%s`. Did you mean `%s`?",
            t,
            c
          ), cn[t] = !0;
        if (US.test(t))
          return console.error(
            "Unknown event handler property `%s`. It will be ignored.",
            t
          ), cn[t] = !0;
      } else if (US.test(t))
        return cE.test(t) && console.error(
          "Invalid event handler property `%s`. React events use the camelCase naming convention, for example `onClick`.",
          t
        ), cn[t] = !0;
      if (iE.test(t) || oE.test(t)) return !0;
      if (o === "innerhtml")
        return console.error(
          "Directly setting property `innerHTML` is not permitted. For more information, lookup documentation on `dangerouslySetInnerHTML`."
        ), cn[t] = !0;
      if (o === "aria")
        return console.error(
          "The `aria` attribute is reserved for future use in React. Pass individual `aria-` attributes instead."
        ), cn[t] = !0;
      if (o === "is" && a !== null && a !== void 0 && typeof a != "string")
        return console.error(
          "Received a `%s` for a string attribute `is`. If this is expected, cast the value to a string.",
          typeof a
        ), cn[t] = !0;
      if (typeof a == "number" && isNaN(a))
        return console.error(
          "Received NaN for the `%s` attribute. If this is expected, cast the value to a string.",
          t
        ), cn[t] = !0;
      if (tu.hasOwnProperty(o)) {
        if (o = tu[o], o !== t)
          return console.error(
            "Invalid DOM property `%s`. Did you mean `%s`?",
            t,
            o
          ), cn[t] = !0;
      } else if (t !== o)
        return console.error(
          "React does not recognize the `%s` prop on a DOM element. If you intentionally want it to appear in the DOM as a custom attribute, spell it as lowercase `%s` instead. If you accidentally passed it from a parent component, remove it from the DOM element.",
          t,
          o
        ), cn[t] = !0;
      switch (t) {
        case "dangerouslySetInnerHTML":
        case "children":
        case "style":
        case "suppressContentEditableWarning":
        case "suppressHydrationWarning":
        case "defaultValue":
        case "defaultChecked":
        case "innerHTML":
        case "ref":
          return !0;
        case "innerText":
        case "textContent":
          return !0;
      }
      switch (typeof a) {
        case "boolean":
          switch (t) {
            case "autoFocus":
            case "checked":
            case "multiple":
            case "muted":
            case "selected":
            case "contentEditable":
            case "spellCheck":
            case "draggable":
            case "value":
            case "autoReverse":
            case "externalResourcesRequired":
            case "focusable":
            case "preserveAlpha":
            case "allowFullScreen":
            case "async":
            case "autoPlay":
            case "controls":
            case "default":
            case "defer":
            case "disabled":
            case "disablePictureInPicture":
            case "disableRemotePlayback":
            case "formNoValidate":
            case "hidden":
            case "loop":
            case "noModule":
            case "noValidate":
            case "open":
            case "playsInline":
            case "readOnly":
            case "required":
            case "reversed":
            case "scoped":
            case "seamless":
            case "itemScope":
            case "capture":
            case "download":
            case "inert":
              return !0;
            default:
              return o = t.toLowerCase().slice(0, 5), o === "data-" || o === "aria-" ? !0 : (a ? console.error(
                'Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.',
                a,
                t,
                t,
                a,
                t
              ) : console.error(
                'Received `%s` for a non-boolean attribute `%s`.\n\nIf you want to write it to the DOM, pass a string instead: %s="%s" or %s={value.toString()}.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.',
                a,
                t,
                t,
                a,
                t,
                t,
                t
              ), cn[t] = !0);
          }
        case "function":
        case "symbol":
          return cn[t] = !0, !1;
        case "string":
          if (a === "false" || a === "true") {
            switch (t) {
              case "checked":
              case "selected":
              case "multiple":
              case "muted":
              case "allowFullScreen":
              case "async":
              case "autoPlay":
              case "controls":
              case "default":
              case "defer":
              case "disabled":
              case "disablePictureInPicture":
              case "disableRemotePlayback":
              case "formNoValidate":
              case "hidden":
              case "loop":
              case "noModule":
              case "noValidate":
              case "open":
              case "playsInline":
              case "readOnly":
              case "required":
              case "reversed":
              case "scoped":
              case "seamless":
              case "itemScope":
              case "inert":
                break;
              default:
                return !0;
            }
            console.error(
              "Received the string `%s` for the boolean attribute `%s`. %s Did you mean %s={%s}?",
              a,
              t,
              a === "false" ? "The browser will interpret it as a truthy value." : 'Although this works, it will not work as expected if you pass the string "false".',
              t,
              a
            ), cn[t] = !0;
          }
      }
      return !0;
    }
    function e1(e, t, a) {
      var c = [], o;
      for (o in t)
        Nm(e, o, t[o], a) || c.push(o);
      t = c.map(function(f) {
        return "`" + f + "`";
      }).join(", "), c.length === 1 ? console.error(
        "Invalid value for prop %s on <%s> tag. Either remove it from the element, or pass a string or number value to keep it in the DOM. For details, see https://react.dev/link/attribute-behavior ",
        t,
        e
      ) : 1 < c.length && console.error(
        "Invalid values for props %s on <%s> tag. Either remove them from the element, or pass a string or number value to keep them in the DOM. For details, see https://react.dev/link/attribute-behavior ",
        t,
        e
      );
    }
    function Ss(e) {
      return fE.test("" + e) ? "javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')" : e;
    }
    function yn() {
    }
    function Nn(e) {
      return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
    }
    function dd(e) {
      var t = ae(e);
      if (t && (e = t.stateNode)) {
        var a = e[Da] || null;
        e: switch (e = t.stateNode, t.type) {
          case "input":
            if (Nc(
              e,
              a.value,
              a.defaultValue,
              a.defaultValue,
              a.checked,
              a.defaultChecked,
              a.type,
              a.name
            ), t = a.name, a.type === "radio" && t != null) {
              for (a = e; a.parentNode; ) a = a.parentNode;
              for (vt(t, "name"), a = a.querySelectorAll(
                'input[name="' + Ut(
                  "" + t
                ) + '"][type="radio"]'
              ), t = 0; t < a.length; t++) {
                var c = a[t];
                if (c !== e && c.form === e.form) {
                  var o = c[Da] || null;
                  if (!o)
                    throw Error(
                      "ReactDOMInput: Mixing React and non-React radio inputs with the same `name` is not supported."
                    );
                  Nc(
                    c,
                    o.value,
                    o.defaultValue,
                    o.defaultValue,
                    o.checked,
                    o.defaultChecked,
                    o.type,
                    o.name
                  );
                }
              }
              for (t = 0; t < a.length; t++)
                c = a[t], c.form === e.form && Dm(c);
            }
            break e;
          case "textarea":
            Ai(e, a.value, a.defaultValue);
            break e;
          case "select":
            t = a.value, t != null && su(e, !!a.multiple, t, !1);
        }
      }
    }
    function hd(e, t, a) {
      if (m1) return e(t, a);
      m1 = !0;
      try {
        var c = e(t);
        return c;
      } finally {
        if (m1 = !1, (Jh !== null || Kh !== null) && (ln(), Jh && (t = Jh, e = Kh, Kh = Jh = null, dd(t), e)))
          for (t = 0; t < e.length; t++) dd(e[t]);
      }
    }
    function hu(e, t) {
      var a = e.stateNode;
      if (a === null) return null;
      var c = a[Da] || null;
      if (c === null) return null;
      a = c[t];
      e: switch (t) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          (c = !c.disabled) || (e = e.type, c = !(e === "button" || e === "input" || e === "select" || e === "textarea")), e = !c;
          break e;
        default:
          e = !1;
      }
      if (e) return null;
      if (a && typeof a != "function")
        throw Error(
          "Expected `" + t + "` listener to be a function, instead got a value of `" + typeof a + "` type."
        );
      return a;
    }
    function Ri() {
      if (Wg) return Wg;
      var e, t = p1, a = t.length, c, o = "value" in Qf ? Qf.value : Qf.textContent, f = o.length;
      for (e = 0; e < a && t[e] === o[e]; e++) ;
      var d = a - e;
      for (c = 1; c <= d && t[a - c] === o[f - c]; c++) ;
      return Wg = o.slice(e, 1 < c ? 1 - c : void 0);
    }
    function bs(e) {
      var t = e.keyCode;
      return "charCode" in e ? (e = e.charCode, e === 0 && t === 13 && (e = 13)) : e = t, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
    }
    function Go() {
      return !0;
    }
    function Hm() {
      return !1;
    }
    function Hl(e) {
      function t(a, c, o, f, d) {
        this._reactName = a, this._targetInst = o, this.type = c, this.nativeEvent = f, this.target = d, this.currentTarget = null;
        for (var h in e)
          e.hasOwnProperty(h) && (a = e[h], this[h] = a ? a(f) : f[h]);
        return this.isDefaultPrevented = (f.defaultPrevented != null ? f.defaultPrevented : f.returnValue === !1) ? Go : Hm, this.isPropagationStopped = Hm, this;
      }
      return Ie(t.prototype, {
        preventDefault: function() {
          this.defaultPrevented = !0;
          var a = this.nativeEvent;
          a && (a.preventDefault ? a.preventDefault() : typeof a.returnValue != "unknown" && (a.returnValue = !1), this.isDefaultPrevented = Go);
        },
        stopPropagation: function() {
          var a = this.nativeEvent;
          a && (a.stopPropagation ? a.stopPropagation() : typeof a.cancelBubble != "unknown" && (a.cancelBubble = !0), this.isPropagationStopped = Go);
        },
        persist: function() {
        },
        isPersistent: Go
      }), t;
    }
    function ec(e) {
      var t = this.nativeEvent;
      return t.getModifierState ? t.getModifierState(e) : (e = TE[e]) ? !!t[e] : !1;
    }
    function Es() {
      return ec;
    }
    function Xo(e, t) {
      switch (e) {
        case "keyup":
          return HE.indexOf(t.keyCode) !== -1;
        case "keydown":
          return t.keyCode !== jS;
        case "keypress":
        case "mousedown":
        case "focusout":
          return !0;
        default:
          return !1;
      }
    }
    function tc(e) {
      return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
    }
    function jm(e, t) {
      switch (e) {
        case "compositionend":
          return tc(t);
        case "keypress":
          return t.which !== YS ? null : (wS = !0, qS);
        case "textInput":
          return e = t.data, e === qS && wS ? null : e;
        default:
          return null;
      }
    }
    function md(e, t) {
      if ($h)
        return e === "compositionend" || !b1 && Xo(e, t) ? (e = Ri(), Wg = p1 = Qf = null, $h = !1, e) : null;
      switch (e) {
        case "paste":
          return null;
        case "keypress":
          if (!(t.ctrlKey || t.altKey || t.metaKey) || t.ctrlKey && t.altKey) {
            if (t.char && 1 < t.char.length)
              return t.char;
            if (t.which)
              return String.fromCharCode(t.which);
          }
          return null;
        case "compositionend":
          return BS && t.locale !== "ko" ? null : t.data;
        default:
          return null;
      }
    }
    function Bm(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t === "input" ? !!BE[e.type] : t === "textarea";
    }
    function yd(e) {
      if (!mi) return !1;
      e = "on" + e;
      var t = e in document;
      return t || (t = document.createElement("div"), t.setAttribute(e, "return;"), t = typeof t[e] == "function"), t;
    }
    function Ts(e, t, a, c) {
      Jh ? Kh ? Kh.push(c) : Kh = [c] : Jh = c, t = Wn(t, "onChange"), 0 < t.length && (a = new Fg(
        "onChange",
        "change",
        null,
        a,
        c
      ), e.push({ event: a, listeners: t }));
    }
    function Mp(e) {
      _t(e, 0);
    }
    function kl(e) {
      var t = he(e);
      if (Dm(t)) return e;
    }
    function Bc(e, t) {
      if (e === "change") return t;
    }
    function As() {
      H0 && (H0.detachEvent("onpropertychange", Lo), j0 = H0 = null);
    }
    function Lo(e) {
      if (e.propertyName === "value" && kl(j0)) {
        var t = [];
        Ts(
          t,
          j0,
          e,
          Nn(e)
        ), hd(Mp, t);
      }
    }
    function t1(e, t, a) {
      e === "focusin" ? (As(), H0 = t, j0 = a, H0.attachEvent("onpropertychange", Lo)) : e === "focusout" && As();
    }
    function Ym(e) {
      if (e === "selectionchange" || e === "keyup" || e === "keydown")
        return kl(j0);
    }
    function qm(e, t) {
      if (e === "click") return kl(t);
    }
    function Os(e, t) {
      if (e === "input" || e === "change")
        return kl(t);
    }
    function pd(e, t) {
      return e === t && (e !== 0 || 1 / e === 1 / t) || e !== e && t !== t;
    }
    function Qo(e, t) {
      if (on(e, t)) return !0;
      if (typeof e != "object" || e === null || typeof t != "object" || t === null)
        return !1;
      var a = Object.keys(e), c = Object.keys(t);
      if (a.length !== c.length) return !1;
      for (c = 0; c < a.length; c++) {
        var o = a[c];
        if (!un.call(t, o) || !on(e[o], t[o]))
          return !1;
      }
      return !0;
    }
    function Cp(e) {
      for (; e && e.firstChild; ) e = e.firstChild;
      return e;
    }
    function Up(e, t) {
      var a = Cp(e);
      e = 0;
      for (var c; a; ) {
        if (a.nodeType === 3) {
          if (c = e + a.textContent.length, e <= t && c >= t)
            return { node: a, offset: t - e };
          e = c;
        }
        e: {
          for (; a; ) {
            if (a.nextSibling) {
              a = a.nextSibling;
              break e;
            }
            a = a.parentNode;
          }
          a = void 0;
        }
        a = Cp(a);
      }
    }
    function xp(e, t) {
      return e && t ? e === t ? !0 : e && e.nodeType === 3 ? !1 : t && t.nodeType === 3 ? xp(e, t.parentNode) : "contains" in e ? e.contains(t) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(t) & 16) : !1 : !1;
    }
    function gd(e) {
      e = e != null && e.ownerDocument != null && e.ownerDocument.defaultView != null ? e.ownerDocument.defaultView : window;
      for (var t = xn(e.document); t instanceof e.HTMLIFrameElement; ) {
        try {
          var a = typeof t.contentWindow.location.href == "string";
        } catch {
          a = !1;
        }
        if (a) e = t.contentWindow;
        else break;
        t = xn(e.document);
      }
      return t;
    }
    function wm(e) {
      var t = e && e.nodeName && e.nodeName.toLowerCase();
      return t && (t === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || t === "textarea" || e.contentEditable === "true");
    }
    function Np(e, t, a) {
      var c = a.window === a ? a.document : a.nodeType === 9 ? a : a.ownerDocument;
      T1 || kh == null || kh !== xn(c) || (c = kh, "selectionStart" in c && wm(c) ? c = { start: c.selectionStart, end: c.selectionEnd } : (c = (c.ownerDocument && c.ownerDocument.defaultView || window).getSelection(), c = {
        anchorNode: c.anchorNode,
        anchorOffset: c.anchorOffset,
        focusNode: c.focusNode,
        focusOffset: c.focusOffset
      }), B0 && Qo(B0, c) || (B0 = c, c = Wn(E1, "onSelect"), 0 < c.length && (t = new Fg(
        "onSelect",
        "select",
        null,
        t,
        a
      ), e.push({ event: t, listeners: c }), t.target = kh)));
    }
    function _i(e, t) {
      var a = {};
      return a[e.toLowerCase()] = t.toLowerCase(), a["Webkit" + e] = "webkit" + t, a["Moz" + e] = "moz" + t, a;
    }
    function Mi(e) {
      if (A1[e]) return A1[e];
      if (!Wh[e]) return e;
      var t = Wh[e], a;
      for (a in t)
        if (t.hasOwnProperty(a) && a in XS)
          return A1[e] = t[a];
      return e;
    }
    function Hn(e, t) {
      JS.set(e, t), lt(t, [e]);
    }
    function Hp(e) {
      for (var t = Pg, a = 0; a < e.length; a++) {
        var c = e[a];
        if (typeof c == "object" && c !== null)
          if (Al(c) && c.length === 2 && typeof c[0] == "string") {
            if (t !== Pg && t !== _1)
              return D1;
            t = _1;
          } else return D1;
        else {
          if (typeof c == "function" || typeof c == "string" && 50 < c.length || t !== Pg && t !== R1)
            return D1;
          t = R1;
        }
      }
      return t;
    }
    function Gm(e, t, a, c) {
      for (var o in e)
        un.call(e, o) && o[0] !== "_" && mu(o, e[o], t, a, c);
    }
    function mu(e, t, a, c, o) {
      switch (typeof t) {
        case "object":
          if (t === null) {
            t = "null";
            break;
          } else {
            if (t.$$typeof === Dn) {
              var f = Je(t.type) || "…", d = t.key;
              t = t.props;
              var h = Object.keys(t), y = h.length;
              if (d == null && y === 0) {
                t = "<" + f + " />";
                break;
              }
              if (3 > c || y === 1 && h[0] === "children" && d == null) {
                t = "<" + f + " … />";
                break;
              }
              a.push([
                o + "  ".repeat(c) + e,
                "<" + f
              ]), d !== null && mu(
                "key",
                d,
                a,
                c + 1,
                o
              ), e = !1;
              for (var p in t)
                p === "children" ? t.children != null && (!Al(t.children) || 0 < t.children.length) && (e = !0) : un.call(t, p) && p[0] !== "_" && mu(
                  p,
                  t[p],
                  a,
                  c + 1,
                  o
                );
              a.push([
                "",
                e ? ">…</" + f + ">" : "/>"
              ]);
              return;
            }
            if (f = Object.prototype.toString.call(t), f = f.slice(8, f.length - 1), f === "Array") {
              if (p = Hp(t), p === R1 || p === Pg) {
                t = JSON.stringify(t);
                break;
              } else if (p === _1) {
                for (a.push([
                  o + "  ".repeat(c) + e,
                  ""
                ]), e = 0; e < t.length; e++)
                  f = t[e], mu(
                    f[0],
                    f[1],
                    a,
                    c + 1,
                    o
                  );
                return;
              }
            }
            if (f === "Promise") {
              if (t.status === "fulfilled") {
                if (f = a.length, mu(
                  e,
                  t.value,
                  a,
                  c,
                  o
                ), a.length > f) {
                  a = a[f], a[1] = "Promise<" + (a[1] || "Object") + ">";
                  return;
                }
              } else if (t.status === "rejected" && (f = a.length, mu(
                e,
                t.reason,
                a,
                c,
                o
              ), a.length > f)) {
                a = a[f], a[1] = "Rejected Promise<" + a[1] + ">";
                return;
              }
              a.push([
                "  ".repeat(c) + e,
                "Promise"
              ]);
              return;
            }
            f === "Object" && (p = Object.getPrototypeOf(t)) && typeof p.constructor == "function" && (f = p.constructor.name), a.push([
              o + "  ".repeat(c) + e,
              f === "Object" ? 3 > c ? "" : "…" : f
            ]), 3 > c && Gm(t, a, c + 1, o);
            return;
          }
        case "function":
          t = t.name === "" ? "() => {}" : t.name + "() {}";
          break;
        case "string":
          t = t === QE ? "…" : JSON.stringify(t);
          break;
        case "undefined":
          t = "undefined";
          break;
        case "boolean":
          t = t ? "true" : "false";
          break;
        default:
          t = String(t);
      }
      a.push([
        o + "  ".repeat(c) + e,
        t
      ]);
    }
    function jp(e, t, a, c) {
      var o = !0;
      for (d in e)
        d in t || (a.push([
          ev + "  ".repeat(c) + d,
          "…"
        ]), o = !1);
      for (var f in t)
        if (f in e) {
          var d = e[f], h = t[f];
          if (d !== h) {
            if (c === 0 && f === "children")
              o = "  ".repeat(c) + f, a.push(
                [ev + o, "…"],
                [tv + o, "…"]
              );
            else {
              if (!(3 <= c)) {
                if (typeof d == "object" && typeof h == "object" && d !== null && h !== null && d.$$typeof === h.$$typeof)
                  if (h.$$typeof === Dn) {
                    if (d.type === h.type && d.key === h.key) {
                      d = Je(h.type) || "…", o = "  ".repeat(c) + f, d = "<" + d + " … />", a.push(
                        [ev + o, d],
                        [tv + o, d]
                      ), o = !1;
                      continue;
                    }
                  } else {
                    var y = Object.prototype.toString.call(d), p = Object.prototype.toString.call(h);
                    if (y === p && (p === "[object Object]" || p === "[object Array]")) {
                      y = [
                        kS + "  ".repeat(c) + f,
                        p === "[object Array]" ? "Array" : ""
                      ], a.push(y), p = a.length, jp(
                        d,
                        h,
                        a,
                        c + 1
                      ) ? p === a.length && (y[1] = "Referentially unequal but deeply equal objects. Consider memoization.") : o = !1;
                      continue;
                    }
                  }
                else if (typeof d == "function" && typeof h == "function" && d.name === h.name && d.length === h.length && (y = Function.prototype.toString.call(d), p = Function.prototype.toString.call(h), y === p)) {
                  d = h.name === "" ? "() => {}" : h.name + "() {}", a.push([
                    kS + "  ".repeat(c) + f,
                    d + " Referentially unequal function closure. Consider memoization."
                  ]);
                  continue;
                }
              }
              mu(f, d, a, c, ev), mu(f, h, a, c, tv);
            }
            o = !1;
          }
        } else
          a.push([
            tv + "  ".repeat(c) + f,
            "…"
          ]), o = !1;
      return o;
    }
    function jn(e) {
      ht = e & 63 ? "Blocking" : e & 64 ? "Gesture" : e & 4194176 ? "Transition" : e & 62914560 ? "Suspense" : e & 2080374784 ? "Idle" : "Other";
    }
    function pn(e, t, a, c) {
      tl && (Zf.start = t, Zf.end = a, yo.color = "warning", yo.tooltipText = c, yo.properties = null, (e = e._debugTask) ? e.run(
        performance.measure.bind(
          performance,
          c,
          Zf
        )
      ) : performance.measure(c, Zf));
    }
    function vd(e, t, a) {
      pn(e, t, a, "Reconnect");
    }
    function Sd(e, t, a, c, o) {
      var f = se(e);
      if (f !== null && tl) {
        var d = e.alternate, h = e.actualDuration;
        if (d === null || d.child !== e.child)
          for (var y = e.child; y !== null; y = y.sibling)
            h -= y.actualDuration;
        c = 0.5 > h ? c ? "tertiary-light" : "primary-light" : 10 > h ? c ? "tertiary" : "primary" : 100 > h ? c ? "tertiary-dark" : "primary-dark" : "error";
        var p = e.memoizedProps;
        h = e._debugTask, p !== null && d !== null && d.memoizedProps !== p ? (y = [VE], p = jp(
          d.memoizedProps,
          p,
          y,
          0
        ), 1 < y.length && (p && !Vf && (d.lanes & o) === 0 && 100 < e.actualDuration ? (Vf = !0, y[0] = ZE, yo.color = "warning", yo.tooltipText = WS) : (yo.color = c, yo.tooltipText = f), yo.properties = y, Zf.start = t, Zf.end = a, h != null ? h.run(
          performance.measure.bind(
            performance,
            "​" + f,
            Zf
          )
        ) : performance.measure(
          "​" + f,
          Zf
        ))) : h != null ? h.run(
          console.timeStamp.bind(
            console,
            f,
            t,
            a,
            Xu,
            void 0,
            c
          )
        ) : console.timeStamp(
          f,
          t,
          a,
          Xu,
          void 0,
          c
        );
      }
    }
    function Xm(e, t, a, c) {
      if (tl) {
        var o = se(e);
        if (o !== null) {
          for (var f = null, d = [], h = 0; h < c.length; h++) {
            var y = c[h];
            f == null && y.source !== null && (f = y.source._debugTask), y = y.value, d.push([
              "Error",
              typeof y == "object" && y !== null && typeof y.message == "string" ? String(y.message) : String(y)
            ]);
          }
          e.key !== null && mu("key", e.key, d, 0, ""), e.memoizedProps !== null && Gm(e.memoizedProps, d, 0, ""), f == null && (f = e._debugTask), e = {
            start: t,
            end: a,
            detail: {
              devtools: {
                color: "error",
                track: Xu,
                tooltipText: e.tag === 13 ? "Hydration failed" : "Error boundary caught an error",
                properties: d
              }
            }
          }, f ? f.run(
            performance.measure.bind(performance, "​" + o, e)
          ) : performance.measure("​" + o, e);
        }
      }
    }
    function Bn(e, t, a, c, o) {
      if (o !== null) {
        if (tl) {
          var f = se(e);
          if (f !== null) {
            c = [];
            for (var d = 0; d < o.length; d++) {
              var h = o[d].value;
              c.push([
                "Error",
                typeof h == "object" && h !== null && typeof h.message == "string" ? String(h.message) : String(h)
              ]);
            }
            e.key !== null && mu("key", e.key, c, 0, ""), e.memoizedProps !== null && Gm(e.memoizedProps, c, 0, ""), t = {
              start: t,
              end: a,
              detail: {
                devtools: {
                  color: "error",
                  track: Xu,
                  tooltipText: "A lifecycle or effect errored",
                  properties: c
                }
              }
            }, (e = e._debugTask) ? e.run(
              performance.measure.bind(
                performance,
                "​" + f,
                t
              )
            ) : performance.measure("​" + f, t);
          }
        }
      } else
        f = se(e), f !== null && tl && (o = 1 > c ? "secondary-light" : 100 > c ? "secondary" : 500 > c ? "secondary-dark" : "error", (e = e._debugTask) ? e.run(
          console.timeStamp.bind(
            console,
            f,
            t,
            a,
            Xu,
            void 0,
            o
          )
        ) : console.timeStamp(
          f,
          t,
          a,
          Xu,
          void 0,
          o
        ));
    }
    function l1(e, t, a, c) {
      if (tl && !(t <= e)) {
        var o = (a & 738197653) === a ? "tertiary-dark" : "primary-dark";
        a = (a & 536870912) === a ? "Prepared" : (a & 201326741) === a ? "Hydrated" : "Render", c ? c.run(
          console.timeStamp.bind(
            console,
            a,
            e,
            t,
            ht,
            rt,
            o
          )
        ) : console.timeStamp(
          a,
          e,
          t,
          ht,
          rt,
          o
        );
      }
    }
    function Bp(e, t, a, c) {
      !tl || t <= e || (a = (a & 738197653) === a ? "tertiary-dark" : "primary-dark", c ? c.run(
        console.timeStamp.bind(
          console,
          "Prewarm",
          e,
          t,
          ht,
          rt,
          a
        )
      ) : console.timeStamp(
        "Prewarm",
        e,
        t,
        ht,
        rt,
        a
      ));
    }
    function Yp(e, t, a, c) {
      !tl || t <= e || (a = (a & 738197653) === a ? "tertiary-dark" : "primary-dark", c ? c.run(
        console.timeStamp.bind(
          console,
          "Suspended",
          e,
          t,
          ht,
          rt,
          a
        )
      ) : console.timeStamp(
        "Suspended",
        e,
        t,
        ht,
        rt,
        a
      ));
    }
    function a1(e, t, a, c, o, f) {
      if (tl && !(t <= e)) {
        a = [];
        for (var d = 0; d < c.length; d++) {
          var h = c[d].value;
          a.push([
            "Recoverable Error",
            typeof h == "object" && h !== null && typeof h.message == "string" ? String(h.message) : String(h)
          ]);
        }
        e = {
          start: e,
          end: t,
          detail: {
            devtools: {
              color: "primary-dark",
              track: ht,
              trackGroup: rt,
              tooltipText: o ? "Hydration Failed" : "Recovered after Error",
              properties: a
            }
          }
        }, f ? f.run(
          performance.measure.bind(performance, "Recovered", e)
        ) : performance.measure("Recovered", e);
      }
    }
    function Lm(e, t, a, c) {
      !tl || t <= e || (c ? c.run(
        console.timeStamp.bind(
          console,
          "Errored",
          e,
          t,
          ht,
          rt,
          "error"
        )
      ) : console.timeStamp(
        "Errored",
        e,
        t,
        ht,
        rt,
        "error"
      ));
    }
    function n1(e, t, a, c) {
      !tl || t <= e || (c ? c.run(
        console.timeStamp.bind(
          console,
          a,
          e,
          t,
          ht,
          rt,
          "secondary-light"
        )
      ) : console.timeStamp(
        a,
        e,
        t,
        ht,
        rt,
        "secondary-light"
      ));
    }
    function qp(e, t, a, c, o) {
      if (tl && !(t <= e)) {
        for (var f = [], d = 0; d < a.length; d++) {
          var h = a[d].value;
          f.push([
            "Error",
            typeof h == "object" && h !== null && typeof h.message == "string" ? String(h.message) : String(h)
          ]);
        }
        e = {
          start: e,
          end: t,
          detail: {
            devtools: {
              color: "error",
              track: ht,
              trackGroup: rt,
              tooltipText: c ? "Remaining Effects Errored" : "Commit Errored",
              properties: f
            }
          }
        }, o ? o.run(
          performance.measure.bind(performance, "Errored", e)
        ) : performance.measure("Errored", e);
      }
    }
    function Qm(e, t, a) {
      !tl || t <= e || console.timeStamp(
        "Animating",
        e,
        t,
        ht,
        rt,
        "secondary-dark"
      );
    }
    function bd() {
      for (var e = Fh, t = M1 = Fh = 0; t < e; ) {
        var a = Lu[t];
        Lu[t++] = null;
        var c = Lu[t];
        Lu[t++] = null;
        var o = Lu[t];
        Lu[t++] = null;
        var f = Lu[t];
        if (Lu[t++] = null, c !== null && o !== null) {
          var d = c.pending;
          d === null ? o.next = o : (o.next = d.next, d.next = o), c.pending = o;
        }
        f !== 0 && Vm(a, o, f);
      }
    }
    function Vo(e, t, a, c) {
      Lu[Fh++] = e, Lu[Fh++] = t, Lu[Fh++] = a, Lu[Fh++] = c, M1 |= c, e.lanes |= c, e = e.alternate, e !== null && (e.lanes |= c);
    }
    function Ci(e, t, a, c) {
      return Vo(e, t, a, c), zs(e);
    }
    function aa(e, t) {
      return Vo(e, null, null, t), zs(e);
    }
    function Vm(e, t, a) {
      e.lanes |= a;
      var c = e.alternate;
      c !== null && (c.lanes |= a);
      for (var o = !1, f = e.return; f !== null; )
        f.childLanes |= a, c = f.alternate, c !== null && (c.childLanes |= a), f.tag === 22 && (e = f.stateNode, e === null || e._visibility & Y0 || (o = !0)), e = f, f = f.return;
      return e.tag === 3 ? (f = e.stateNode, o && t !== null && (o = 31 - Fl(a), e = f.hiddenUpdates, c = e[o], c === null ? e[o] = [t] : c.push(t), t.lane = a | 536870912), f) : null;
    }
    function zs(e) {
      if (sp > iT)
        throw Kr = sp = 0, rp = oS = null, Error(
          "Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate. React limits the number of nested updates to prevent infinite loops."
        );
      Kr > oT && (Kr = 0, rp = null, console.error(
        "Maximum update depth exceeded. This can happen when a component calls setState inside useEffect, but useEffect either doesn't have a dependency array, or one of the dependencies changes on every render."
      )), e.alternate === null && (e.flags & 4098) !== 0 && zn(e);
      for (var t = e, a = t.return; a !== null; )
        t.alternate === null && (t.flags & 4098) !== 0 && zn(e), t = a, a = t.return;
      return t.tag === 3 ? t.stateNode : null;
    }
    function Yc(e) {
      if (Qu === null) return e;
      var t = Qu(e);
      return t === void 0 ? e : t.current;
    }
    function Ed(e) {
      if (Qu === null) return e;
      var t = Qu(e);
      return t === void 0 ? e != null && typeof e.render == "function" && (t = Yc(e.render), e.render !== t) ? (t = { $$typeof: xf, render: t }, e.displayName !== void 0 && (t.displayName = e.displayName), t) : e : t.current;
    }
    function Zm(e, t) {
      if (Qu === null) return !1;
      var a = e.elementType;
      t = t.type;
      var c = !1, o = typeof t == "object" && t !== null ? t.$$typeof : null;
      switch (e.tag) {
        case 1:
          typeof t == "function" && (c = !0);
          break;
        case 0:
          (typeof t == "function" || o === ca) && (c = !0);
          break;
        case 11:
          (o === xf || o === ca) && (c = !0);
          break;
        case 14:
        case 15:
          (o === zr || o === ca) && (c = !0);
          break;
        default:
          return !1;
      }
      return !!(c && (e = Qu(a), e !== void 0 && e === Qu(t)));
    }
    function Ui(e) {
      Qu !== null && typeof WeakSet == "function" && (Ih === null && (Ih = /* @__PURE__ */ new WeakSet()), Ih.add(e));
    }
    function wp(e, t, a) {
      do {
        var c = e, o = c.alternate, f = c.child, d = c.sibling, h = c.tag;
        c = c.type;
        var y = null;
        switch (h) {
          case 0:
          case 15:
          case 1:
            y = c;
            break;
          case 11:
            y = c.render;
        }
        if (Qu === null)
          throw Error("Expected resolveFamily to be set during hot reload.");
        var p = !1;
        if (c = !1, y !== null && (y = Qu(y), y !== void 0 && (a.has(y) ? c = !0 : t.has(y) && (h === 1 ? c = !0 : p = !0))), Ih !== null && (Ih.has(e) || o !== null && Ih.has(o)) && (c = !0), c && (e._debugNeedsRemount = !0), (c || p) && (o = aa(e, 2), o !== null && je(o, e, 2)), f === null || c || wp(
          f,
          t,
          a
        ), d === null) break;
        e = d;
      } while (!0);
    }
    function u1(e, t, a, c) {
      this.tag = e, this.key = a, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.refCleanup = this.ref = null, this.pendingProps = t, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = c, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null, this.actualDuration = -0, this.actualStartTime = -1.1, this.treeBaseDuration = this.selfBaseDuration = -0, this._debugTask = this._debugStack = this._debugOwner = this._debugInfo = null, this._debugNeedsRemount = !1, this._debugHookTypes = null, FS || typeof Object.preventExtensions != "function" || Object.preventExtensions(this);
    }
    function Jm(e) {
      return e = e.prototype, !(!e || !e.isReactComponent);
    }
    function yu(e, t) {
      var a = e.alternate;
      switch (a === null ? (a = x(
        e.tag,
        t,
        e.key,
        e.mode
      ), a.elementType = e.elementType, a.type = e.type, a.stateNode = e.stateNode, a._debugOwner = e._debugOwner, a._debugStack = e._debugStack, a._debugTask = e._debugTask, a._debugHookTypes = e._debugHookTypes, a.alternate = e, e.alternate = a) : (a.pendingProps = t, a.type = e.type, a.flags = 0, a.subtreeFlags = 0, a.deletions = null, a.actualDuration = -0, a.actualStartTime = -1.1), a.flags = e.flags & 65011712, a.childLanes = e.childLanes, a.lanes = e.lanes, a.child = e.child, a.memoizedProps = e.memoizedProps, a.memoizedState = e.memoizedState, a.updateQueue = e.updateQueue, t = e.dependencies, a.dependencies = t === null ? null : {
        lanes: t.lanes,
        firstContext: t.firstContext,
        _debugThenableState: t._debugThenableState
      }, a.sibling = e.sibling, a.index = e.index, a.ref = e.ref, a.refCleanup = e.refCleanup, a.selfBaseDuration = e.selfBaseDuration, a.treeBaseDuration = e.treeBaseDuration, a._debugInfo = e._debugInfo, a._debugNeedsRemount = e._debugNeedsRemount, a.tag) {
        case 0:
        case 15:
          a.type = Yc(e.type);
          break;
        case 1:
          a.type = Yc(e.type);
          break;
        case 11:
          a.type = Ed(e.type);
      }
      return a;
    }
    function Km(e, t) {
      e.flags &= 65011714;
      var a = e.alternate;
      return a === null ? (e.childLanes = 0, e.lanes = t, e.child = null, e.subtreeFlags = 0, e.memoizedProps = null, e.memoizedState = null, e.updateQueue = null, e.dependencies = null, e.stateNode = null, e.selfBaseDuration = 0, e.treeBaseDuration = 0) : (e.childLanes = a.childLanes, e.lanes = a.lanes, e.child = a.child, e.subtreeFlags = 0, e.deletions = null, e.memoizedProps = a.memoizedProps, e.memoizedState = a.memoizedState, e.updateQueue = a.updateQueue, e.type = a.type, t = a.dependencies, e.dependencies = t === null ? null : {
        lanes: t.lanes,
        firstContext: t.firstContext,
        _debugThenableState: t._debugThenableState
      }, e.selfBaseDuration = a.selfBaseDuration, e.treeBaseDuration = a.treeBaseDuration), e;
    }
    function xi(e, t, a, c, o, f) {
      var d = 0, h = e;
      if (typeof e == "function")
        Jm(e) && (d = 1), h = Yc(h);
      else if (typeof e == "string")
        d = Z(), d = Hg(e, a, d) ? 26 : e === "html" || e === "head" || e === "body" ? 27 : 5;
      else
        e: switch (e) {
          case eu:
            return t = x(31, a, t, o), t.elementType = eu, t.lanes = f, t;
          case Uf:
            return Ni(
              a.children,
              o,
              f,
              t
            );
          case za:
            d = 8, o |= Ba, o |= Tc;
            break;
          case Or:
            return e = a, c = o, typeof e.id != "string" && console.error(
              'Profiler must specify an "id" of type `string` as a prop. Received the type `%s` instead.',
              typeof e.id
            ), t = x(12, e, t, c | Pe), t.elementType = Or, t.lanes = f, t.stateNode = { effectDuration: 0, passiveEffectDuration: 0 }, t;
          case fo:
            return t = x(13, a, t, o), t.elementType = fo, t.lanes = f, t;
          case Ha:
            return t = x(19, a, t, o), t.elementType = Ha, t.lanes = f, t;
          default:
            if (typeof e == "object" && e !== null)
              switch (e.$$typeof) {
                case Pn:
                  d = 10;
                  break e;
                case Nh:
                  d = 9;
                  break e;
                case xf:
                  d = 11, h = Ed(h);
                  break e;
                case zr:
                  d = 14;
                  break e;
                case ca:
                  d = 16, h = null;
                  break e;
              }
            h = "", (e === void 0 || typeof e == "object" && e !== null && Object.keys(e).length === 0) && (h += " You likely forgot to export your component from the file it's defined in, or you might have mixed up default and named imports."), e === null ? a = "null" : Al(e) ? a = "array" : e !== void 0 && e.$$typeof === Dn ? (a = "<" + (Je(e.type) || "Unknown") + " />", h = " Did you accidentally export a JSX literal instead of a component?") : a = typeof e, (d = c ? Me(c) : null) && (h += `

Check the render method of \`` + d + "`."), d = 29, a = Error(
              "Element type is invalid: expected a string (for built-in components) or a class/function (for composite components) but got: " + (a + "." + h)
            ), h = null;
        }
      return t = x(d, a, t, o), t.elementType = e, t.type = h, t.lanes = f, t._debugOwner = c, t;
    }
    function qc(e, t, a) {
      return t = xi(
        e.type,
        e.key,
        e.props,
        e._owner,
        t,
        a
      ), t._debugOwner = e._owner, t._debugStack = e._debugStack, t._debugTask = e._debugTask, t;
    }
    function Ni(e, t, a, c) {
      return e = x(7, e, c, t), e.lanes = a, e;
    }
    function Zo(e, t, a) {
      return e = x(6, e, null, t), e.lanes = a, e;
    }
    function $m(e) {
      var t = x(18, null, null, He);
      return t.stateNode = e, t;
    }
    function Td(e, t, a) {
      return t = x(
        4,
        e.children !== null ? e.children : [],
        e.key,
        t
      ), t.lanes = a, t.stateNode = {
        containerInfo: e.containerInfo,
        pendingChildren: null,
        implementation: e.implementation
      }, t;
    }
    function da(e, t) {
      if (typeof e == "object" && e !== null) {
        var a = C1.get(e);
        return a !== void 0 ? a : (t = {
          value: e,
          source: t,
          stack: Oe(t)
        }, C1.set(e, t), t);
      }
      return {
        value: e,
        source: t,
        stack: Oe(t)
      };
    }
    function Yn(e, t) {
      wc(), Ph[em++] = q0, Ph[em++] = lv, lv = e, q0 = t;
    }
    function km(e, t, a) {
      wc(), Vu[Zu++] = go, Vu[Zu++] = vo, Vu[Zu++] = xr, xr = e;
      var c = go;
      e = vo;
      var o = 32 - Fl(c) - 1;
      c &= ~(1 << o), a += 1;
      var f = 32 - Fl(t) + o;
      if (30 < f) {
        var d = o - o % 5;
        f = (c & (1 << d) - 1).toString(32), c >>= d, o -= d, go = 1 << 32 - Fl(t) + o | a << o | c, vo = f + e;
      } else
        go = 1 << f | a << o | c, vo = e;
    }
    function Ad(e) {
      wc(), e.return !== null && (Yn(e, 1), km(e, 1, 0));
    }
    function Od(e) {
      for (; e === lv; )
        lv = Ph[--em], Ph[em] = null, q0 = Ph[--em], Ph[em] = null;
      for (; e === xr; )
        xr = Vu[--Zu], Vu[Zu] = null, vo = Vu[--Zu], Vu[Zu] = null, go = Vu[--Zu], Vu[Zu] = null;
    }
    function Gp() {
      return wc(), xr !== null ? { id: go, overflow: vo } : null;
    }
    function Xp(e, t) {
      wc(), Vu[Zu++] = go, Vu[Zu++] = vo, Vu[Zu++] = xr, go = t.id, vo = t.overflow, xr = e;
    }
    function wc() {
      st || console.error(
        "Expected to be hydrating. This is a bug in React. Please file an issue."
      );
    }
    function Hi(e, t) {
      if (e.return === null) {
        if (lu === null)
          lu = {
            fiber: e,
            children: [],
            serverProps: void 0,
            serverTail: [],
            distanceFromLeaf: t
          };
        else {
          if (lu.fiber !== e)
            throw Error(
              "Saw multiple hydration diff roots in a pass. This is a bug in React."
            );
          lu.distanceFromLeaf > t && (lu.distanceFromLeaf = t);
        }
        return lu;
      }
      var a = Hi(
        e.return,
        t + 1
      ).children;
      return 0 < a.length && a[a.length - 1].fiber === e ? (a = a[a.length - 1], a.distanceFromLeaf > t && (a.distanceFromLeaf = t), a) : (t = {
        fiber: e,
        children: [],
        serverProps: void 0,
        serverTail: [],
        distanceFromLeaf: t
      }, a.push(t), t);
    }
    function Lp() {
      st && console.error(
        "We should not be hydrating here. This is a bug in React. Please file a bug."
      );
    }
    function na(e, t) {
      yi || (e = Hi(e, 0), e.serverProps = null, t !== null && (t = Cg(t), e.serverTail.push(t)));
    }
    function gn(e) {
      var t = 1 < arguments.length && arguments[1] !== void 0 ? arguments[1] : !1, a = "", c = lu;
      throw c !== null && (lu = null, a = Mm(c)), Rs(
        da(
          Error(
            "Hydration failed because the server rendered " + (t ? "text" : "HTML") + ` didn't match the client. As a result this tree will be regenerated on the client. This can happen if a SSR-ed Client Component used:

- A server/client branch \`if (typeof window !== 'undefined')\`.
- Variable input such as \`Date.now()\` or \`Math.random()\` which changes each time it's called.
- Date formatting in a user's locale which doesn't match the server.
- External changing data without sending a snapshot of it along with the HTML.
- Invalid HTML tag nesting.

It can also happen if the client has a browser extension installed which messes with the HTML before React loaded.

https://react.dev/link/hydration-mismatch` + a
          ),
          e
        )
      ), U1;
    }
    function Wm(e) {
      var t = e.stateNode, a = e.type, c = e.memoizedProps;
      switch (t[el] = e, t[Da] = c, Aa(a, c), a) {
        case "dialog":
          xe("cancel", t), xe("close", t);
          break;
        case "iframe":
        case "object":
        case "embed":
          xe("load", t);
          break;
        case "video":
        case "audio":
          for (a = 0; a < dp.length; a++)
            xe(dp[a], t);
          break;
        case "source":
          xe("error", t);
          break;
        case "img":
        case "image":
        case "link":
          xe("error", t), xe("load", t);
          break;
        case "details":
          xe("toggle", t);
          break;
        case "input":
          la("input", c), xe("invalid", t), ra(t, c), ud(
            t,
            c.value,
            c.defaultValue,
            c.checked,
            c.defaultChecked,
            c.type,
            c.name,
            !0
          );
          break;
        case "option":
          zp(t, c);
          break;
        case "select":
          la("select", c), xe("invalid", t), cd(t, c);
          break;
        case "textarea":
          la("textarea", c), xe("invalid", t), Ti(t, c), jo(
            t,
            c.value,
            c.defaultValue,
            c.children
          );
      }
      a = c.children, typeof a != "string" && typeof a != "number" && typeof a != "bigint" || t.textContent === "" + a || c.suppressHydrationWarning === !0 || Iy(t.textContent, a) ? (c.popover != null && (xe("beforetoggle", t), xe("toggle", t)), c.onScroll != null && xe("scroll", t), c.onScrollEnd != null && xe("scrollend", t), c.onClick != null && (t.onclick = yn), t = !0) : t = !1, t || gn(e, !0);
    }
    function Fm(e) {
      for (Ra = e.return; Ra; )
        switch (Ra.tag) {
          case 5:
          case 31:
          case 13:
            Ju = !1;
            return;
          case 27:
          case 3:
            Ju = !0;
            return;
          default:
            Ra = Ra.return;
        }
    }
    function ji(e) {
      if (e !== Ra) return !1;
      if (!st)
        return Fm(e), st = !0, !1;
      var t = e.tag, a;
      if ((a = t !== 3 && t !== 27) && ((a = t === 5) && (a = e.type, a = !(a !== "form" && a !== "button") || Af(e.type, e.memoizedProps)), a = !a), a && ll) {
        for (a = ll; a; ) {
          var c = Hi(e, 0), o = Cg(a);
          c.serverTail.push(o), a = o.type === "Suspense" ? Df(a) : an(a.nextSibling);
        }
        gn(e);
      }
      if (Fm(e), t === 13) {
        if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
          throw Error(
            "Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue."
          );
        ll = Df(e);
      } else if (t === 31) {
        if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e)
          throw Error(
            "Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue."
          );
        ll = Df(e);
      } else
        t === 27 ? (t = ll, oi(e.type) ? (e = bS, bS = null, ll = e) : ll = t) : ll = Ra ? an(e.stateNode.nextSibling) : null;
      return !0;
    }
    function Gc() {
      ll = Ra = null, yi = st = !1;
    }
    function Ds() {
      var e = Kf;
      return e !== null && (dn === null ? dn = e : dn.push.apply(
        dn,
        e
      ), Kf = null), e;
    }
    function Rs(e) {
      Kf === null ? Kf = [e] : Kf.push(e);
    }
    function Xc() {
      var e = lu;
      if (e !== null) {
        lu = null;
        for (var t = Mm(e); 0 < e.children.length; )
          e = e.children[0];
        oe(e.fiber, function() {
          console.error(
            `A tree hydrated but some attributes of the server rendered HTML didn't match the client properties. This won't be patched up. This can happen if a SSR-ed Client Component used:

- A server/client branch \`if (typeof window !== 'undefined')\`.
- Variable input such as \`Date.now()\` or \`Math.random()\` which changes each time it's called.
- Date formatting in a user's locale which doesn't match the server.
- External changing data without sending a snapshot of it along with the HTML.
- Invalid HTML tag nesting.

It can also happen if the client has a browser extension installed which messes with the HTML before React loaded.

%s%s`,
            "https://react.dev/link/hydration-mismatch",
            t
          );
        });
      }
    }
    function Jo() {
      tm = av = null, lm = !1;
    }
    function vn(e, t, a) {
      Xe(x1, t._currentValue, e), t._currentValue = a, Xe(N1, t._currentRenderer, e), t._currentRenderer !== void 0 && t._currentRenderer !== null && t._currentRenderer !== PS && console.error(
        "Detected multiple renderers concurrently rendering the same context provider. This is currently unsupported."
      ), t._currentRenderer = PS;
    }
    function qn(e, t) {
      e._currentValue = x1.current;
      var a = N1.current;
      pe(N1, t), e._currentRenderer = a, pe(x1, t);
    }
    function zd(e, t, a) {
      for (; e !== null; ) {
        var c = e.alternate;
        if ((e.childLanes & t) !== t ? (e.childLanes |= t, c !== null && (c.childLanes |= t)) : c !== null && (c.childLanes & t) !== t && (c.childLanes |= t), e === a) break;
        e = e.return;
      }
      e !== a && console.error(
        "Expected to find the propagation root when scheduling context work. This error is likely caused by a bug in React. Please file an issue."
      );
    }
    function lc(e, t, a, c) {
      var o = e.child;
      for (o !== null && (o.return = e); o !== null; ) {
        var f = o.dependencies;
        if (f !== null) {
          var d = o.child;
          f = f.firstContext;
          e: for (; f !== null; ) {
            var h = f;
            f = o;
            for (var y = 0; y < t.length; y++)
              if (h.context === t[y]) {
                f.lanes |= a, h = f.alternate, h !== null && (h.lanes |= a), zd(
                  f.return,
                  a,
                  e
                ), c || (d = null);
                break e;
              }
            f = h.next;
          }
        } else if (o.tag === 18) {
          if (d = o.return, d === null)
            throw Error(
              "We just came from a parent so we must have had a parent. This is a bug in React."
            );
          d.lanes |= a, f = d.alternate, f !== null && (f.lanes |= a), zd(
            d,
            a,
            e
          ), d = null;
        } else d = o.child;
        if (d !== null) d.return = o;
        else
          for (d = o; d !== null; ) {
            if (d === e) {
              d = null;
              break;
            }
            if (o = d.sibling, o !== null) {
              o.return = d.return, d = o;
              break;
            }
            d = d.return;
          }
        o = d;
      }
    }
    function wn(e, t, a, c) {
      e = null;
      for (var o = t, f = !1; o !== null; ) {
        if (!f) {
          if ((o.flags & 524288) !== 0) f = !0;
          else if ((o.flags & 262144) !== 0) break;
        }
        if (o.tag === 10) {
          var d = o.alternate;
          if (d === null)
            throw Error("Should have a current fiber. This is a bug in React.");
          if (d = d.memoizedProps, d !== null) {
            var h = o.type;
            on(o.pendingProps.value, d.value) || (e !== null ? e.push(h) : e = [h]);
          }
        } else if (o === di.current) {
          if (d = o.alternate, d === null)
            throw Error("Should have a current fiber. This is a bug in React.");
          d.memoizedState.memoizedState !== o.memoizedState.memoizedState && (e !== null ? e.push(gp) : e = [gp]);
        }
        o = o.return;
      }
      e !== null && lc(
        t,
        e,
        a,
        c
      ), t.flags |= 262144;
    }
    function Ko(e) {
      for (e = e.firstContext; e !== null; ) {
        if (!on(
          e.context._currentValue,
          e.memoizedValue
        ))
          return !0;
        e = e.next;
      }
      return !1;
    }
    function Lc(e) {
      av = e, tm = null, e = e.dependencies, e !== null && (e.firstContext = null);
    }
    function Et(e) {
      return lm && console.error(
        "Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo()."
      ), Im(av, e);
    }
    function _s(e, t) {
      return av === null && Lc(e), Im(e, t);
    }
    function Im(e, t) {
      var a = t._currentValue;
      if (t = { context: t, memoizedValue: a, next: null }, tm === null) {
        if (e === null)
          throw Error(
            "Context can only be read while React is rendering. In classes, you can read it in the render method or getDerivedStateFromProps. In function components, you can read it directly in the function body, but not inside Hooks like useReducer() or useMemo()."
          );
        tm = t, e.dependencies = {
          lanes: 0,
          firstContext: t,
          _debugThenableState: null
        }, e.flags |= 524288;
      } else tm = tm.next = t;
      return a;
    }
    function Dd() {
      return {
        controller: new $E(),
        data: /* @__PURE__ */ new Map(),
        refCount: 0
      };
    }
    function Bi(e) {
      e.controller.signal.aborted && console.warn(
        "A cache instance was retained after it was already freed. This likely indicates a bug in React."
      ), e.refCount++;
    }
    function Ms(e) {
      e.refCount--, 0 > e.refCount && console.warn(
        "A cache instance was released after it was already freed. This likely indicates a bug in React."
      ), e.refCount === 0 && kE(WE, function() {
        e.controller.abort();
      });
    }
    function pu(e, t, a) {
      (e & 127) !== 0 ? 0 > pi && (pi = Ql(), G0 = nv(t), H1 = t, a != null && (j1 = se(a)), (pt & (ea | uu)) !== sa && (Sl = !0, kf = w0), e = Of(), t = ju(), e !== am || t !== X0 ? am = -1.1 : t !== null && (kf = w0), jr = e, X0 = t) : (e & 4194048) !== 0 && 0 > Ku && (Ku = Ql(), L0 = nv(t), eb = t, a != null && (tb = se(a)), 0 > To) && (e = Of(), t = ju(), (e !== Ff || t !== Br) && (Ff = -1.1), Wf = e, Br = t);
    }
    function Qp(e) {
      if (0 > pi) {
        pi = Ql(), G0 = e._debugTask != null ? e._debugTask : null, (pt & (ea | uu)) !== sa && (kf = w0);
        var t = Of(), a = ju();
        t !== am || a !== X0 ? am = -1.1 : a !== null && (kf = w0), jr = t, X0 = a;
      }
      0 > Ku && (Ku = Ql(), L0 = e._debugTask != null ? e._debugTask : null, 0 > To) && (e = Of(), t = ju(), (e !== Ff || t !== Br) && (Ff = -1.1), Wf = e, Br = t);
    }
    function gu() {
      var e = Nr;
      return Nr = 0, e;
    }
    function $o(e) {
      var t = Nr;
      return Nr = e, t;
    }
    function ha(e) {
      var t = Nr;
      return Nr += e, t;
    }
    function Yi() {
      Ue = ze = -1.1;
    }
    function Ft() {
      var e = ze;
      return ze = -1.1, e;
    }
    function jl(e) {
      0 <= e && (ze = e);
    }
    function Sn() {
      var e = rl;
      return rl = -0, e;
    }
    function Za(e) {
      0 <= e && (rl = e);
    }
    function Ja() {
      var e = il;
      return il = null, e;
    }
    function bn() {
      var e = Sl;
      return Sl = !1, e;
    }
    function ac(e) {
      fn = Ql(), 0 > e.actualStartTime && (e.actualStartTime = fn);
    }
    function Rd(e) {
      if (0 <= fn) {
        var t = Ql() - fn;
        e.actualDuration += t, e.selfBaseDuration = t, fn = -1;
      }
    }
    function Cs(e) {
      if (0 <= fn) {
        var t = Ql() - fn;
        e.actualDuration += t, fn = -1;
      }
    }
    function ma() {
      if (0 <= fn) {
        var e = Ql(), t = e - fn;
        fn = -1, Nr += t, rl += t, Ue = e;
      }
    }
    function Vp(e) {
      il === null && (il = []), il.push(e), bo === null && (bo = []), bo.push(e);
    }
    function ol() {
      fn = Ql(), 0 > ze && (ze = fn);
    }
    function qi(e) {
      for (var t = e.child; t; )
        e.actualDuration += t.actualDuration, t = t.sibling;
    }
    function nc(e, t) {
      if (V0 === null) {
        var a = V0 = [];
        Y1 = 0, Yr = Fy(), nm = {
          status: "pending",
          value: void 0,
          then: function(c) {
            a.push(c);
          }
        };
      }
      return Y1++, t.then(Pm, Pm), t;
    }
    function Pm() {
      if (--Y1 === 0 && (-1 < Ku || (To = -1.1), V0 !== null)) {
        nm !== null && (nm.status = "fulfilled");
        var e = V0;
        V0 = null, Yr = 0, nm = null;
        for (var t = 0; t < e.length; t++) (0, e[t])();
      }
    }
    function _d(e, t) {
      var a = [], c = {
        status: "pending",
        value: null,
        reason: null,
        then: function(o) {
          a.push(o);
        }
      };
      return e.then(
        function() {
          c.status = "fulfilled", c.value = t;
          for (var o = 0; o < a.length; o++) (0, a[o])(t);
        },
        function(o) {
          for (c.status = "rejected", c.reason = o, o = 0; o < a.length; o++)
            (0, a[o])(void 0);
        }
      ), c;
    }
    function uc() {
      var e = qr.current;
      return e !== null ? e : Jt.pooledCache;
    }
    function ko(e, t) {
      t === null ? Xe(qr, qr.current, e) : Xe(qr, t.pool, e);
    }
    function ey() {
      var e = uc();
      return e === null ? null : { parent: Ll._currentValue, pool: e };
    }
    function Md() {
      return { didWarnAboutUncachedPromise: !1, thenables: [] };
    }
    function ty(e) {
      return e = e.status, e === "fulfilled" || e === "rejected";
    }
    function Ka(e, t, a) {
      G.actQueue !== null && (G.didUsePromise = !0);
      var c = e.thenables;
      if (a = c[a], a === void 0 ? c.push(t) : a !== t && (e.didWarnAboutUncachedPromise || (e.didWarnAboutUncachedPromise = !0, console.error(
        "A component was suspended by an uncached promise. Creating promises inside a Client Component or hook is not yet supported, except via a Suspense-compatible library or framework."
      )), t.then(yn, yn), t = a), t._debugInfo === void 0) {
        e = performance.now(), c = t.displayName;
        var o = {
          name: typeof c == "string" ? c : "Promise",
          start: e,
          end: e,
          value: t
        };
        t._debugInfo = [{ awaited: o }], t.status !== "fulfilled" && t.status !== "rejected" && (e = function() {
          o.end = performance.now();
        }, t.then(e, e));
      }
      switch (t.status) {
        case "fulfilled":
          return t.value;
        case "rejected":
          throw e = t.reason, Us(e), e;
        default:
          if (typeof t.status == "string")
            t.then(yn, yn);
          else {
            if (e = Jt, e !== null && 100 < e.shellSuspendCounter)
              throw Error(
                "An unknown Component is an async Client Component. Only Server Components can be async at the moment. This error is often caused by accidentally adding `'use client'` to a module that was originally written for the server."
              );
            e = t, e.status = "pending", e.then(
              function(f) {
                if (t.status === "pending") {
                  var d = t;
                  d.status = "fulfilled", d.value = f;
                }
              },
              function(f) {
                if (t.status === "pending") {
                  var d = t;
                  d.status = "rejected", d.reason = f;
                }
              }
            );
          }
          switch (t.status) {
            case "fulfilled":
              return t.value;
            case "rejected":
              throw e = t.reason, Us(e), e;
          }
          throw Gr = t, F0 = !0, um;
      }
    }
    function $a(e) {
      try {
        return tT(e);
      } catch (t) {
        throw t !== null && typeof t == "object" && typeof t.then == "function" ? (Gr = t, F0 = !0, um) : t;
      }
    }
    function wi() {
      if (Gr === null)
        throw Error(
          "Expected a suspended thenable. This is a bug in React. Please file an issue."
        );
      var e = Gr;
      return Gr = null, F0 = !1, e;
    }
    function Us(e) {
      if (e === um || e === dv)
        throw Error(
          "Hooks are not supported inside an async component. This error is often caused by accidentally adding `'use client'` to a module that was originally written for the server."
        );
    }
    function ml(e) {
      var t = et;
      return e != null && (et = t === null ? e : t.concat(e)), t;
    }
    function _a() {
      var e = et;
      if (e != null) {
        for (var t = e.length - 1; 0 <= t; t--)
          if (e[t].name != null) {
            var a = e[t].debugTask;
            if (a != null) return a;
          }
      }
      return null;
    }
    function ya(e, t, a) {
      for (var c = Object.keys(e.props), o = 0; o < c.length; o++) {
        var f = c[o];
        if (f !== "children" && f !== "key") {
          t === null && (t = qc(e, a.mode, 0), t._debugInfo = et, t.return = a), oe(
            t,
            function(d) {
              console.error(
                "Invalid prop `%s` supplied to `React.Fragment`. React.Fragment can only have `key` and `children` props.",
                d
              );
            },
            f
          );
          break;
        }
      }
    }
    function Gn(e) {
      var t = I0;
      return I0 += 1, cm === null && (cm = Md()), Ka(cm, e, t);
    }
    function Ma(e, t) {
      t = t.props.ref, e.ref = t !== void 0 ? t : null;
    }
    function Xn(e, t) {
      throw t.$$typeof === Gg ? Error(
        `A React Element from an older version of React was rendered. This is not supported. It can happen if:
- Multiple copies of the "react" package is used.
- A library pre-bundled an old copy of "react" or "react/jsx-runtime".
- A compiler tries to "inline" JSX instead of using the runtime.`
      ) : (e = Object.prototype.toString.call(t), Error(
        "Objects are not valid as a React child (found: " + (e === "[object Object]" ? "object with keys {" + Object.keys(t).join(", ") + "}" : e) + "). If you meant to render a collection of children, use an array instead."
      ));
    }
    function En(e, t) {
      var a = _a();
      a !== null ? a.run(
        Xn.bind(null, e, t)
      ) : Xn(e, t);
    }
    function ly(e, t) {
      var a = se(e) || "Component";
      Eb[a] || (Eb[a] = !0, t = t.displayName || t.name || "Component", e.tag === 3 ? console.error(
        `Functions are not valid as a React child. This may happen if you return %s instead of <%s /> from render. Or maybe you meant to call this function rather than return it.
  root.render(%s)`,
        t,
        t,
        t
      ) : console.error(
        `Functions are not valid as a React child. This may happen if you return %s instead of <%s /> from render. Or maybe you meant to call this function rather than return it.
  <%s>{%s}</%s>`,
        t,
        t,
        a,
        t,
        a
      ));
    }
    function Wo(e, t) {
      var a = _a();
      a !== null ? a.run(
        ly.bind(null, e, t)
      ) : ly(e, t);
    }
    function Cd(e, t) {
      var a = se(e) || "Component";
      Tb[a] || (Tb[a] = !0, t = String(t), e.tag === 3 ? console.error(
        `Symbols are not valid as a React child.
  root.render(%s)`,
        t
      ) : console.error(
        `Symbols are not valid as a React child.
  <%s>%s</%s>`,
        a,
        t,
        a
      ));
    }
    function xs(e, t) {
      var a = _a();
      a !== null ? a.run(
        Cd.bind(null, e, t)
      ) : Cd(e, t);
    }
    function Bl(e) {
      function t(b, T) {
        if (e) {
          var O = b.deletions;
          O === null ? (b.deletions = [T], b.flags |= 16) : O.push(T);
        }
      }
      function a(b, T) {
        if (!e) return null;
        for (; T !== null; )
          t(b, T), T = T.sibling;
        return null;
      }
      function c(b) {
        for (var T = /* @__PURE__ */ new Map(); b !== null; )
          b.key !== null ? T.set(b.key, b) : T.set(b.index, b), b = b.sibling;
        return T;
      }
      function o(b, T) {
        return b = yu(b, T), b.index = 0, b.sibling = null, b;
      }
      function f(b, T, O) {
        return b.index = O, e ? (O = b.alternate, O !== null ? (O = O.index, O < T ? (b.flags |= 67108866, T) : O) : (b.flags |= 67108866, T)) : (b.flags |= 1048576, T);
      }
      function d(b) {
        return e && b.alternate === null && (b.flags |= 67108866), b;
      }
      function h(b, T, O, J) {
        return T === null || T.tag !== 6 ? (T = Zo(
          O,
          b.mode,
          J
        ), T.return = b, T._debugOwner = b, T._debugTask = b._debugTask, T._debugInfo = et, T) : (T = o(T, O), T.return = b, T._debugInfo = et, T);
      }
      function y(b, T, O, J) {
        var ie = O.type;
        return ie === Uf ? (T = z(
          b,
          T,
          O.props.children,
          J,
          O.key
        ), ya(O, T, b), T) : T !== null && (T.elementType === ie || Zm(T, O) || typeof ie == "object" && ie !== null && ie.$$typeof === ca && $a(ie) === T.type) ? (T = o(T, O.props), Ma(T, O), T.return = b, T._debugOwner = O._owner, T._debugInfo = et, T) : (T = qc(O, b.mode, J), Ma(T, O), T.return = b, T._debugInfo = et, T);
      }
      function p(b, T, O, J) {
        return T === null || T.tag !== 4 || T.stateNode.containerInfo !== O.containerInfo || T.stateNode.implementation !== O.implementation ? (T = Td(O, b.mode, J), T.return = b, T._debugInfo = et, T) : (T = o(T, O.children || []), T.return = b, T._debugInfo = et, T);
      }
      function z(b, T, O, J, ie) {
        return T === null || T.tag !== 7 ? (T = Ni(
          O,
          b.mode,
          J,
          ie
        ), T.return = b, T._debugOwner = b, T._debugTask = b._debugTask, T._debugInfo = et, T) : (T = o(T, O), T.return = b, T._debugInfo = et, T);
      }
      function _(b, T, O) {
        if (typeof T == "string" && T !== "" || typeof T == "number" || typeof T == "bigint")
          return T = Zo(
            "" + T,
            b.mode,
            O
          ), T.return = b, T._debugOwner = b, T._debugTask = b._debugTask, T._debugInfo = et, T;
        if (typeof T == "object" && T !== null) {
          switch (T.$$typeof) {
            case Dn:
              return O = qc(
                T,
                b.mode,
                O
              ), Ma(O, T), O.return = b, b = ml(T._debugInfo), O._debugInfo = et, et = b, O;
            case si:
              return T = Td(
                T,
                b.mode,
                O
              ), T.return = b, T._debugInfo = et, T;
            case ca:
              var J = ml(T._debugInfo);
              return T = $a(T), b = _(b, T, O), et = J, b;
          }
          if (Al(T) || Ae(T))
            return O = Ni(
              T,
              b.mode,
              O,
              null
            ), O.return = b, O._debugOwner = b, O._debugTask = b._debugTask, b = ml(T._debugInfo), O._debugInfo = et, et = b, O;
          if (typeof T.then == "function")
            return J = ml(T._debugInfo), b = _(
              b,
              Gn(T),
              O
            ), et = J, b;
          if (T.$$typeof === Pn)
            return _(
              b,
              _s(b, T),
              O
            );
          En(b, T);
        }
        return typeof T == "function" && Wo(b, T), typeof T == "symbol" && xs(b, T), null;
      }
      function E(b, T, O, J) {
        var ie = T !== null ? T.key : null;
        if (typeof O == "string" && O !== "" || typeof O == "number" || typeof O == "bigint")
          return ie !== null ? null : h(b, T, "" + O, J);
        if (typeof O == "object" && O !== null) {
          switch (O.$$typeof) {
            case Dn:
              return O.key === ie ? (ie = ml(O._debugInfo), b = y(
                b,
                T,
                O,
                J
              ), et = ie, b) : null;
            case si:
              return O.key === ie ? p(b, T, O, J) : null;
            case ca:
              return ie = ml(O._debugInfo), O = $a(O), b = E(
                b,
                T,
                O,
                J
              ), et = ie, b;
          }
          if (Al(O) || Ae(O))
            return ie !== null ? null : (ie = ml(O._debugInfo), b = z(
              b,
              T,
              O,
              J,
              null
            ), et = ie, b);
          if (typeof O.then == "function")
            return ie = ml(O._debugInfo), b = E(
              b,
              T,
              Gn(O),
              J
            ), et = ie, b;
          if (O.$$typeof === Pn)
            return E(
              b,
              T,
              _s(b, O),
              J
            );
          En(b, O);
        }
        return typeof O == "function" && Wo(b, O), typeof O == "symbol" && xs(b, O), null;
      }
      function Y(b, T, O, J, ie) {
        if (typeof J == "string" && J !== "" || typeof J == "number" || typeof J == "bigint")
          return b = b.get(O) || null, h(T, b, "" + J, ie);
        if (typeof J == "object" && J !== null) {
          switch (J.$$typeof) {
            case Dn:
              return O = b.get(
                J.key === null ? O : J.key
              ) || null, b = ml(J._debugInfo), T = y(
                T,
                O,
                J,
                ie
              ), et = b, T;
            case si:
              return b = b.get(
                J.key === null ? O : J.key
              ) || null, p(T, b, J, ie);
            case ca:
              var we = ml(J._debugInfo);
              return J = $a(J), T = Y(
                b,
                T,
                O,
                J,
                ie
              ), et = we, T;
          }
          if (Al(J) || Ae(J))
            return O = b.get(O) || null, b = ml(J._debugInfo), T = z(
              T,
              O,
              J,
              ie,
              null
            ), et = b, T;
          if (typeof J.then == "function")
            return we = ml(J._debugInfo), T = Y(
              b,
              T,
              O,
              Gn(J),
              ie
            ), et = we, T;
          if (J.$$typeof === Pn)
            return Y(
              b,
              T,
              O,
              _s(T, J),
              ie
            );
          En(T, J);
        }
        return typeof J == "function" && Wo(T, J), typeof J == "symbol" && xs(T, J), null;
      }
      function ue(b, T, O, J) {
        if (typeof O != "object" || O === null) return J;
        switch (O.$$typeof) {
          case Dn:
          case si:
            Ne(b, T, O);
            var ie = O.key;
            if (typeof ie != "string") break;
            if (J === null) {
              J = /* @__PURE__ */ new Set(), J.add(ie);
              break;
            }
            if (!J.has(ie)) {
              J.add(ie);
              break;
            }
            oe(T, function() {
              console.error(
                "Encountered two children with the same key, `%s`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.",
                ie
              );
            });
            break;
          case ca:
            O = $a(O), ue(b, T, O, J);
        }
        return J;
      }
      function fe(b, T, O, J) {
        for (var ie = null, we = null, Te = null, ve = T, Fe = T = 0, al = null; ve !== null && Fe < O.length; Fe++) {
          ve.index > Fe ? (al = ve, ve = null) : al = ve.sibling;
          var xl = E(
            b,
            ve,
            O[Fe],
            J
          );
          if (xl === null) {
            ve === null && (ve = al);
            break;
          }
          ie = ue(
            b,
            xl,
            O[Fe],
            ie
          ), e && ve && xl.alternate === null && t(b, ve), T = f(xl, T, Fe), Te === null ? we = xl : Te.sibling = xl, Te = xl, ve = al;
        }
        if (Fe === O.length)
          return a(b, ve), st && Yn(b, Fe), we;
        if (ve === null) {
          for (; Fe < O.length; Fe++)
            ve = _(b, O[Fe], J), ve !== null && (ie = ue(
              b,
              ve,
              O[Fe],
              ie
            ), T = f(
              ve,
              T,
              Fe
            ), Te === null ? we = ve : Te.sibling = ve, Te = ve);
          return st && Yn(b, Fe), we;
        }
        for (ve = c(ve); Fe < O.length; Fe++)
          al = Y(
            ve,
            b,
            Fe,
            O[Fe],
            J
          ), al !== null && (ie = ue(
            b,
            al,
            O[Fe],
            ie
          ), e && al.alternate !== null && ve.delete(
            al.key === null ? Fe : al.key
          ), T = f(
            al,
            T,
            Fe
          ), Te === null ? we = al : Te.sibling = al, Te = al);
        return e && ve.forEach(function(Co) {
          return t(b, Co);
        }), st && Yn(b, Fe), we;
      }
      function Wt(b, T, O, J) {
        if (O == null)
          throw Error("An iterable object provided no iterator.");
        for (var ie = null, we = null, Te = T, ve = T = 0, Fe = null, al = null, xl = O.next(); Te !== null && !xl.done; ve++, xl = O.next()) {
          Te.index > ve ? (Fe = Te, Te = null) : Fe = Te.sibling;
          var Co = E(b, Te, xl.value, J);
          if (Co === null) {
            Te === null && (Te = Fe);
            break;
          }
          al = ue(
            b,
            Co,
            xl.value,
            al
          ), e && Te && Co.alternate === null && t(b, Te), T = f(Co, T, ve), we === null ? ie = Co : we.sibling = Co, we = Co, Te = Fe;
        }
        if (xl.done)
          return a(b, Te), st && Yn(b, ve), ie;
        if (Te === null) {
          for (; !xl.done; ve++, xl = O.next())
            Te = _(b, xl.value, J), Te !== null && (al = ue(
              b,
              Te,
              xl.value,
              al
            ), T = f(
              Te,
              T,
              ve
            ), we === null ? ie = Te : we.sibling = Te, we = Te);
          return st && Yn(b, ve), ie;
        }
        for (Te = c(Te); !xl.done; ve++, xl = O.next())
          Fe = Y(
            Te,
            b,
            ve,
            xl.value,
            J
          ), Fe !== null && (al = ue(
            b,
            Fe,
            xl.value,
            al
          ), e && Fe.alternate !== null && Te.delete(
            Fe.key === null ? ve : Fe.key
          ), T = f(
            Fe,
            T,
            ve
          ), we === null ? ie = Fe : we.sibling = Fe, we = Fe);
        return e && Te.forEach(function(zT) {
          return t(b, zT);
        }), st && Yn(b, ve), ie;
      }
      function dt(b, T, O, J) {
        if (typeof O == "object" && O !== null && O.type === Uf && O.key === null && (ya(O, null, b), O = O.props.children), typeof O == "object" && O !== null) {
          switch (O.$$typeof) {
            case Dn:
              var ie = ml(O._debugInfo);
              e: {
                for (var we = O.key; T !== null; ) {
                  if (T.key === we) {
                    if (we = O.type, we === Uf) {
                      if (T.tag === 7) {
                        a(
                          b,
                          T.sibling
                        ), J = o(
                          T,
                          O.props.children
                        ), J.return = b, J._debugOwner = O._owner, J._debugInfo = et, ya(O, J, b), b = J;
                        break e;
                      }
                    } else if (T.elementType === we || Zm(
                      T,
                      O
                    ) || typeof we == "object" && we !== null && we.$$typeof === ca && $a(we) === T.type) {
                      a(
                        b,
                        T.sibling
                      ), J = o(T, O.props), Ma(J, O), J.return = b, J._debugOwner = O._owner, J._debugInfo = et, b = J;
                      break e;
                    }
                    a(b, T);
                    break;
                  } else t(b, T);
                  T = T.sibling;
                }
                O.type === Uf ? (J = Ni(
                  O.props.children,
                  b.mode,
                  J,
                  O.key
                ), J.return = b, J._debugOwner = b, J._debugTask = b._debugTask, J._debugInfo = et, ya(O, J, b), b = J) : (J = qc(
                  O,
                  b.mode,
                  J
                ), Ma(J, O), J.return = b, J._debugInfo = et, b = J);
              }
              return b = d(b), et = ie, b;
            case si:
              e: {
                for (ie = O, O = ie.key; T !== null; ) {
                  if (T.key === O)
                    if (T.tag === 4 && T.stateNode.containerInfo === ie.containerInfo && T.stateNode.implementation === ie.implementation) {
                      a(
                        b,
                        T.sibling
                      ), J = o(
                        T,
                        ie.children || []
                      ), J.return = b, b = J;
                      break e;
                    } else {
                      a(b, T);
                      break;
                    }
                  else t(b, T);
                  T = T.sibling;
                }
                J = Td(
                  ie,
                  b.mode,
                  J
                ), J.return = b, b = J;
              }
              return d(b);
            case ca:
              return ie = ml(O._debugInfo), O = $a(O), b = dt(
                b,
                T,
                O,
                J
              ), et = ie, b;
          }
          if (Al(O))
            return ie = ml(O._debugInfo), b = fe(
              b,
              T,
              O,
              J
            ), et = ie, b;
          if (Ae(O)) {
            if (ie = ml(O._debugInfo), we = Ae(O), typeof we != "function")
              throw Error(
                "An object is not an iterable. This error is likely caused by a bug in React. Please file an issue."
              );
            var Te = we.call(O);
            return Te === O ? (b.tag !== 0 || Object.prototype.toString.call(b.type) !== "[object GeneratorFunction]" || Object.prototype.toString.call(Te) !== "[object Generator]") && (Sb || console.error(
              "Using Iterators as children is unsupported and will likely yield unexpected results because enumerating a generator mutates it. You may convert it to an array with `Array.from()` or the `[...spread]` operator before rendering. You can also use an Iterable that can iterate multiple times over the same items."
            ), Sb = !0) : O.entries !== we || X1 || (console.error(
              "Using Maps as children is not supported. Use an array of keyed ReactElements instead."
            ), X1 = !0), b = Wt(
              b,
              T,
              Te,
              J
            ), et = ie, b;
          }
          if (typeof O.then == "function")
            return ie = ml(O._debugInfo), b = dt(
              b,
              T,
              Gn(O),
              J
            ), et = ie, b;
          if (O.$$typeof === Pn)
            return dt(
              b,
              T,
              _s(b, O),
              J
            );
          En(b, O);
        }
        return typeof O == "string" && O !== "" || typeof O == "number" || typeof O == "bigint" ? (ie = "" + O, T !== null && T.tag === 6 ? (a(
          b,
          T.sibling
        ), J = o(T, ie), J.return = b, b = J) : (a(b, T), J = Zo(
          ie,
          b.mode,
          J
        ), J.return = b, J._debugOwner = b, J._debugTask = b._debugTask, J._debugInfo = et, b = J), d(b)) : (typeof O == "function" && Wo(b, O), typeof O == "symbol" && xs(b, O), a(b, T));
      }
      return function(b, T, O, J) {
        var ie = et;
        et = null;
        try {
          I0 = 0;
          var we = dt(
            b,
            T,
            O,
            J
          );
          return cm = null, we;
        } catch (al) {
          if (al === um || al === dv) throw al;
          var Te = x(29, al, null, b.mode);
          Te.lanes = J, Te.return = b;
          var ve = Te._debugInfo = et;
          if (Te._debugOwner = b._debugOwner, Te._debugTask = b._debugTask, ve != null) {
            for (var Fe = ve.length - 1; 0 <= Fe; Fe--)
              if (typeof ve[Fe].stack == "string") {
                Te._debugOwner = ve[Fe], Te._debugTask = ve[Fe].debugTask;
                break;
              }
          }
          return Te;
        } finally {
          et = ie;
        }
      };
    }
    function Lt(e, t) {
      var a = Al(e);
      return e = !a && typeof Ae(e) == "function", a || e ? (a = a ? "array" : "iterable", console.error(
        "A nested %s was passed to row #%s in <SuspenseList />. Wrap it in an additional SuspenseList to configure its revealOrder: <SuspenseList revealOrder=...> ... <SuspenseList revealOrder=...>{%s}</SuspenseList> ... </SuspenseList>",
        a,
        t,
        a
      ), !1) : !0;
    }
    function ot(e) {
      e.updateQueue = {
        baseState: e.memoizedState,
        firstBaseUpdate: null,
        lastBaseUpdate: null,
        shared: { pending: null, lanes: 0, hiddenCallbacks: null },
        callbacks: null
      };
    }
    function vu(e, t) {
      e = e.updateQueue, t.updateQueue === e && (t.updateQueue = {
        baseState: e.baseState,
        firstBaseUpdate: e.firstBaseUpdate,
        lastBaseUpdate: e.lastBaseUpdate,
        shared: e.shared,
        callbacks: null
      });
    }
    function Dl(e) {
      return {
        lane: e,
        tag: Ob,
        payload: null,
        callback: null,
        next: null
      };
    }
    function Su(e, t, a) {
      var c = e.updateQueue;
      if (c === null) return null;
      if (c = c.shared, Q1 === c && !Rb) {
        var o = se(e);
        console.error(
          `An update (setState, replaceState, or forceUpdate) was scheduled from inside an update function. Update functions should be pure, with zero side-effects. Consider using componentDidUpdate or a callback.

Please update the following component: %s`,
          o
        ), Rb = !0;
      }
      return (pt & ea) !== sa ? (o = c.pending, o === null ? t.next = t : (t.next = o.next, o.next = t), c.pending = t, t = zs(e), Vm(e, null, a), t) : (Vo(e, c, t, a), zs(e));
    }
    function Tn(e, t, a) {
      if (t = t.updateQueue, t !== null && (t = t.shared, (a & 4194048) !== 0)) {
        var c = t.lanes;
        c &= e.pendingLanes, a |= c, t.lanes = a, ms(e, a);
      }
    }
    function Ns(e, t) {
      var a = e.updateQueue, c = e.alternate;
      if (c !== null && (c = c.updateQueue, a === c)) {
        var o = null, f = null;
        if (a = a.firstBaseUpdate, a !== null) {
          do {
            var d = {
              lane: a.lane,
              tag: a.tag,
              payload: a.payload,
              callback: null,
              next: null
            };
            f === null ? o = f = d : f = f.next = d, a = a.next;
          } while (a !== null);
          f === null ? o = f = t : f = f.next = t;
        } else o = f = t;
        a = {
          baseState: c.baseState,
          firstBaseUpdate: o,
          lastBaseUpdate: f,
          shared: c.shared,
          callbacks: c.callbacks
        }, e.updateQueue = a;
        return;
      }
      e = a.lastBaseUpdate, e === null ? a.firstBaseUpdate = t : e.next = t, a.lastBaseUpdate = t;
    }
    function Fo() {
      if (V1) {
        var e = nm;
        if (e !== null) throw e;
      }
    }
    function bu(e, t, a, c) {
      V1 = !1;
      var o = e.updateQueue;
      If = !1, Q1 = o.shared;
      var f = o.firstBaseUpdate, d = o.lastBaseUpdate, h = o.shared.pending;
      if (h !== null) {
        o.shared.pending = null;
        var y = h, p = y.next;
        y.next = null, d === null ? f = p : d.next = p, d = y;
        var z = e.alternate;
        z !== null && (z = z.updateQueue, h = z.lastBaseUpdate, h !== d && (h === null ? z.firstBaseUpdate = p : h.next = p, z.lastBaseUpdate = y));
      }
      if (f !== null) {
        var _ = o.baseState;
        d = 0, z = p = y = null, h = f;
        do {
          var E = h.lane & -536870913, Y = E !== h.lane;
          if (Y ? (tt & E) === E : (c & E) === E) {
            E !== 0 && E === Yr && (V1 = !0), z !== null && (z = z.next = {
              lane: 0,
              tag: h.tag,
              payload: h.payload,
              callback: null,
              next: null
            });
            e: {
              E = e;
              var ue = h, fe = t, Wt = a;
              switch (ue.tag) {
                case zb:
                  if (ue = ue.payload, typeof ue == "function") {
                    lm = !0;
                    var dt = ue.call(
                      Wt,
                      _,
                      fe
                    );
                    if (E.mode & Ba) {
                      de(!0);
                      try {
                        ue.call(Wt, _, fe);
                      } finally {
                        de(!1);
                      }
                    }
                    lm = !1, _ = dt;
                    break e;
                  }
                  _ = ue;
                  break e;
                case L1:
                  E.flags = E.flags & -65537 | 128;
                case Ob:
                  if (dt = ue.payload, typeof dt == "function") {
                    if (lm = !0, ue = dt.call(
                      Wt,
                      _,
                      fe
                    ), E.mode & Ba) {
                      de(!0);
                      try {
                        dt.call(Wt, _, fe);
                      } finally {
                        de(!1);
                      }
                    }
                    lm = !1;
                  } else ue = dt;
                  if (ue == null) break e;
                  _ = Ie({}, _, ue);
                  break e;
                case Db:
                  If = !0;
              }
            }
            E = h.callback, E !== null && (e.flags |= 64, Y && (e.flags |= 8192), Y = o.callbacks, Y === null ? o.callbacks = [E] : Y.push(E));
          } else
            Y = {
              lane: E,
              tag: h.tag,
              payload: h.payload,
              callback: h.callback,
              next: null
            }, z === null ? (p = z = Y, y = _) : z = z.next = Y, d |= E;
          if (h = h.next, h === null) {
            if (h = o.shared.pending, h === null)
              break;
            Y = h, h = Y.next, Y.next = null, o.lastBaseUpdate = Y, o.shared.pending = null;
          }
        } while (!0);
        z === null && (y = _), o.baseState = y, o.firstBaseUpdate = p, o.lastBaseUpdate = z, f === null && (o.shared.lanes = 0), ts |= d, e.lanes = d, e.memoizedState = _;
      }
      Q1 = null;
    }
    function Qc(e, t) {
      if (typeof e != "function")
        throw Error(
          "Invalid argument passed as callback. Expected a function. Instead received: " + e
        );
      e.call(t);
    }
    function ay(e, t) {
      var a = e.shared.hiddenCallbacks;
      if (a !== null)
        for (e.shared.hiddenCallbacks = null, e = 0; e < a.length; e++)
          Qc(a[e], t);
    }
    function Io(e, t) {
      var a = e.callbacks;
      if (a !== null)
        for (e.callbacks = null, e = 0; e < a.length; e++)
          Qc(a[e], t);
    }
    function Ud(e, t) {
      var a = vi;
      Xe(mv, a, e), Xe(im, t, e), vi = a | t.baseLanes;
    }
    function cc(e) {
      Xe(mv, vi, e), Xe(
        im,
        im.current,
        e
      );
    }
    function Ln(e) {
      vi = mv.current, pe(im, e), pe(mv, e);
    }
    function pa(e) {
      var t = e.alternate;
      Xe(
        Ul,
        Ul.current & om,
        e
      ), Xe(au, e, e), $u === null && (t === null || im.current !== null || t.memoizedState !== null) && ($u = e);
    }
    function Qn(e) {
      Xe(Ul, Ul.current, e), Xe(au, e, e), $u === null && ($u = e);
    }
    function xd(e) {
      e.tag === 22 ? (Xe(Ul, Ul.current, e), Xe(au, e, e), $u === null && ($u = e)) : Eu(e);
    }
    function Eu(e) {
      Xe(Ul, Ul.current, e), Xe(
        au,
        au.current,
        e
      );
    }
    function Yl(e) {
      pe(au, e), $u === e && ($u = null), pe(Ul, e);
    }
    function Gi(e) {
      for (var t = e; t !== null; ) {
        if (t.tag === 13) {
          var a = t.memoizedState;
          if (a !== null && (a = a.dehydrated, a === null || yr(a) || e0(a)))
            return t;
        } else if (t.tag === 19 && (t.memoizedProps.revealOrder === "forwards" || t.memoizedProps.revealOrder === "backwards" || t.memoizedProps.revealOrder === "unstable_legacy-backwards" || t.memoizedProps.revealOrder === "together")) {
          if ((t.flags & 128) !== 0) return t;
        } else if (t.child !== null) {
          t.child.return = t, t = t.child;
          continue;
        }
        if (t === e) break;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e) return null;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
      return null;
    }
    function Ye() {
      var e = q;
      Wu === null ? Wu = [e] : Wu.push(e);
    }
    function k() {
      var e = q;
      if (Wu !== null && (zo++, Wu[zo] !== e)) {
        var t = se(qe);
        if (!_b.has(t) && (_b.add(t), Wu !== null)) {
          for (var a = "", c = 0; c <= zo; c++) {
            var o = Wu[c], f = c === zo ? e : o;
            for (o = c + 1 + ". " + o; 30 > o.length; )
              o += " ";
            o += f + `
`, a += o;
          }
          console.error(
            `React has detected a change in the order of Hooks called by %s. This will lead to bugs and errors if not fixed. For more information, read the Rules of Hooks: https://react.dev/link/rules-of-hooks

   Previous render            Next render
   ------------------------------------------------------
%s   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`,
            t,
            a
          );
        }
      }
    }
    function ic(e) {
      e == null || Al(e) || console.error(
        "%s received a final argument that is not an array (instead, received `%s`). When specified, the final argument must be an array.",
        q,
        typeof e
      );
    }
    function Hs() {
      var e = se(qe);
      Cb.has(e) || (Cb.add(e), console.error(
        "ReactDOM.useFormState has been renamed to React.useActionState. Please update %s to use React.useActionState.",
        e
      ));
    }
    function fl() {
      throw Error(
        `Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://react.dev/link/invalid-hook-call for tips about how to debug and fix this problem.`
      );
    }
    function ny(e, t) {
      if (tp) return !1;
      if (t === null)
        return console.error(
          "%s received a final argument during this render, but not during the previous render. Even though the final argument is optional, its type cannot change between renders.",
          q
        ), !1;
      e.length !== t.length && console.error(
        `The final argument passed to %s changed size between renders. The order and size of this array must remain constant.

Previous: %s
Incoming: %s`,
        q,
        "[" + t.join(", ") + "]",
        "[" + e.join(", ") + "]"
      );
      for (var a = 0; a < t.length && a < e.length; a++)
        if (!on(e[a], t[a])) return !1;
      return !0;
    }
    function uy(e, t, a, c, o, f) {
      Ao = f, qe = t, Wu = e !== null ? e._debugHookTypes : null, zo = -1, tp = e !== null && e.type !== t.type, (Object.prototype.toString.call(a) === "[object AsyncFunction]" || Object.prototype.toString.call(a) === "[object AsyncGeneratorFunction]") && (f = se(qe), Z1.has(f) || (Z1.add(f), console.error(
        "%s is an async Client Component. Only Server Components can be async at the moment. This error is often caused by accidentally adding `'use client'` to a module that was originally written for the server.",
        f === null ? "An unknown Component" : "<" + f + ">"
      ))), t.memoizedState = null, t.updateQueue = null, t.lanes = 0, G.H = e !== null && e.memoizedState !== null ? K1 : Wu !== null ? Ub : J1, Lr = f = (t.mode & Ba) !== He;
      var d = q1(a, c, o);
      if (Lr = !1, sm && (d = js(
        t,
        a,
        c,
        o
      )), f) {
        de(!0);
        try {
          d = js(
            t,
            a,
            c,
            o
          );
        } finally {
          de(!1);
        }
      }
      return yl(e, t), d;
    }
    function yl(e, t) {
      t._debugHookTypes = Wu, t.dependencies === null ? Oo !== null && (t.dependencies = {
        lanes: 0,
        firstContext: null,
        _debugThenableState: Oo
      }) : t.dependencies._debugThenableState = Oo, G.H = lp;
      var a = Zt !== null && Zt.next !== null;
      if (Ao = 0, Wu = q = Vl = Zt = qe = null, zo = -1, e !== null && (e.flags & 65011712) !== (t.flags & 65011712) && console.error(
        "Internal React error: Expected static flag was missing. Please notify the React team."
      ), pv = !1, ep = 0, Oo = null, a)
        throw Error(
          "Rendered fewer hooks than expected. This may be caused by an accidental early return statement."
        );
      e === null || Zl || (e = e.dependencies, e !== null && Ko(e) && (Zl = !0)), F0 ? (F0 = !1, e = !0) : e = !1, e && (t = se(t) || "Unknown", Mb.has(t) || Z1.has(t) || (Mb.add(t), console.error(
        "`use` was called from inside a try/catch block. This is not allowed and can lead to unexpected behavior. To handle errors triggered by `use`, wrap your component in a error boundary."
      )));
    }
    function js(e, t, a, c) {
      qe = e;
      var o = 0;
      do {
        if (sm && (Oo = null), ep = 0, sm = !1, o >= aT)
          throw Error(
            "Too many re-renders. React limits the number of renders to prevent an infinite loop."
          );
        if (o += 1, tp = !1, Vl = Zt = null, e.updateQueue != null) {
          var f = e.updateQueue;
          f.lastEffect = null, f.events = null, f.stores = null, f.memoCache != null && (f.memoCache.index = 0);
        }
        zo = -1, G.H = xb, f = q1(t, a, c);
      } while (sm);
      return f;
    }
    function Bs() {
      var e = G.H, t = e.useState()[0];
      return t = typeof t.then == "function" ? ws(t) : t, e = e.useState()[0], (Zt !== null ? Zt.memoizedState : null) !== e && (qe.flags |= 1024), t;
    }
    function Xi() {
      var e = gv !== 0;
      return gv = 0, e;
    }
    function Ys(e, t, a) {
      t.updateQueue = e.updateQueue, t.flags = (t.mode & Tc) !== He ? t.flags & -402655237 : t.flags & -2053, e.lanes &= ~a;
    }
    function Vc(e) {
      if (pv) {
        for (e = e.memoizedState; e !== null; ) {
          var t = e.queue;
          t !== null && (t.pending = null), e = e.next;
        }
        pv = !1;
      }
      Ao = 0, Wu = Vl = Zt = qe = null, zo = -1, q = null, sm = !1, ep = gv = 0, Oo = null;
    }
    function El() {
      var e = {
        memoizedState: null,
        baseState: null,
        baseQueue: null,
        queue: null,
        next: null
      };
      return Vl === null ? qe.memoizedState = Vl = e : Vl = Vl.next = e, Vl;
    }
    function Dt() {
      if (Zt === null) {
        var e = qe.alternate;
        e = e !== null ? e.memoizedState : null;
      } else e = Zt.next;
      var t = Vl === null ? qe.memoizedState : Vl.next;
      if (t !== null)
        Vl = t, Zt = e;
      else {
        if (e === null)
          throw qe.alternate === null ? Error(
            "Update hook called on initial render. This is likely a bug in React. Please file an issue."
          ) : Error("Rendered more hooks than during the previous render.");
        Zt = e, e = {
          memoizedState: Zt.memoizedState,
          baseState: Zt.baseState,
          baseQueue: Zt.baseQueue,
          queue: Zt.queue,
          next: null
        }, Vl === null ? qe.memoizedState = Vl = e : Vl = Vl.next = e;
      }
      return Vl;
    }
    function qs() {
      return { lastEffect: null, events: null, stores: null, memoCache: null };
    }
    function ws(e) {
      var t = ep;
      return ep += 1, Oo === null && (Oo = Md()), e = Ka(Oo, e, t), t = qe, (Vl === null ? t.memoizedState : Vl.next) === null && (t = t.alternate, G.H = t !== null && t.memoizedState !== null ? K1 : J1), e;
    }
    function oc(e) {
      if (e !== null && typeof e == "object") {
        if (typeof e.then == "function") return ws(e);
        if (e.$$typeof === Pn) return Et(e);
      }
      throw Error("An unsupported type was passed to use(): " + String(e));
    }
    function ka(e) {
      var t = null, a = qe.updateQueue;
      if (a !== null && (t = a.memoCache), t == null) {
        var c = qe.alternate;
        c !== null && (c = c.updateQueue, c !== null && (c = c.memoCache, c != null && (t = {
          data: c.data.map(function(o) {
            return o.slice();
          }),
          index: 0
        })));
      }
      if (t == null && (t = { data: [], index: 0 }), a === null && (a = qs(), qe.updateQueue = a), a.memoCache = t, a = t.data[t.index], a === void 0 || tp)
        for (a = t.data[t.index] = Array(e), c = 0; c < e; c++)
          a[c] = r1;
      else
        a.length !== e && console.error(
          "Expected a constant size argument for each invocation of useMemoCache. The previous cache was allocated with size %s but size %s was requested.",
          a.length,
          e
        );
      return t.index++, a;
    }
    function Wa(e, t) {
      return typeof t == "function" ? t(e) : t;
    }
    function Po(e, t, a) {
      var c = El();
      if (a !== void 0) {
        var o = a(t);
        if (Lr) {
          de(!0);
          try {
            a(t);
          } finally {
            de(!1);
          }
        }
      } else o = t;
      return c.memoizedState = c.baseState = o, e = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: e,
        lastRenderedState: o
      }, c.queue = e, e = e.dispatch = c1.bind(
        null,
        qe,
        e
      ), [c.memoizedState, e];
    }
    function Li(e) {
      var t = Dt();
      return Zc(t, Zt, e);
    }
    function Zc(e, t, a) {
      var c = e.queue;
      if (c === null)
        throw Error(
          "Should have a queue. You are likely calling Hooks conditionally, which is not allowed. (https://react.dev/link/invalid-hook-call)"
        );
      c.lastRenderedReducer = a;
      var o = e.baseQueue, f = c.pending;
      if (f !== null) {
        if (o !== null) {
          var d = o.next;
          o.next = f.next, f.next = d;
        }
        t.baseQueue !== o && console.error(
          "Internal error: Expected work-in-progress queue to be a clone. This is a bug in React."
        ), t.baseQueue = o = f, c.pending = null;
      }
      if (f = e.baseState, o === null) e.memoizedState = f;
      else {
        t = o.next;
        var h = d = null, y = null, p = t, z = !1;
        do {
          var _ = p.lane & -536870913;
          if (_ !== p.lane ? (tt & _) === _ : (Ao & _) === _) {
            var E = p.revertLane;
            if (E === 0)
              y !== null && (y = y.next = {
                lane: 0,
                revertLane: 0,
                gesture: null,
                action: p.action,
                hasEagerState: p.hasEagerState,
                eagerState: p.eagerState,
                next: null
              }), _ === Yr && (z = !0);
            else if ((Ao & E) === E) {
              p = p.next, E === Yr && (z = !0);
              continue;
            } else
              _ = {
                lane: 0,
                revertLane: p.revertLane,
                gesture: null,
                action: p.action,
                hasEagerState: p.hasEagerState,
                eagerState: p.eagerState,
                next: null
              }, y === null ? (h = y = _, d = f) : y = y.next = _, qe.lanes |= E, ts |= E;
            _ = p.action, Lr && a(f, _), f = p.hasEagerState ? p.eagerState : a(f, _);
          } else
            E = {
              lane: _,
              revertLane: p.revertLane,
              gesture: p.gesture,
              action: p.action,
              hasEagerState: p.hasEagerState,
              eagerState: p.eagerState,
              next: null
            }, y === null ? (h = y = E, d = f) : y = y.next = E, qe.lanes |= _, ts |= _;
          p = p.next;
        } while (p !== null && p !== t);
        if (y === null ? d = f : y.next = h, !on(f, e.memoizedState) && (Zl = !0, z && (a = nm, a !== null)))
          throw a;
        e.memoizedState = f, e.baseState = d, e.baseQueue = y, c.lastRenderedState = f;
      }
      return o === null && (c.lanes = 0), [e.memoizedState, c.dispatch];
    }
    function Qi(e) {
      var t = Dt(), a = t.queue;
      if (a === null)
        throw Error(
          "Should have a queue. You are likely calling Hooks conditionally, which is not allowed. (https://react.dev/link/invalid-hook-call)"
        );
      a.lastRenderedReducer = e;
      var c = a.dispatch, o = a.pending, f = t.memoizedState;
      if (o !== null) {
        a.pending = null;
        var d = o = o.next;
        do
          f = e(f, d.action), d = d.next;
        while (d !== o);
        on(f, t.memoizedState) || (Zl = !0), t.memoizedState = f, t.baseQueue === null && (t.baseState = f), a.lastRenderedState = f;
      }
      return [f, c];
    }
    function ef(e, t, a) {
      var c = qe, o = El();
      if (st) {
        if (a === void 0)
          throw Error(
            "Missing getServerSnapshot, which is required for server-rendered content. Will revert to client rendering."
          );
        var f = a();
        fm || f === a() || (console.error(
          "The result of getServerSnapshot should be cached to avoid an infinite loop"
        ), fm = !0);
      } else {
        if (f = t(), fm || (a = t(), on(f, a) || (console.error(
          "The result of getSnapshot should be cached to avoid an infinite loop"
        ), fm = !0)), Jt === null)
          throw Error(
            "Expected a work-in-progress root. This is a bug in React. Please file an issue."
          );
        (tt & 127) !== 0 || cy(c, t, f);
      }
      return o.memoizedState = f, a = { value: f, getSnapshot: t }, o.queue = a, Ji(
        Jc.bind(null, c, a, e),
        [e]
      ), c.flags |= 2048, Tu(
        ku | rn,
        { destroy: void 0 },
        iy.bind(
          null,
          c,
          a,
          f,
          t
        ),
        null
      ), f;
    }
    function Vi(e, t, a) {
      var c = qe, o = Dt(), f = st;
      if (f) {
        if (a === void 0)
          throw Error(
            "Missing getServerSnapshot, which is required for server-rendered content. Will revert to client rendering."
          );
        a = a();
      } else if (a = t(), !fm) {
        var d = t();
        on(a, d) || (console.error(
          "The result of getSnapshot should be cached to avoid an infinite loop"
        ), fm = !0);
      }
      (d = !on(
        (Zt || o).memoizedState,
        a
      )) && (o.memoizedState = a, Zl = !0), o = o.queue;
      var h = Jc.bind(null, c, o, e);
      if (Rl(2048, rn, h, [e]), o.getSnapshot !== t || d || Vl !== null && Vl.memoizedState.tag & ku) {
        if (c.flags |= 2048, Tu(
          ku | rn,
          { destroy: void 0 },
          iy.bind(
            null,
            c,
            o,
            a,
            t
          ),
          null
        ), Jt === null)
          throw Error(
            "Expected a work-in-progress root. This is a bug in React. Please file an issue."
          );
        f || (Ao & 127) !== 0 || cy(c, t, a);
      }
      return a;
    }
    function cy(e, t, a) {
      e.flags |= 16384, e = { getSnapshot: t, value: a }, t = qe.updateQueue, t === null ? (t = qs(), qe.updateQueue = t, t.stores = [e]) : (a = t.stores, a === null ? t.stores = [e] : a.push(e));
    }
    function iy(e, t, a, c) {
      t.value = a, t.getSnapshot = c, Kc(t) && oy(e);
    }
    function Jc(e, t, a) {
      return a(function() {
        Kc(t) && (pu(2, "updateSyncExternalStore()", e), oy(e));
      });
    }
    function Kc(e) {
      var t = e.getSnapshot;
      e = e.value;
      try {
        var a = t();
        return !on(e, a);
      } catch {
        return !0;
      }
    }
    function oy(e) {
      var t = aa(e, 2);
      t !== null && je(t, e, 2);
    }
    function Nd(e) {
      var t = El();
      if (typeof e == "function") {
        var a = e;
        if (e = a(), Lr) {
          de(!0);
          try {
            a();
          } finally {
            de(!1);
          }
        }
      }
      return t.memoizedState = t.baseState = e, t.queue = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: Wa,
        lastRenderedState: e
      }, t;
    }
    function $c(e) {
      e = Nd(e);
      var t = e.queue, a = wd.bind(null, qe, t);
      return t.dispatch = a, [e.memoizedState, a];
    }
    function Zi(e) {
      var t = El();
      t.memoizedState = t.baseState = e;
      var a = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: null,
        lastRenderedState: null
      };
      return t.queue = a, t = Js.bind(
        null,
        qe,
        !0,
        a
      ), a.dispatch = t, [e, t];
    }
    function Gs(e, t) {
      var a = Dt();
      return tf(a, Zt, e, t);
    }
    function tf(e, t, a, c) {
      return e.baseState = a, Zc(
        e,
        Zt,
        typeof c == "function" ? c : Wa
      );
    }
    function Xs(e, t) {
      var a = Dt();
      return Zt !== null ? tf(a, Zt, e, t) : (a.baseState = e, [e, a.queue.dispatch]);
    }
    function Zp(e, t, a, c, o) {
      if (ql(e))
        throw Error("Cannot update form state while rendering.");
      if (e = t.action, e !== null) {
        var f = {
          payload: o,
          action: e,
          next: null,
          isTransition: !0,
          status: "pending",
          value: null,
          reason: null,
          listeners: [],
          then: function(d) {
            f.listeners.push(d);
          }
        };
        G.T !== null ? a(!0) : f.isTransition = !1, c(f), a = t.pending, a === null ? (f.next = t.pending = f, kc(t, f)) : (f.next = a.next, t.pending = a.next = f);
      }
    }
    function kc(e, t) {
      var a = t.action, c = t.payload, o = e.state;
      if (t.isTransition) {
        var f = G.T, d = {};
        d._updatedFibers = /* @__PURE__ */ new Set(), G.T = d;
        try {
          var h = a(o, c), y = G.S;
          y !== null && y(d, h), fy(e, t, h);
        } catch (p) {
          Ls(e, t, p);
        } finally {
          f !== null && d.types !== null && (f.types !== null && f.types !== d.types && console.error(
            "We expected inner Transitions to have transferred the outer types set and that you cannot add to the outer Transition while inside the inner.This is a bug in React."
          ), f.types = d.types), G.T = f, f === null && d._updatedFibers && (e = d._updatedFibers.size, d._updatedFibers.clear(), 10 < e && console.warn(
            "Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."
          ));
        }
      } else
        try {
          d = a(o, c), fy(e, t, d);
        } catch (p) {
          Ls(e, t, p);
        }
    }
    function fy(e, t, a) {
      a !== null && typeof a == "object" && typeof a.then == "function" ? (G.asyncTransitions++, a.then(Ki, Ki), a.then(
        function(c) {
          fc(e, t, c);
        },
        function(c) {
          return Ls(e, t, c);
        }
      ), t.isTransition || console.error(
        "An async function with useActionState was called outside of a transition. This is likely not what you intended (for example, isPending will not update correctly). Either call the returned function inside startTransition, or pass it to an `action` or `formAction` prop."
      )) : fc(e, t, a);
    }
    function fc(e, t, a) {
      t.status = "fulfilled", t.value = a, Hd(t), e.state = a, t = e.pending, t !== null && (a = t.next, a === t ? e.pending = null : (a = a.next, t.next = a, kc(e, a)));
    }
    function Ls(e, t, a) {
      var c = e.pending;
      if (e.pending = null, c !== null) {
        c = c.next;
        do
          t.status = "rejected", t.reason = a, Hd(t), t = t.next;
        while (t !== c);
      }
      e.action = null;
    }
    function Hd(e) {
      e = e.listeners;
      for (var t = 0; t < e.length; t++) (0, e[t])();
    }
    function sc(e, t) {
      return t;
    }
    function Fa(e, t) {
      if (st) {
        var a = Jt.formState;
        if (a !== null) {
          e: {
            var c = qe;
            if (st) {
              if (ll) {
                t: {
                  for (var o = ll, f = Ju; o.nodeType !== 8; ) {
                    if (!f) {
                      o = null;
                      break t;
                    }
                    if (o = an(
                      o.nextSibling
                    ), o === null) {
                      o = null;
                      break t;
                    }
                  }
                  f = o.data, o = f === pS || f === g2 ? o : null;
                }
                if (o) {
                  ll = an(
                    o.nextSibling
                  ), c = o.data === pS;
                  break e;
                }
              }
              gn(c);
            }
            c = !1;
          }
          c && (t = a[0]);
        }
      }
      return a = El(), a.memoizedState = a.baseState = t, c = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: sc,
        lastRenderedState: t
      }, a.queue = c, a = wd.bind(
        null,
        qe,
        c
      ), c.dispatch = a, c = Nd(!1), f = Js.bind(
        null,
        qe,
        !1,
        c.queue
      ), c = El(), o = {
        state: t,
        dispatch: null,
        action: e,
        pending: null
      }, c.queue = o, a = Zp.bind(
        null,
        qe,
        o,
        f,
        a
      ), o.dispatch = a, c.memoizedState = e, [t, a, !1];
    }
    function Wc(e) {
      var t = Dt();
      return jd(t, Zt, e);
    }
    function jd(e, t, a) {
      if (t = Zc(
        e,
        t,
        sc
      )[0], e = Li(Wa)[0], typeof t == "object" && t !== null && typeof t.then == "function")
        try {
          var c = ws(t);
        } catch (d) {
          throw d === um ? dv : d;
        }
      else c = t;
      t = Dt();
      var o = t.queue, f = o.dispatch;
      return a !== t.memoizedState && (qe.flags |= 2048, Tu(
        ku | rn,
        { destroy: void 0 },
        sy.bind(null, o, a),
        null
      )), [c, f, e];
    }
    function sy(e, t) {
      e.action = t;
    }
    function Fc(e) {
      var t = Dt(), a = Zt;
      if (a !== null)
        return jd(t, a, e);
      Dt(), t = t.memoizedState, a = Dt();
      var c = a.queue.dispatch;
      return a.memoizedState = e, [t, c, !1];
    }
    function Tu(e, t, a, c) {
      return e = { tag: e, create: a, deps: c, inst: t, next: null }, t = qe.updateQueue, t === null && (t = qs(), qe.updateQueue = t), a = t.lastEffect, a === null ? t.lastEffect = e.next = e : (c = a.next, a.next = e, e.next = c, t.lastEffect = e), e;
    }
    function Bd(e) {
      var t = El();
      return e = { current: e }, t.memoizedState = e;
    }
    function Ic(e, t, a, c) {
      var o = El();
      qe.flags |= e, o.memoizedState = Tu(
        ku | t,
        { destroy: void 0 },
        a,
        c === void 0 ? null : c
      );
    }
    function Rl(e, t, a, c) {
      var o = Dt();
      c = c === void 0 ? null : c;
      var f = o.memoizedState.inst;
      Zt !== null && c !== null && ny(c, Zt.memoizedState.deps) ? o.memoizedState = Tu(t, f, a, c) : (qe.flags |= e, o.memoizedState = Tu(
        ku | t,
        f,
        a,
        c
      ));
    }
    function Ji(e, t) {
      (qe.mode & Tc) !== He ? Ic(276826112, rn, e, t) : Ic(8390656, rn, e, t);
    }
    function Jp(e) {
      qe.flags |= 4;
      var t = qe.updateQueue;
      if (t === null)
        t = qs(), qe.updateQueue = t, t.events = [e];
      else {
        var a = t.events;
        a === null ? t.events = [e] : a.push(e);
      }
    }
    function Qs(e) {
      var t = El(), a = { impl: e };
      return t.memoizedState = a, function() {
        if ((pt & ea) !== sa)
          throw Error(
            "A function wrapped in useEffectEvent can't be called during rendering."
          );
        return a.impl.apply(void 0, arguments);
      };
    }
    function lf(e) {
      var t = Dt().memoizedState;
      return Jp({ ref: t, nextImpl: e }), function() {
        if ((pt & ea) !== sa)
          throw Error(
            "A function wrapped in useEffectEvent can't be called during rendering."
          );
        return t.impl.apply(void 0, arguments);
      };
    }
    function ga(e, t) {
      var a = 4194308;
      return (qe.mode & Tc) !== He && (a |= 134217728), Ic(a, nu, e, t);
    }
    function Ia(e, t) {
      if (typeof t == "function") {
        e = e();
        var a = t(e);
        return function() {
          typeof a == "function" ? a() : t(null);
        };
      }
      if (t != null)
        return t.hasOwnProperty("current") || console.error(
          "Expected useImperativeHandle() first argument to either be a ref callback or React.createRef() object. Instead received: %s.",
          "an object with keys {" + Object.keys(t).join(", ") + "}"
        ), e = e(), t.current = e, function() {
          t.current = null;
        };
    }
    function Au(e, t, a) {
      typeof t != "function" && console.error(
        "Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.",
        t !== null ? typeof t : "null"
      ), a = a != null ? a.concat([e]) : null;
      var c = 4194308;
      (qe.mode & Tc) !== He && (c |= 134217728), Ic(
        c,
        nu,
        Ia.bind(null, t, e),
        a
      );
    }
    function af(e, t, a) {
      typeof t != "function" && console.error(
        "Expected useImperativeHandle() second argument to be a function that creates a handle. Instead received: %s.",
        t !== null ? typeof t : "null"
      ), a = a != null ? a.concat([e]) : null, Rl(
        4,
        nu,
        Ia.bind(null, t, e),
        a
      );
    }
    function Yd(e, t) {
      return El().memoizedState = [
        e,
        t === void 0 ? null : t
      ], e;
    }
    function Vn(e, t) {
      var a = Dt();
      t = t === void 0 ? null : t;
      var c = a.memoizedState;
      return t !== null && ny(t, c[1]) ? c[0] : (a.memoizedState = [e, t], e);
    }
    function va(e, t) {
      var a = El();
      t = t === void 0 ? null : t;
      var c = e();
      if (Lr) {
        de(!0);
        try {
          e();
        } finally {
          de(!1);
        }
      }
      return a.memoizedState = [c, t], c;
    }
    function It(e, t) {
      var a = Dt();
      t = t === void 0 ? null : t;
      var c = a.memoizedState;
      if (t !== null && ny(t, c[1]))
        return c[0];
      if (c = e(), Lr) {
        de(!0);
        try {
          e();
        } finally {
          de(!1);
        }
      }
      return a.memoizedState = [c, t], c;
    }
    function nf(e, t) {
      var a = El();
      return Rt(a, e, t);
    }
    function Ou(e, t) {
      var a = Dt();
      return pl(
        a,
        Zt.memoizedState,
        e,
        t
      );
    }
    function Ke(e, t) {
      var a = Dt();
      return Zt === null ? Rt(a, e, t) : pl(
        a,
        Zt.memoizedState,
        e,
        t
      );
    }
    function Rt(e, t, a) {
      return a === void 0 || (Ao & 1073741824) !== 0 && (tt & 261930) === 0 ? e.memoizedState = t : (e.memoizedState = a, e = hf(), qe.lanes |= e, ts |= e, a);
    }
    function pl(e, t, a, c) {
      return on(a, t) ? a : im.current !== null ? (e = Rt(e, a, c), on(e, t) || (Zl = !0), e) : (Ao & 42) === 0 || (Ao & 1073741824) !== 0 && (tt & 261930) === 0 ? (Zl = !0, e.memoizedState = a) : (e = hf(), qe.lanes |= e, ts |= e, t);
    }
    function Ki() {
      G.asyncTransitions--;
    }
    function $i(e, t, a, c, o) {
      var f = At.p;
      At.p = f !== 0 && f < Il ? f : Il;
      var d = G.T, h = {};
      h._updatedFibers = /* @__PURE__ */ new Set(), G.T = h, Js(e, !1, t, a);
      try {
        var y = o(), p = G.S;
        if (p !== null && p(h, y), y !== null && typeof y == "object" && typeof y.then == "function") {
          G.asyncTransitions++, y.then(Ki, Ki);
          var z = _d(
            y,
            c
          );
          ki(
            e,
            t,
            z,
            ua(e)
          );
        } else
          ki(
            e,
            t,
            c,
            ua(e)
          );
      } catch (_) {
        ki(
          e,
          t,
          { then: function() {
          }, status: "rejected", reason: _ },
          ua(e)
        );
      } finally {
        At.p = f, d !== null && h.types !== null && (d.types !== null && d.types !== h.types && console.error(
          "We expected inner Transitions to have transferred the outer types set and that you cannot add to the outer Transition while inside the inner.This is a bug in React."
        ), d.types = h.types), G.T = d, d === null && h._updatedFibers && (e = h._updatedFibers.size, h._updatedFibers.clear(), 10 < e && console.warn(
          "Detected a large number of updates inside startTransition. If this is due to a subscription please re-write it to use React provided hooks. Otherwise concurrent mode guarantees are off the table."
        ));
      }
    }
    function rc(e, t, a, c) {
      if (e.tag !== 5)
        throw Error(
          "Expected the form instance to be a HostComponent. This is a bug in React."
        );
      var o = Vs(e).queue;
      Qp(e), $i(
        e,
        o,
        t,
        Pr,
        a === null ? W : function() {
          return uf(e), a(c);
        }
      );
    }
    function Vs(e) {
      var t = e.memoizedState;
      if (t !== null) return t;
      t = {
        memoizedState: Pr,
        baseState: Pr,
        baseQueue: null,
        queue: {
          pending: null,
          lanes: 0,
          dispatch: null,
          lastRenderedReducer: Wa,
          lastRenderedState: Pr
        },
        next: null
      };
      var a = {};
      return t.next = {
        memoizedState: a,
        baseState: a,
        baseQueue: null,
        queue: {
          pending: null,
          lanes: 0,
          dispatch: null,
          lastRenderedReducer: Wa,
          lastRenderedState: a
        },
        next: null
      }, e.memoizedState = t, e = e.alternate, e !== null && (e.memoizedState = t), t;
    }
    function uf(e) {
      G.T === null && console.error(
        "requestFormReset was called outside a transition or action. To fix, move to an action, or wrap with startTransition."
      );
      var t = Vs(e);
      t.next === null && (t = e.alternate.memoizedState), ki(
        e,
        t.next.queue,
        {},
        ua(e)
      );
    }
    function Pc() {
      var e = Nd(!1);
      return e = $i.bind(
        null,
        qe,
        e.queue,
        !0,
        !1
      ), El().memoizedState = e, [!1, e];
    }
    function Kp() {
      var e = Li(Wa)[0], t = Dt().memoizedState;
      return [
        typeof e == "boolean" ? e : ws(e),
        t
      ];
    }
    function nl() {
      var e = Qi(Wa)[0], t = Dt().memoizedState;
      return [
        typeof e == "boolean" ? e : ws(e),
        t
      ];
    }
    function dc() {
      return Et(gp);
    }
    function Zs() {
      var e = El(), t = Jt.identifierPrefix;
      if (st) {
        var a = vo, c = go;
        a = (c & ~(1 << 32 - Fl(c) - 1)).toString(32) + a, t = "_" + t + "R_" + a, a = gv++, 0 < a && (t += "H" + a.toString(32)), t += "_";
      } else
        a = lT++, t = "_" + t + "r_" + a.toString(32) + "_";
      return e.memoizedState = t;
    }
    function qd() {
      return El().memoizedState = $p.bind(
        null,
        qe
      );
    }
    function $p(e, t) {
      for (var a = e.return; a !== null; ) {
        switch (a.tag) {
          case 24:
          case 3:
            var c = ua(a), o = Dl(c), f = Su(a, o, c);
            f !== null && (pu(c, "refresh()", e), je(f, a, c), Tn(f, a, c)), e = Dd(), t != null && f !== null && console.error(
              "The seed argument is not enabled outside experimental channels."
            ), o.payload = { cache: e };
            return;
        }
        a = a.return;
      }
    }
    function c1(e, t, a) {
      var c = arguments;
      typeof c[3] == "function" && console.error(
        "State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect()."
      ), c = ua(e);
      var o = {
        lane: c,
        revertLane: 0,
        gesture: null,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      ql(e) ? sl(t, o) : (o = Ci(e, t, o, c), o !== null && (pu(c, "dispatch()", e), je(o, e, c), Ks(o, t, c)));
    }
    function wd(e, t, a) {
      var c = arguments;
      typeof c[3] == "function" && console.error(
        "State updates from the useState() and useReducer() Hooks don't support the second callback argument. To execute a side effect after rendering, declare it in the component body with useEffect()."
      ), c = ua(e), ki(e, t, a, c) && pu(c, "setState()", e);
    }
    function ki(e, t, a, c) {
      var o = {
        lane: c,
        revertLane: 0,
        gesture: null,
        action: a,
        hasEagerState: !1,
        eagerState: null,
        next: null
      };
      if (ql(e)) sl(t, o);
      else {
        var f = e.alternate;
        if (e.lanes === 0 && (f === null || f.lanes === 0) && (f = t.lastRenderedReducer, f !== null)) {
          var d = G.H;
          G.H = Oc;
          try {
            var h = t.lastRenderedState, y = f(h, a);
            if (o.hasEagerState = !0, o.eagerState = y, on(y, h))
              return Vo(e, t, o, 0), Jt === null && bd(), !1;
          } catch {
          } finally {
            G.H = d;
          }
        }
        if (a = Ci(e, t, o, c), a !== null)
          return je(a, e, c), Ks(a, t, c), !0;
      }
      return !1;
    }
    function Js(e, t, a, c) {
      if (G.T === null && Yr === 0 && console.error(
        "An optimistic state update occurred outside a transition or action. To fix, move the update to an action, or wrap with startTransition."
      ), c = {
        lane: 2,
        revertLane: Fy(),
        gesture: null,
        action: c,
        hasEagerState: !1,
        eagerState: null,
        next: null
      }, ql(e)) {
        if (t)
          throw Error("Cannot update optimistic state while rendering.");
        console.error("Cannot call startTransition while rendering.");
      } else
        t = Ci(
          e,
          a,
          c,
          2
        ), t !== null && (pu(2, "setOptimistic()", e), je(t, e, 2));
    }
    function ql(e) {
      var t = e.alternate;
      return e === qe || t !== null && t === qe;
    }
    function sl(e, t) {
      sm = pv = !0;
      var a = e.pending;
      a === null ? t.next = t : (t.next = a.next, a.next = t), e.pending = t;
    }
    function Ks(e, t, a) {
      if ((a & 4194048) !== 0) {
        var c = t.lanes;
        c &= e.pendingLanes, a |= c, t.lanes = a, ms(e, a);
      }
    }
    function Wi(e) {
      if (e !== null && typeof e != "function") {
        var t = String(e);
        Qb.has(t) || (Qb.add(t), console.error(
          "Expected the last optional `callback` argument to be a function. Instead received: %s.",
          e
        ));
      }
    }
    function cf(e, t, a, c) {
      var o = e.memoizedState, f = a(c, o);
      if (e.mode & Ba) {
        de(!0);
        try {
          f = a(c, o);
        } finally {
          de(!1);
        }
      }
      f === void 0 && (t = Je(t) || "Component", wb.has(t) || (wb.add(t), console.error(
        "%s.getDerivedStateFromProps(): A valid state object (or null) must be returned. You have returned undefined.",
        t
      ))), o = f == null ? o : Ie({}, o, f), e.memoizedState = o, e.lanes === 0 && (e.updateQueue.baseState = o);
    }
    function Gd(e, t, a, c, o, f, d) {
      var h = e.stateNode;
      if (typeof h.shouldComponentUpdate == "function") {
        if (a = h.shouldComponentUpdate(
          c,
          f,
          d
        ), e.mode & Ba) {
          de(!0);
          try {
            a = h.shouldComponentUpdate(
              c,
              f,
              d
            );
          } finally {
            de(!1);
          }
        }
        return a === void 0 && console.error(
          "%s.shouldComponentUpdate(): Returned undefined instead of a boolean value. Make sure to return true or false.",
          Je(t) || "Component"
        ), a;
      }
      return t.prototype && t.prototype.isPureReactComponent ? !Qo(a, c) || !Qo(o, f) : !0;
    }
    function zu(e, t, a, c) {
      var o = t.state;
      typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps(a, c), typeof t.UNSAFE_componentWillReceiveProps == "function" && t.UNSAFE_componentWillReceiveProps(a, c), t.state !== o && (e = se(e) || "Component", Hb.has(e) || (Hb.add(e), console.error(
        "%s.componentWillReceiveProps(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.",
        e
      )), $1.enqueueReplaceState(
        t,
        t.state,
        null
      ));
    }
    function Du(e, t) {
      var a = t;
      if ("ref" in t) {
        a = {};
        for (var c in t)
          c !== "ref" && (a[c] = t[c]);
      }
      if (e = e.defaultProps) {
        a === t && (a = Ie({}, a));
        for (var o in e)
          a[o] === void 0 && (a[o] = e[o]);
      }
      return a;
    }
    function Xd(e) {
      z1(e), console.warn(
        `%s

%s
`,
        rm ? "An error occurred in the <" + rm + "> component." : "An error occurred in one of your React components.",
        `Consider adding an error boundary to your tree to customize error handling behavior.
Visit https://react.dev/link/error-boundaries to learn more about error boundaries.`
      );
    }
    function Ld(e) {
      var t = rm ? "The above error occurred in the <" + rm + "> component." : "The above error occurred in one of your React components.", a = "React will try to recreate this component tree from scratch using the error boundary you provided, " + ((k1 || "Anonymous") + ".");
      if (typeof e == "object" && e !== null && typeof e.environmentName == "string") {
        var c = e.environmentName;
        e = [
          `%o

%s

%s
`,
          e,
          t,
          a
        ].slice(0), typeof e[0] == "string" ? e.splice(
          0,
          1,
          z2 + " " + e[0],
          D2,
          Lv + c + Lv,
          R2
        ) : e.splice(
          0,
          0,
          z2,
          D2,
          Lv + c + Lv,
          R2
        ), e.unshift(console), c = AT.apply(console.error, e), c();
      } else
        console.error(
          `%o

%s

%s
`,
          e,
          t,
          a
        );
    }
    function ry(e) {
      z1(e);
    }
    function $s(e, t) {
      try {
        rm = t.source ? se(t.source) : null, k1 = null;
        var a = t.value;
        if (G.actQueue !== null)
          G.thrownErrors.push(a);
        else {
          var c = e.onUncaughtError;
          c(a, { componentStack: t.stack });
        }
      } catch (o) {
        setTimeout(function() {
          throw o;
        });
      }
    }
    function dy(e, t, a) {
      try {
        rm = a.source ? se(a.source) : null, k1 = se(t);
        var c = e.onCaughtError;
        c(a.value, {
          componentStack: a.stack,
          errorBoundary: t.tag === 1 ? t.stateNode : null
        });
      } catch (o) {
        setTimeout(function() {
          throw o;
        });
      }
    }
    function Qd(e, t, a) {
      return a = Dl(a), a.tag = L1, a.payload = { element: null }, a.callback = function() {
        oe(t.source, $s, e, t);
      }, a;
    }
    function Vd(e) {
      return e = Dl(e), e.tag = L1, e;
    }
    function Zd(e, t, a, c) {
      var o = a.type.getDerivedStateFromError;
      if (typeof o == "function") {
        var f = c.value;
        e.payload = function() {
          return o(f);
        }, e.callback = function() {
          Ui(a), oe(
            c.source,
            dy,
            t,
            a,
            c
          );
        };
      }
      var d = a.stateNode;
      d !== null && typeof d.componentDidCatch == "function" && (e.callback = function() {
        Ui(a), oe(
          c.source,
          dy,
          t,
          a,
          c
        ), typeof o != "function" && (as === null ? as = /* @__PURE__ */ new Set([this]) : as.add(this)), IE(this, c), typeof o == "function" || (a.lanes & 2) === 0 && console.error(
          "%s: Error boundaries should implement getDerivedStateFromError(). In that method, return a state update to display an error message or fallback UI.",
          se(a) || "Unknown"
        );
      });
    }
    function hy(e, t, a, c, o) {
      if (a.flags |= 32768, wu && vf(e, o), c !== null && typeof c == "object" && typeof c.then == "function") {
        if (t = a.alternate, t !== null && wn(
          t,
          a,
          o,
          !0
        ), st && (yi = !0), a = au.current, a !== null) {
          switch (a.tag) {
            case 31:
            case 13:
              return $u === null ? yf() : a.alternate === null && dl === Ro && (dl = bv), a.flags &= -257, a.flags |= 65536, a.lanes = o, c === hv ? a.flags |= 16384 : (t = a.updateQueue, t === null ? a.updateQueue = /* @__PURE__ */ new Set([c]) : t.add(c), rh(e, c, o)), !1;
            case 22:
              return a.flags |= 65536, c === hv ? a.flags |= 16384 : (t = a.updateQueue, t === null ? (t = {
                transitions: null,
                markerInstances: null,
                retryQueue: /* @__PURE__ */ new Set([c])
              }, a.updateQueue = t) : (a = t.retryQueue, a === null ? t.retryQueue = /* @__PURE__ */ new Set([c]) : a.add(c)), rh(e, c, o)), !1;
          }
          throw Error(
            "Unexpected Suspense handler tag (" + a.tag + "). This is a bug in React."
          );
        }
        return rh(e, c, o), yf(), !1;
      }
      if (st)
        return yi = !0, t = au.current, t !== null ? ((t.flags & 65536) === 0 && (t.flags |= 256), t.flags |= 65536, t.lanes = o, c !== U1 && Rs(
          da(
            Error(
              "There was an error while hydrating but React was able to recover by instead client rendering from the nearest Suspense boundary.",
              { cause: c }
            ),
            a
          )
        )) : (c !== U1 && Rs(
          da(
            Error(
              "There was an error while hydrating but React was able to recover by instead client rendering the entire root.",
              { cause: c }
            ),
            a
          )
        ), e = e.current.alternate, e.flags |= 65536, o &= -o, e.lanes |= o, c = da(c, a), o = Qd(
          e.stateNode,
          c,
          o
        ), Ns(e, o), dl !== Pf && (dl = Qr)), !1;
      var f = da(
        Error(
          "There was an error during concurrent rendering but React was able to recover by instead synchronously rendering the entire root.",
          { cause: c }
        ),
        a
      );
      if (op === null ? op = [f] : op.push(f), dl !== Pf && (dl = Qr), t === null) return !0;
      c = da(c, a), a = t;
      do {
        switch (a.tag) {
          case 3:
            return a.flags |= 65536, e = o & -o, a.lanes |= e, e = Qd(
              a.stateNode,
              c,
              e
            ), Ns(a, e), !1;
          case 1:
            if (t = a.type, f = a.stateNode, (a.flags & 128) === 0 && (typeof t.getDerivedStateFromError == "function" || f !== null && typeof f.componentDidCatch == "function" && (as === null || !as.has(f))))
              return a.flags |= 65536, o &= -o, a.lanes |= o, o = Vd(o), Zd(
                o,
                e,
                a,
                c
              ), Ns(a, o), !1;
        }
        a = a.return;
      } while (a !== null);
      return !1;
    }
    function wl(e, t, a, c) {
      t.child = e === null ? Ab(t, null, a, c) : Xr(
        t,
        e.child,
        a,
        c
      );
    }
    function kp(e, t, a, c, o) {
      a = a.render;
      var f = t.ref;
      if ("ref" in c) {
        var d = {};
        for (var h in c)
          h !== "ref" && (d[h] = c[h]);
      } else d = c;
      return Lc(t), c = uy(
        e,
        t,
        a,
        d,
        f,
        o
      ), h = Xi(), e !== null && !Zl ? (Ys(e, t, o), Zn(e, t, o)) : (st && h && Ad(t), t.flags |= 1, wl(e, t, c, o), t.child);
    }
    function my(e, t, a, c, o) {
      if (e === null) {
        var f = a.type;
        return typeof f == "function" && !Jm(f) && f.defaultProps === void 0 && a.compare === null ? (a = Yc(f), t.tag = 15, t.type = a, of(t, f), yy(
          e,
          t,
          a,
          c,
          o
        )) : (e = xi(
          a.type,
          null,
          c,
          t,
          t.mode,
          o
        ), e.ref = t.ref, e.return = t, t.child = e);
      }
      if (f = e.child, !Wd(e, o)) {
        var d = f.memoizedProps;
        if (a = a.compare, a = a !== null ? a : Qo, a(d, c) && e.ref === t.ref)
          return Zn(
            e,
            t,
            o
          );
      }
      return t.flags |= 1, e = yu(f, c), e.ref = t.ref, e.return = t, t.child = e;
    }
    function yy(e, t, a, c, o) {
      if (e !== null) {
        var f = e.memoizedProps;
        if (Qo(f, c) && e.ref === t.ref && t.type === e.type)
          if (Zl = !1, t.pendingProps = c = f, Wd(e, o))
            (e.flags & 131072) !== 0 && (Zl = !0);
          else
            return t.lanes = e.lanes, Zn(e, t, o);
      }
      return Sy(
        e,
        t,
        a,
        c,
        o
      );
    }
    function py(e, t, a, c) {
      var o = c.children, f = e !== null ? e.memoizedState : null;
      if (e === null && t.stateNode === null && (t.stateNode = {
        _visibility: Y0,
        _pendingMarkers: null,
        _retryCache: null,
        _transitions: null
      }), c.mode === "hidden") {
        if ((t.flags & 128) !== 0) {
          if (f = f !== null ? f.baseLanes | a : a, e !== null) {
            for (c = t.child = e.child, o = 0; c !== null; )
              o = o | c.lanes | c.childLanes, c = c.sibling;
            c = o & ~f;
          } else c = 0, t.child = null;
          return gy(
            e,
            t,
            f,
            a,
            c
          );
        }
        if ((a & 536870912) !== 0)
          t.memoizedState = { baseLanes: 0, cachePool: null }, e !== null && ko(
            t,
            f !== null ? f.cachePool : null
          ), f !== null ? Ud(t, f) : cc(t), xd(t);
        else
          return c = t.lanes = 536870912, gy(
            e,
            t,
            f !== null ? f.baseLanes | a : a,
            a,
            c
          );
      } else
        f !== null ? (ko(t, f.cachePool), Ud(t, f), Eu(t), t.memoizedState = null) : (e !== null && ko(t, null), cc(t), Eu(t));
      return wl(e, t, o, a), t.child;
    }
    function Fi(e, t) {
      return e !== null && e.tag === 22 || t.stateNode !== null || (t.stateNode = {
        _visibility: Y0,
        _pendingMarkers: null,
        _retryCache: null,
        _transitions: null
      }), t.sibling;
    }
    function gy(e, t, a, c, o) {
      var f = uc();
      return f = f === null ? null : {
        parent: Ll._currentValue,
        pool: f
      }, t.memoizedState = {
        baseLanes: a,
        cachePool: f
      }, e !== null && ko(t, null), cc(t), xd(t), e !== null && wn(e, t, c, !0), t.childLanes = o, null;
    }
    function ks(e, t) {
      var a = t.hidden;
      return a !== void 0 && console.error(
        `<Activity> doesn't accept a hidden prop. Use mode="hidden" instead.
- <Activity %s>
+ <Activity %s>`,
        a === !0 ? "hidden" : a === !1 ? "hidden={false}" : "hidden={...}",
        a ? 'mode="hidden"' : 'mode="visible"'
      ), t = Fs(
        { mode: t.mode, children: t.children },
        e.mode
      ), t.ref = e.ref, e.child = t, t.return = e, t;
    }
    function vy(e, t, a) {
      return Xr(t, e.child, null, a), e = ks(
        t,
        t.pendingProps
      ), e.flags |= 2, Yl(t), t.memoizedState = null, e;
    }
    function Wp(e, t, a) {
      var c = t.pendingProps, o = (t.flags & 128) !== 0;
      if (t.flags &= -129, e === null) {
        if (st) {
          if (c.mode === "hidden")
            return e = ks(t, c), t.lanes = 536870912, Fi(null, e);
          if (Qn(t), (e = ll) ? (a = Mt(
            e,
            Ju
          ), a = a !== null && a.data === kr ? a : null, a !== null && (c = {
            dehydrated: a,
            treeContext: Gp(),
            retryLane: 536870912,
            hydrationErrors: null
          }, t.memoizedState = c, c = $m(a), c.return = t, t.child = c, Ra = t, ll = null)) : a = null, a === null)
            throw na(t, e), gn(t);
          return t.lanes = 536870912, null;
        }
        return ks(t, c);
      }
      var f = e.memoizedState;
      if (f !== null) {
        var d = f.dehydrated;
        if (Qn(t), o)
          if (t.flags & 256)
            t.flags &= -257, t = vy(
              e,
              t,
              a
            );
          else if (t.memoizedState !== null)
            t.child = e.child, t.flags |= 128, t = null;
          else
            throw Error(
              "Client rendering an Activity suspended it again. This is a bug in React."
            );
        else if (Lp(), (a & 536870912) !== 0 && mf(t), Zl || wn(
          e,
          t,
          a,
          !1
        ), o = (a & e.childLanes) !== 0, Zl || o) {
          if (c = Jt, c !== null && (d = Ei(
            c,
            a
          ), d !== 0 && d !== f.retryLane))
            throw f.retryLane = d, aa(e, d), je(c, e, d), W1;
          yf(), t = vy(
            e,
            t,
            a
          );
        } else
          e = f.treeContext, ll = an(
            d.nextSibling
          ), Ra = t, st = !0, Kf = null, yi = !1, lu = null, Ju = !1, e !== null && Xp(t, e), t = ks(t, c), t.flags |= 4096;
        return t;
      }
      return f = e.child, c = { mode: c.mode, children: c.children }, (a & 536870912) !== 0 && (a & e.lanes) !== 0 && mf(t), e = yu(f, c), e.ref = t.ref, t.child = e, e.return = t, e;
    }
    function Ws(e, t) {
      var a = t.ref;
      if (a === null)
        e !== null && e.ref !== null && (t.flags |= 4194816);
      else {
        if (typeof a != "function" && typeof a != "object")
          throw Error(
            "Expected ref to be a function, an object returned by React.createRef(), or undefined/null."
          );
        (e === null || e.ref !== a) && (t.flags |= 4194816);
      }
    }
    function Sy(e, t, a, c, o) {
      if (a.prototype && typeof a.prototype.render == "function") {
        var f = Je(a) || "Unknown";
        Vb[f] || (console.error(
          "The <%s /> component appears to have a render method, but doesn't extend React.Component. This is likely to cause errors. Change %s to extend React.Component instead.",
          f,
          f
        ), Vb[f] = !0);
      }
      return t.mode & Ba && Ac.recordLegacyContextWarning(
        t,
        null
      ), e === null && (of(t, t.type), a.contextTypes && (f = Je(a) || "Unknown", Jb[f] || (Jb[f] = !0, console.error(
        "%s uses the legacy contextTypes API which was removed in React 19. Use React.createContext() with React.useContext() instead. (https://react.dev/link/legacy-context)",
        f
      )))), Lc(t), a = uy(
        e,
        t,
        a,
        c,
        void 0,
        o
      ), c = Xi(), e !== null && !Zl ? (Ys(e, t, o), Zn(e, t, o)) : (st && c && Ad(t), t.flags |= 1, wl(e, t, a, o), t.child);
    }
    function by(e, t, a, c, o, f) {
      return Lc(t), zo = -1, tp = e !== null && e.type !== t.type, t.updateQueue = null, a = js(
        t,
        c,
        a,
        o
      ), yl(e, t), c = Xi(), e !== null && !Zl ? (Ys(e, t, f), Zn(e, t, f)) : (st && c && Ad(t), t.flags |= 1, wl(e, t, a, f), t.child);
    }
    function Ii(e, t, a, c, o) {
      switch (mt(t)) {
        case !1:
          var f = t.stateNode, d = new t.type(
            t.memoizedProps,
            f.context
          ).state;
          f.updater.enqueueSetState(f, d, null);
          break;
        case !0:
          t.flags |= 128, t.flags |= 65536, f = Error("Simulated error coming from DevTools");
          var h = o & -o;
          if (t.lanes |= h, d = Jt, d === null)
            throw Error(
              "Expected a work-in-progress root. This is a bug in React. Please file an issue."
            );
          h = Vd(h), Zd(
            h,
            d,
            t,
            da(f, t)
          ), Ns(t, h);
      }
      if (Lc(t), t.stateNode === null) {
        if (d = Jf, f = a.contextType, "contextType" in a && f !== null && (f === void 0 || f.$$typeof !== Pn) && !Lb.has(a) && (Lb.add(a), h = f === void 0 ? " However, it is set to undefined. This can be caused by a typo or by mixing up named and default imports. This can also happen due to a circular dependency, so try moving the createContext() call to a separate file." : typeof f != "object" ? " However, it is set to a " + typeof f + "." : f.$$typeof === Nh ? " Did you accidentally pass the Context.Consumer instead?" : " However, it is set to an object with keys {" + Object.keys(f).join(", ") + "}.", console.error(
          "%s defines an invalid contextType. contextType should point to the Context object returned by React.createContext().%s",
          Je(a) || "Component",
          h
        )), typeof f == "object" && f !== null && (d = Et(f)), f = new a(c, d), t.mode & Ba) {
          de(!0);
          try {
            f = new a(c, d);
          } finally {
            de(!1);
          }
        }
        if (d = t.memoizedState = f.state !== null && f.state !== void 0 ? f.state : null, f.updater = $1, t.stateNode = f, f._reactInternals = t, f._reactInternalInstance = Nb, typeof a.getDerivedStateFromProps == "function" && d === null && (d = Je(a) || "Component", jb.has(d) || (jb.add(d), console.error(
          "`%s` uses `getDerivedStateFromProps` but its initial state is %s. This is not recommended. Instead, define the initial state by assigning an object to `this.state` in the constructor of `%s`. This ensures that `getDerivedStateFromProps` arguments have a consistent shape.",
          d,
          f.state === null ? "null" : "undefined",
          d
        ))), typeof a.getDerivedStateFromProps == "function" || typeof f.getSnapshotBeforeUpdate == "function") {
          var y = h = d = null;
          if (typeof f.componentWillMount == "function" && f.componentWillMount.__suppressDeprecationWarning !== !0 ? d = "componentWillMount" : typeof f.UNSAFE_componentWillMount == "function" && (d = "UNSAFE_componentWillMount"), typeof f.componentWillReceiveProps == "function" && f.componentWillReceiveProps.__suppressDeprecationWarning !== !0 ? h = "componentWillReceiveProps" : typeof f.UNSAFE_componentWillReceiveProps == "function" && (h = "UNSAFE_componentWillReceiveProps"), typeof f.componentWillUpdate == "function" && f.componentWillUpdate.__suppressDeprecationWarning !== !0 ? y = "componentWillUpdate" : typeof f.UNSAFE_componentWillUpdate == "function" && (y = "UNSAFE_componentWillUpdate"), d !== null || h !== null || y !== null) {
            f = Je(a) || "Component";
            var p = typeof a.getDerivedStateFromProps == "function" ? "getDerivedStateFromProps()" : "getSnapshotBeforeUpdate()";
            Yb.has(f) || (Yb.add(f), console.error(
              `Unsafe legacy lifecycles will not be called for components using new component APIs.

%s uses %s but also contains the following legacy lifecycles:%s%s%s

The above lifecycles should be removed. Learn more about this warning here:
https://react.dev/link/unsafe-component-lifecycles`,
              f,
              p,
              d !== null ? `
  ` + d : "",
              h !== null ? `
  ` + h : "",
              y !== null ? `
  ` + y : ""
            ));
          }
        }
        f = t.stateNode, d = Je(a) || "Component", f.render || (a.prototype && typeof a.prototype.render == "function" ? console.error(
          "No `render` method found on the %s instance: did you accidentally return an object from the constructor?",
          d
        ) : console.error(
          "No `render` method found on the %s instance: you may have forgotten to define `render`.",
          d
        )), !f.getInitialState || f.getInitialState.isReactClassApproved || f.state || console.error(
          "getInitialState was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Did you mean to define a state property instead?",
          d
        ), f.getDefaultProps && !f.getDefaultProps.isReactClassApproved && console.error(
          "getDefaultProps was defined on %s, a plain JavaScript class. This is only supported for classes created using React.createClass. Use a static property to define defaultProps instead.",
          d
        ), f.contextType && console.error(
          "contextType was defined as an instance property on %s. Use a static property to define contextType instead.",
          d
        ), a.childContextTypes && !Xb.has(a) && (Xb.add(a), console.error(
          "%s uses the legacy childContextTypes API which was removed in React 19. Use React.createContext() instead. (https://react.dev/link/legacy-context)",
          d
        )), a.contextTypes && !Gb.has(a) && (Gb.add(a), console.error(
          "%s uses the legacy contextTypes API which was removed in React 19. Use React.createContext() with static contextType instead. (https://react.dev/link/legacy-context)",
          d
        )), typeof f.componentShouldUpdate == "function" && console.error(
          "%s has a method called componentShouldUpdate(). Did you mean shouldComponentUpdate()? The name is phrased as a question because the function is expected to return a value.",
          d
        ), a.prototype && a.prototype.isPureReactComponent && typeof f.shouldComponentUpdate < "u" && console.error(
          "%s has a method called shouldComponentUpdate(). shouldComponentUpdate should not be used when extending React.PureComponent. Please extend React.Component if shouldComponentUpdate is used.",
          Je(a) || "A pure component"
        ), typeof f.componentDidUnmount == "function" && console.error(
          "%s has a method called componentDidUnmount(). But there is no such lifecycle method. Did you mean componentWillUnmount()?",
          d
        ), typeof f.componentDidReceiveProps == "function" && console.error(
          "%s has a method called componentDidReceiveProps(). But there is no such lifecycle method. If you meant to update the state in response to changing props, use componentWillReceiveProps(). If you meant to fetch data or run side-effects or mutations after React has updated the UI, use componentDidUpdate().",
          d
        ), typeof f.componentWillRecieveProps == "function" && console.error(
          "%s has a method called componentWillRecieveProps(). Did you mean componentWillReceiveProps()?",
          d
        ), typeof f.UNSAFE_componentWillRecieveProps == "function" && console.error(
          "%s has a method called UNSAFE_componentWillRecieveProps(). Did you mean UNSAFE_componentWillReceiveProps()?",
          d
        ), h = f.props !== c, f.props !== void 0 && h && console.error(
          "When calling super() in `%s`, make sure to pass up the same props that your component's constructor was passed.",
          d
        ), f.defaultProps && console.error(
          "Setting defaultProps as an instance property on %s is not supported and will be ignored. Instead, define defaultProps as a static property on %s.",
          d,
          d
        ), typeof f.getSnapshotBeforeUpdate != "function" || typeof f.componentDidUpdate == "function" || Bb.has(a) || (Bb.add(a), console.error(
          "%s: getSnapshotBeforeUpdate() should be used with componentDidUpdate(). This component defines getSnapshotBeforeUpdate() only.",
          Je(a)
        )), typeof f.getDerivedStateFromProps == "function" && console.error(
          "%s: getDerivedStateFromProps() is defined as an instance method and will be ignored. Instead, declare it as a static method.",
          d
        ), typeof f.getDerivedStateFromError == "function" && console.error(
          "%s: getDerivedStateFromError() is defined as an instance method and will be ignored. Instead, declare it as a static method.",
          d
        ), typeof a.getSnapshotBeforeUpdate == "function" && console.error(
          "%s: getSnapshotBeforeUpdate() is defined as a static method and will be ignored. Instead, declare it as an instance method.",
          d
        ), (h = f.state) && (typeof h != "object" || Al(h)) && console.error("%s.state: must be set to an object or null", d), typeof f.getChildContext == "function" && typeof a.childContextTypes != "object" && console.error(
          "%s.getChildContext(): childContextTypes must be defined in order to use getChildContext().",
          d
        ), f = t.stateNode, f.props = c, f.state = t.memoizedState, f.refs = {}, ot(t), d = a.contextType, f.context = typeof d == "object" && d !== null ? Et(d) : Jf, f.state === c && (d = Je(a) || "Component", qb.has(d) || (qb.add(d), console.error(
          "%s: It is not recommended to assign props directly to state because updates to props won't be reflected in state. In most cases, it is better to use props directly.",
          d
        ))), t.mode & Ba && Ac.recordLegacyContextWarning(
          t,
          f
        ), Ac.recordUnsafeLifecycleWarnings(
          t,
          f
        ), f.state = t.memoizedState, d = a.getDerivedStateFromProps, typeof d == "function" && (cf(
          t,
          a,
          d,
          c
        ), f.state = t.memoizedState), typeof a.getDerivedStateFromProps == "function" || typeof f.getSnapshotBeforeUpdate == "function" || typeof f.UNSAFE_componentWillMount != "function" && typeof f.componentWillMount != "function" || (d = f.state, typeof f.componentWillMount == "function" && f.componentWillMount(), typeof f.UNSAFE_componentWillMount == "function" && f.UNSAFE_componentWillMount(), d !== f.state && (console.error(
          "%s.componentWillMount(): Assigning directly to this.state is deprecated (except inside a component's constructor). Use setState instead.",
          se(t) || "Component"
        ), $1.enqueueReplaceState(
          f,
          f.state,
          null
        )), bu(t, c, f, o), Fo(), f.state = t.memoizedState), typeof f.componentDidMount == "function" && (t.flags |= 4194308), (t.mode & Tc) !== He && (t.flags |= 134217728), f = !0;
      } else if (e === null) {
        f = t.stateNode;
        var z = t.memoizedProps;
        h = Du(a, z), f.props = h;
        var _ = f.context;
        y = a.contextType, d = Jf, typeof y == "object" && y !== null && (d = Et(y)), p = a.getDerivedStateFromProps, y = typeof p == "function" || typeof f.getSnapshotBeforeUpdate == "function", z = t.pendingProps !== z, y || typeof f.UNSAFE_componentWillReceiveProps != "function" && typeof f.componentWillReceiveProps != "function" || (z || _ !== d) && zu(
          t,
          f,
          c,
          d
        ), If = !1;
        var E = t.memoizedState;
        f.state = E, bu(t, c, f, o), Fo(), _ = t.memoizedState, z || E !== _ || If ? (typeof p == "function" && (cf(
          t,
          a,
          p,
          c
        ), _ = t.memoizedState), (h = If || Gd(
          t,
          a,
          h,
          c,
          E,
          _,
          d
        )) ? (y || typeof f.UNSAFE_componentWillMount != "function" && typeof f.componentWillMount != "function" || (typeof f.componentWillMount == "function" && f.componentWillMount(), typeof f.UNSAFE_componentWillMount == "function" && f.UNSAFE_componentWillMount()), typeof f.componentDidMount == "function" && (t.flags |= 4194308), (t.mode & Tc) !== He && (t.flags |= 134217728)) : (typeof f.componentDidMount == "function" && (t.flags |= 4194308), (t.mode & Tc) !== He && (t.flags |= 134217728), t.memoizedProps = c, t.memoizedState = _), f.props = c, f.state = _, f.context = d, f = h) : (typeof f.componentDidMount == "function" && (t.flags |= 4194308), (t.mode & Tc) !== He && (t.flags |= 134217728), f = !1);
      } else {
        f = t.stateNode, vu(e, t), d = t.memoizedProps, y = Du(a, d), f.props = y, p = t.pendingProps, E = f.context, _ = a.contextType, h = Jf, typeof _ == "object" && _ !== null && (h = Et(_)), z = a.getDerivedStateFromProps, (_ = typeof z == "function" || typeof f.getSnapshotBeforeUpdate == "function") || typeof f.UNSAFE_componentWillReceiveProps != "function" && typeof f.componentWillReceiveProps != "function" || (d !== p || E !== h) && zu(
          t,
          f,
          c,
          h
        ), If = !1, E = t.memoizedState, f.state = E, bu(t, c, f, o), Fo();
        var Y = t.memoizedState;
        d !== p || E !== Y || If || e !== null && e.dependencies !== null && Ko(e.dependencies) ? (typeof z == "function" && (cf(
          t,
          a,
          z,
          c
        ), Y = t.memoizedState), (y = If || Gd(
          t,
          a,
          y,
          c,
          E,
          Y,
          h
        ) || e !== null && e.dependencies !== null && Ko(e.dependencies)) ? (_ || typeof f.UNSAFE_componentWillUpdate != "function" && typeof f.componentWillUpdate != "function" || (typeof f.componentWillUpdate == "function" && f.componentWillUpdate(c, Y, h), typeof f.UNSAFE_componentWillUpdate == "function" && f.UNSAFE_componentWillUpdate(
          c,
          Y,
          h
        )), typeof f.componentDidUpdate == "function" && (t.flags |= 4), typeof f.getSnapshotBeforeUpdate == "function" && (t.flags |= 1024)) : (typeof f.componentDidUpdate != "function" || d === e.memoizedProps && E === e.memoizedState || (t.flags |= 4), typeof f.getSnapshotBeforeUpdate != "function" || d === e.memoizedProps && E === e.memoizedState || (t.flags |= 1024), t.memoizedProps = c, t.memoizedState = Y), f.props = c, f.state = Y, f.context = h, f = y) : (typeof f.componentDidUpdate != "function" || d === e.memoizedProps && E === e.memoizedState || (t.flags |= 4), typeof f.getSnapshotBeforeUpdate != "function" || d === e.memoizedProps && E === e.memoizedState || (t.flags |= 1024), f = !1);
      }
      if (h = f, Ws(e, t), d = (t.flags & 128) !== 0, h || d) {
        if (h = t.stateNode, _c(t), d && typeof a.getDerivedStateFromError != "function")
          a = null, fn = -1;
        else if (a = fb(h), t.mode & Ba) {
          de(!0);
          try {
            fb(h);
          } finally {
            de(!1);
          }
        }
        t.flags |= 1, e !== null && d ? (t.child = Xr(
          t,
          e.child,
          null,
          o
        ), t.child = Xr(
          t,
          null,
          a,
          o
        )) : wl(e, t, a, o), t.memoizedState = h.state, e = t.child;
      } else
        e = Zn(
          e,
          t,
          o
        );
      return o = t.stateNode, f && o.props !== c && (dm || console.error(
        "It looks like %s is reassigning its own `this.props` while rendering. This is not supported and can lead to confusing bugs.",
        se(t) || "a component"
      ), dm = !0), e;
    }
    function Ey(e, t, a, c) {
      return Gc(), t.flags |= 256, wl(e, t, a, c), t.child;
    }
    function of(e, t) {
      t && t.childContextTypes && console.error(
        `childContextTypes cannot be defined on a function component.
  %s.childContextTypes = ...`,
        t.displayName || t.name || "Component"
      ), typeof t.getDerivedStateFromProps == "function" && (e = Je(t) || "Unknown", Kb[e] || (console.error(
        "%s: Function components do not support getDerivedStateFromProps.",
        e
      ), Kb[e] = !0)), typeof t.contextType == "object" && t.contextType !== null && (t = Je(t) || "Unknown", Zb[t] || (console.error(
        "%s: Function components do not support contextType.",
        t
      ), Zb[t] = !0));
    }
    function ff(e) {
      return { baseLanes: e, cachePool: ey() };
    }
    function Jd(e, t, a) {
      return e = e !== null ? e.childLanes & ~a : 0, t && (e |= Cn), e;
    }
    function Kd(e, t, a) {
      var c, o = t.pendingProps;
      Se(t) && (t.flags |= 128);
      var f = !1, d = (t.flags & 128) !== 0;
      if ((c = d) || (c = e !== null && e.memoizedState === null ? !1 : (Ul.current & P0) !== 0), c && (f = !0, t.flags &= -129), c = (t.flags & 32) !== 0, t.flags &= -33, e === null) {
        if (st) {
          if (f ? pa(t) : Eu(t), (e = ll) ? (a = Mt(
            e,
            Ju
          ), a = a !== null && a.data !== kr ? a : null, a !== null && (c = {
            dehydrated: a,
            treeContext: Gp(),
            retryLane: 536870912,
            hydrationErrors: null
          }, t.memoizedState = c, c = $m(a), c.return = t, t.child = c, Ra = t, ll = null)) : a = null, a === null)
            throw na(t, e), gn(t);
          return e0(a) ? t.lanes = 32 : t.lanes = 536870912, null;
        }
        var h = o.children;
        if (o = o.fallback, f) {
          Eu(t);
          var y = t.mode;
          return h = Fs(
            { mode: "hidden", children: h },
            y
          ), o = Ni(
            o,
            y,
            a,
            null
          ), h.return = t, o.return = t, h.sibling = o, t.child = h, o = t.child, o.memoizedState = ff(a), o.childLanes = Jd(
            e,
            c,
            a
          ), t.memoizedState = F1, Fi(
            null,
            o
          );
        }
        return pa(t), Ty(
          t,
          h
        );
      }
      var p = e.memoizedState;
      if (p !== null) {
        var z = p.dehydrated;
        if (z !== null) {
          if (d)
            t.flags & 256 ? (pa(t), t.flags &= -257, t = $d(
              e,
              t,
              a
            )) : t.memoizedState !== null ? (Eu(t), t.child = e.child, t.flags |= 128, t = null) : (Eu(t), h = o.fallback, y = t.mode, o = Fs(
              {
                mode: "visible",
                children: o.children
              },
              y
            ), h = Ni(
              h,
              y,
              a,
              null
            ), h.flags |= 2, o.return = t, h.return = t, o.sibling = h, t.child = o, Xr(
              t,
              e.child,
              null,
              a
            ), o = t.child, o.memoizedState = ff(a), o.childLanes = Jd(
              e,
              c,
              a
            ), t.memoizedState = F1, t = Fi(
              null,
              o
            ));
          else if (pa(t), Lp(), (a & 536870912) !== 0 && mf(t), e0(
            z
          )) {
            if (c = z.nextSibling && z.nextSibling.dataset, c) {
              h = c.dgst;
              var _ = c.msg;
              y = c.stck;
              var E = c.cstck;
            }
            f = _, c = h, o = y, z = E, h = f, y = z, h = Error(h || "The server could not finish this Suspense boundary, likely due to an error during server rendering. Switched to client rendering."), h.stack = o || "", h.digest = c, c = y === void 0 ? null : y, o = {
              value: h,
              source: null,
              stack: c
            }, typeof c == "string" && C1.set(
              h,
              o
            ), Rs(o), t = $d(
              e,
              t,
              a
            );
          } else if (Zl || wn(
            e,
            t,
            a,
            !1
          ), c = (a & e.childLanes) !== 0, Zl || c) {
            if (c = Jt, c !== null && (o = Ei(
              c,
              a
            ), o !== 0 && o !== p.retryLane))
              throw p.retryLane = o, aa(
                e,
                o
              ), je(
                c,
                e,
                o
              ), W1;
            yr(
              z
            ) || yf(), t = $d(
              e,
              t,
              a
            );
          } else
            yr(
              z
            ) ? (t.flags |= 192, t.child = e.child, t = null) : (e = p.treeContext, ll = an(
              z.nextSibling
            ), Ra = t, st = !0, Kf = null, yi = !1, lu = null, Ju = !1, e !== null && Xp(t, e), t = Ty(
              t,
              o.children
            ), t.flags |= 4096);
          return t;
        }
      }
      return f ? (Eu(t), h = o.fallback, y = t.mode, E = e.child, z = E.sibling, o = yu(
        E,
        {
          mode: "hidden",
          children: o.children
        }
      ), o.subtreeFlags = E.subtreeFlags & 65011712, z !== null ? h = yu(
        z,
        h
      ) : (h = Ni(
        h,
        y,
        a,
        null
      ), h.flags |= 2), h.return = t, o.return = t, o.sibling = h, t.child = o, Fi(null, o), o = t.child, h = e.child.memoizedState, h === null ? h = ff(a) : (y = h.cachePool, y !== null ? (E = Ll._currentValue, y = y.parent !== E ? { parent: E, pool: E } : y) : y = ey(), h = {
        baseLanes: h.baseLanes | a,
        cachePool: y
      }), o.memoizedState = h, o.childLanes = Jd(
        e,
        c,
        a
      ), t.memoizedState = F1, Fi(
        e.child,
        o
      )) : (p !== null && (a & 62914560) === a && (a & e.lanes) !== 0 && mf(t), pa(t), a = e.child, e = a.sibling, a = yu(a, {
        mode: "visible",
        children: o.children
      }), a.return = t, a.sibling = null, e !== null && (c = t.deletions, c === null ? (t.deletions = [e], t.flags |= 16) : c.push(e)), t.child = a, t.memoizedState = null, a);
    }
    function Ty(e, t) {
      return t = Fs(
        { mode: "visible", children: t },
        e.mode
      ), t.return = e, e.child = t;
    }
    function Fs(e, t) {
      return e = x(22, e, null, t), e.lanes = 0, e;
    }
    function $d(e, t, a) {
      return Xr(t, e.child, null, a), e = Ty(
        t,
        t.pendingProps.children
      ), e.flags |= 2, t.memoizedState = null, e;
    }
    function Ay(e, t, a) {
      e.lanes |= t;
      var c = e.alternate;
      c !== null && (c.lanes |= t), zd(
        e.return,
        t,
        a
      );
    }
    function kd(e, t, a, c, o, f) {
      var d = e.memoizedState;
      d === null ? e.memoizedState = {
        isBackwards: t,
        rendering: null,
        renderingStartTime: 0,
        last: c,
        tail: a,
        tailMode: o,
        treeForkCount: f
      } : (d.isBackwards = t, d.rendering = null, d.renderingStartTime = 0, d.last = c, d.tail = a, d.tailMode = o, d.treeForkCount = f);
    }
    function Oy(e, t, a) {
      var c = t.pendingProps, o = c.revealOrder, f = c.tail, d = c.children, h = Ul.current;
      if ((c = (h & P0) !== 0) ? (h = h & om | P0, t.flags |= 128) : h &= om, Xe(Ul, h, t), h = o ?? "null", o !== "forwards" && o !== "unstable_legacy-backwards" && o !== "together" && o !== "independent" && !$b[h])
        if ($b[h] = !0, o == null)
          console.error(
            'The default for the <SuspenseList revealOrder="..."> prop is changing. To be future compatible you must explictly specify either "independent" (the current default), "together", "forwards" or "legacy_unstable-backwards".'
          );
        else if (o === "backwards")
          console.error(
            'The rendering order of <SuspenseList revealOrder="backwards"> is changing. To be future compatible you must specify revealOrder="legacy_unstable-backwards" instead.'
          );
        else if (typeof o == "string")
          switch (o.toLowerCase()) {
            case "together":
            case "forwards":
            case "backwards":
            case "independent":
              console.error(
                '"%s" is not a valid value for revealOrder on <SuspenseList />. Use lowercase "%s" instead.',
                o,
                o.toLowerCase()
              );
              break;
            case "forward":
            case "backward":
              console.error(
                '"%s" is not a valid value for revealOrder on <SuspenseList />. React uses the -s suffix in the spelling. Use "%ss" instead.',
                o,
                o.toLowerCase()
              );
              break;
            default:
              console.error(
                '"%s" is not a supported revealOrder on <SuspenseList />. Did you mean "independent", "together", "forwards" or "backwards"?',
                o
              );
          }
        else
          console.error(
            '%s is not a supported value for revealOrder on <SuspenseList />. Did you mean "independent", "together", "forwards" or "backwards"?',
            o
          );
      h = f ?? "null", Sv[h] || (f == null ? (o === "forwards" || o === "backwards" || o === "unstable_legacy-backwards") && (Sv[h] = !0, console.error(
        'The default for the <SuspenseList tail="..."> prop is changing. To be future compatible you must explictly specify either "visible" (the current default), "collapsed" or "hidden".'
      )) : f !== "visible" && f !== "collapsed" && f !== "hidden" ? (Sv[h] = !0, console.error(
        '"%s" is not a supported value for tail on <SuspenseList />. Did you mean "visible", "collapsed" or "hidden"?',
        f
      )) : o !== "forwards" && o !== "backwards" && o !== "unstable_legacy-backwards" && (Sv[h] = !0, console.error(
        '<SuspenseList tail="%s" /> is only valid if revealOrder is "forwards" or "backwards". Did you mean to specify revealOrder="forwards"?',
        f
      )));
      e: if ((o === "forwards" || o === "backwards" || o === "unstable_legacy-backwards") && d !== void 0 && d !== null && d !== !1)
        if (Al(d)) {
          for (h = 0; h < d.length; h++)
            if (!Lt(
              d[h],
              h
            ))
              break e;
        } else if (h = Ae(d), typeof h == "function") {
          if (h = h.call(d))
            for (var y = h.next(), p = 0; !y.done; y = h.next()) {
              if (!Lt(y.value, p)) break e;
              p++;
            }
        } else
          console.error(
            'A single row was passed to a <SuspenseList revealOrder="%s" />. This is not useful since it needs multiple rows. Did you mean to pass multiple children or an array?',
            o
          );
      if (wl(e, t, d, a), st ? (wc(), d = q0) : d = 0, !c && e !== null && (e.flags & 128) !== 0)
        e: for (e = t.child; e !== null; ) {
          if (e.tag === 13)
            e.memoizedState !== null && Ay(e, a, t);
          else if (e.tag === 19)
            Ay(e, a, t);
          else if (e.child !== null) {
            e.child.return = e, e = e.child;
            continue;
          }
          if (e === t) break e;
          for (; e.sibling === null; ) {
            if (e.return === null || e.return === t)
              break e;
            e = e.return;
          }
          e.sibling.return = e.return, e = e.sibling;
        }
      switch (o) {
        case "forwards":
          for (a = t.child, o = null; a !== null; )
            e = a.alternate, e !== null && Gi(e) === null && (o = a), a = a.sibling;
          a = o, a === null ? (o = t.child, t.child = null) : (o = a.sibling, a.sibling = null), kd(
            t,
            !1,
            o,
            a,
            f,
            d
          );
          break;
        case "backwards":
        case "unstable_legacy-backwards":
          for (a = null, o = t.child, t.child = null; o !== null; ) {
            if (e = o.alternate, e !== null && Gi(e) === null) {
              t.child = o;
              break;
            }
            e = o.sibling, o.sibling = a, a = o, o = e;
          }
          kd(
            t,
            !0,
            a,
            null,
            f,
            d
          );
          break;
        case "together":
          kd(
            t,
            !1,
            null,
            null,
            void 0,
            d
          );
          break;
        default:
          t.memoizedState = null;
      }
      return t.child;
    }
    function Zn(e, t, a) {
      if (e !== null && (t.dependencies = e.dependencies), fn = -1, ts |= t.lanes, (a & t.childLanes) === 0)
        if (e !== null) {
          if (wn(
            e,
            t,
            a,
            !1
          ), (a & t.childLanes) === 0)
            return null;
        } else return null;
      if (e !== null && t.child !== e.child)
        throw Error("Resuming work not yet implemented.");
      if (t.child !== null) {
        for (e = t.child, a = yu(e, e.pendingProps), t.child = a, a.return = t; e.sibling !== null; )
          e = e.sibling, a = a.sibling = yu(e, e.pendingProps), a.return = t;
        a.sibling = null;
      }
      return t.child;
    }
    function Wd(e, t) {
      return (e.lanes & t) !== 0 ? !0 : (e = e.dependencies, !!(e !== null && Ko(e)));
    }
    function Fp(e, t, a) {
      switch (t.tag) {
        case 3:
          Xt(
            t,
            t.stateNode.containerInfo
          ), vn(
            t,
            Ll,
            e.memoizedState.cache
          ), Gc();
          break;
        case 27:
        case 5:
          ee(t);
          break;
        case 4:
          Xt(
            t,
            t.stateNode.containerInfo
          );
          break;
        case 10:
          vn(
            t,
            t.type,
            t.memoizedProps.value
          );
          break;
        case 12:
          (a & t.childLanes) !== 0 && (t.flags |= 4), t.flags |= 2048;
          var c = t.stateNode;
          c.effectDuration = -0, c.passiveEffectDuration = -0;
          break;
        case 31:
          if (t.memoizedState !== null)
            return t.flags |= 128, Qn(t), null;
          break;
        case 13:
          if (c = t.memoizedState, c !== null)
            return c.dehydrated !== null ? (pa(t), t.flags |= 128, null) : (a & t.child.childLanes) !== 0 ? Kd(
              e,
              t,
              a
            ) : (pa(t), e = Zn(
              e,
              t,
              a
            ), e !== null ? e.sibling : null);
          pa(t);
          break;
        case 19:
          var o = (e.flags & 128) !== 0;
          if (c = (a & t.childLanes) !== 0, c || (wn(
            e,
            t,
            a,
            !1
          ), c = (a & t.childLanes) !== 0), o) {
            if (c)
              return Oy(
                e,
                t,
                a
              );
            t.flags |= 128;
          }
          if (o = t.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), Xe(
            Ul,
            Ul.current,
            t
          ), c) break;
          return null;
        case 22:
          return t.lanes = 0, py(
            e,
            t,
            a,
            t.pendingProps
          );
        case 24:
          vn(
            t,
            Ll,
            e.memoizedState.cache
          );
      }
      return Zn(e, t, a);
    }
    function Is(e, t, a) {
      if (t._debugNeedsRemount && e !== null) {
        a = xi(
          t.type,
          t.key,
          t.pendingProps,
          t._debugOwner || null,
          t.mode,
          t.lanes
        ), a._debugStack = t._debugStack, a._debugTask = t._debugTask;
        var c = t.return;
        if (c === null) throw Error("Cannot swap the root fiber.");
        if (e.alternate = null, t.alternate = null, a.index = t.index, a.sibling = t.sibling, a.return = t.return, a.ref = t.ref, a._debugInfo = t._debugInfo, t === c.child)
          c.child = a;
        else {
          var o = c.child;
          if (o === null)
            throw Error("Expected parent to have a child.");
          for (; o.sibling !== t; )
            if (o = o.sibling, o === null)
              throw Error("Expected to find the previous sibling.");
          o.sibling = a;
        }
        return t = c.deletions, t === null ? (c.deletions = [e], c.flags |= 16) : t.push(e), a.flags |= 2, a;
      }
      if (e !== null)
        if (e.memoizedProps !== t.pendingProps || t.type !== e.type)
          Zl = !0;
        else {
          if (!Wd(e, a) && (t.flags & 128) === 0)
            return Zl = !1, Fp(
              e,
              t,
              a
            );
          Zl = (e.flags & 131072) !== 0;
        }
      else
        Zl = !1, (c = st) && (wc(), c = (t.flags & 1048576) !== 0), c && (c = t.index, wc(), km(t, q0, c));
      switch (t.lanes = 0, t.tag) {
        case 16:
          e: if (c = t.pendingProps, e = $a(t.elementType), t.type = e, typeof e == "function")
            Jm(e) ? (c = Du(
              e,
              c
            ), t.tag = 1, t.type = e = Yc(e), t = Ii(
              null,
              t,
              e,
              c,
              a
            )) : (t.tag = 0, of(t, e), t.type = e = Yc(e), t = Sy(
              null,
              t,
              e,
              c,
              a
            ));
          else {
            if (e != null) {
              if (o = e.$$typeof, o === xf) {
                t.tag = 11, t.type = e = Ed(e), t = kp(
                  null,
                  t,
                  e,
                  c,
                  a
                );
                break e;
              } else if (o === zr) {
                t.tag = 14, t = my(
                  null,
                  t,
                  e,
                  c,
                  a
                );
                break e;
              }
            }
            throw t = "", e !== null && typeof e == "object" && e.$$typeof === ca && (t = " Did you wrap a component in React.lazy() more than once?"), a = Je(e) || e, Error(
              "Element type is invalid. Received a promise that resolves to: " + a + ". Lazy element type must resolve to a class or function." + t
            );
          }
          return t;
        case 0:
          return Sy(
            e,
            t,
            t.type,
            t.pendingProps,
            a
          );
        case 1:
          return c = t.type, o = Du(
            c,
            t.pendingProps
          ), Ii(
            e,
            t,
            c,
            o,
            a
          );
        case 3:
          e: {
            if (Xt(
              t,
              t.stateNode.containerInfo
            ), e === null)
              throw Error(
                "Should have a current fiber. This is a bug in React."
              );
            c = t.pendingProps;
            var f = t.memoizedState;
            o = f.element, vu(e, t), bu(t, c, null, a);
            var d = t.memoizedState;
            if (c = d.cache, vn(t, Ll, c), c !== f.cache && lc(
              t,
              [Ll],
              a,
              !0
            ), Fo(), c = d.element, f.isDehydrated)
              if (f = {
                element: c,
                isDehydrated: !1,
                cache: d.cache
              }, t.updateQueue.baseState = f, t.memoizedState = f, t.flags & 256) {
                t = Ey(
                  e,
                  t,
                  c,
                  a
                );
                break e;
              } else if (c !== o) {
                o = da(
                  Error(
                    "This root received an early update, before anything was able hydrate. Switched the entire root to client rendering."
                  ),
                  t
                ), Rs(o), t = Ey(
                  e,
                  t,
                  c,
                  a
                );
                break e;
              } else
                for (e = t.stateNode.containerInfo, e.nodeType === 9 ? e = e.body : e = e.nodeName === "HTML" ? e.ownerDocument.body : e, ll = an(e.firstChild), Ra = t, st = !0, Kf = null, yi = !1, lu = null, Ju = !0, a = Ab(
                  t,
                  null,
                  c,
                  a
                ), t.child = a; a; )
                  a.flags = a.flags & -3 | 4096, a = a.sibling;
            else {
              if (Gc(), c === o) {
                t = Zn(
                  e,
                  t,
                  a
                );
                break e;
              }
              wl(
                e,
                t,
                c,
                a
              );
            }
            t = t.child;
          }
          return t;
        case 26:
          return Ws(e, t), e === null ? (a = n0(
            t.type,
            null,
            t.pendingProps,
            null
          )) ? t.memoizedState = a : st || (a = t.type, e = t.pendingProps, c = Kt(
            nn.current
          ), c = hr(
            c
          ).createElement(a), c[el] = t, c[Da] = e, Pt(c, a, e), me(c), t.stateNode = c) : t.memoizedState = n0(
            t.type,
            e.memoizedProps,
            t.pendingProps,
            e.memoizedState
          ), null;
        case 27:
          return ee(t), e === null && st && (c = Kt(nn.current), o = Z(), c = t.stateNode = vc(
            t.type,
            t.pendingProps,
            c,
            o,
            !1
          ), yi || (o = Na(
            c,
            t.type,
            t.pendingProps,
            o
          ), o !== null && (Hi(t, 0).serverProps = o)), Ra = t, Ju = !0, o = ll, oi(t.type) ? (bS = o, ll = an(
            c.firstChild
          )) : ll = o), wl(
            e,
            t,
            t.pendingProps.children,
            a
          ), Ws(e, t), e === null && (t.flags |= 4194304), t.child;
        case 5:
          return e === null && st && (f = Z(), c = gs(
            t.type,
            f.ancestorInfo
          ), o = ll, (d = !o) || (d = Rg(
            o,
            t.type,
            t.pendingProps,
            Ju
          ), d !== null ? (t.stateNode = d, yi || (f = Na(
            d,
            t.type,
            t.pendingProps,
            f
          ), f !== null && (Hi(t, 0).serverProps = f)), Ra = t, ll = an(
            d.firstChild
          ), Ju = !1, f = !0) : f = !1, d = !f), d && (c && na(t, o), gn(t))), ee(t), o = t.type, f = t.pendingProps, d = e !== null ? e.memoizedProps : null, c = f.children, Af(o, f) ? c = null : d !== null && Af(o, d) && (t.flags |= 32), t.memoizedState !== null && (o = uy(
            e,
            t,
            Bs,
            null,
            null,
            a
          ), gp._currentValue = o), Ws(e, t), wl(
            e,
            t,
            c,
            a
          ), t.child;
        case 6:
          return e === null && st && (a = t.pendingProps, e = Z(), c = e.ancestorInfo.current, a = c != null ? vs(
            a,
            c.tag,
            e.ancestorInfo.implicitRootScope
          ) : !0, e = ll, (c = !e) || (c = _g(
            e,
            t.pendingProps,
            Ju
          ), c !== null ? (t.stateNode = c, Ra = t, ll = null, c = !0) : c = !1, c = !c), c && (a && na(t, e), gn(t))), null;
        case 13:
          return Kd(e, t, a);
        case 4:
          return Xt(
            t,
            t.stateNode.containerInfo
          ), c = t.pendingProps, e === null ? t.child = Xr(
            t,
            null,
            c,
            a
          ) : wl(
            e,
            t,
            c,
            a
          ), t.child;
        case 11:
          return kp(
            e,
            t,
            t.type,
            t.pendingProps,
            a
          );
        case 7:
          return wl(
            e,
            t,
            t.pendingProps,
            a
          ), t.child;
        case 8:
          return wl(
            e,
            t,
            t.pendingProps.children,
            a
          ), t.child;
        case 12:
          return t.flags |= 4, t.flags |= 2048, c = t.stateNode, c.effectDuration = -0, c.passiveEffectDuration = -0, wl(
            e,
            t,
            t.pendingProps.children,
            a
          ), t.child;
        case 10:
          return c = t.type, o = t.pendingProps, f = o.value, "value" in o || kb || (kb = !0, console.error(
            "The `value` prop is required for the `<Context.Provider>`. Did you misspell it or forget to pass it?"
          )), vn(t, c, f), wl(
            e,
            t,
            o.children,
            a
          ), t.child;
        case 9:
          return o = t.type._context, c = t.pendingProps.children, typeof c != "function" && console.error(
            "A context consumer was rendered with multiple children, or a child that isn't a function. A context consumer expects a single child that is a function. If you did pass a function, make sure there is no trailing or leading whitespace around it."
          ), Lc(t), o = Et(o), c = q1(
            c,
            o,
            void 0
          ), t.flags |= 1, wl(
            e,
            t,
            c,
            a
          ), t.child;
        case 14:
          return my(
            e,
            t,
            t.type,
            t.pendingProps,
            a
          );
        case 15:
          return yy(
            e,
            t,
            t.type,
            t.pendingProps,
            a
          );
        case 19:
          return Oy(
            e,
            t,
            a
          );
        case 31:
          return Wp(e, t, a);
        case 22:
          return py(
            e,
            t,
            a,
            t.pendingProps
          );
        case 24:
          return Lc(t), c = Et(Ll), e === null ? (o = uc(), o === null && (o = Jt, f = Dd(), o.pooledCache = f, Bi(f), f !== null && (o.pooledCacheLanes |= a), o = f), t.memoizedState = {
            parent: c,
            cache: o
          }, ot(t), vn(t, Ll, o)) : ((e.lanes & a) !== 0 && (vu(e, t), bu(t, null, null, a), Fo()), o = e.memoizedState, f = t.memoizedState, o.parent !== c ? (o = {
            parent: c,
            cache: c
          }, t.memoizedState = o, t.lanes === 0 && (t.memoizedState = t.updateQueue.baseState = o), vn(t, Ll, c)) : (c = f.cache, vn(t, Ll, c), c !== o.cache && lc(
            t,
            [Ll],
            a,
            !0
          ))), wl(
            e,
            t,
            t.pendingProps.children,
            a
          ), t.child;
        case 29:
          throw t.pendingProps;
      }
      throw Error(
        "Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue."
      );
    }
    function Ru(e) {
      e.flags |= 4;
    }
    function Fd(e, t, a, c, o) {
      if ((t = (e.mode & KE) !== He) && (t = !1), t) {
        if (e.flags |= 16777216, (o & 335544128) === o)
          if (e.stateNode.complete) e.flags |= 8192;
          else if (Ly()) e.flags |= 8192;
          else
            throw Gr = hv, G1;
      } else e.flags &= -16777217;
    }
    function Ip(e, t) {
      if (t.type !== "stylesheet" || (t.state.loading & Fu) !== Ir)
        e.flags &= -16777217;
      else if (e.flags |= 16777216, !ct(t))
        if (Ly()) e.flags |= 8192;
        else
          throw Gr = hv, G1;
    }
    function sf(e, t) {
      t !== null && (e.flags |= 4), e.flags & 16384 && (t = e.tag !== 22 ? Uo() : 536870912, e.lanes |= t, Jr |= t);
    }
    function rf(e, t) {
      if (!st)
        switch (e.tailMode) {
          case "hidden":
            t = e.tail;
            for (var a = null; t !== null; )
              t.alternate !== null && (a = t), t = t.sibling;
            a === null ? e.tail = null : a.sibling = null;
            break;
          case "collapsed":
            a = e.tail;
            for (var c = null; a !== null; )
              a.alternate !== null && (c = a), a = a.sibling;
            c === null ? t || e.tail === null ? e.tail = null : e.tail.sibling = null : c.sibling = null;
        }
    }
    function xt(e) {
      var t = e.alternate !== null && e.alternate.child === e.child, a = 0, c = 0;
      if (t)
        if ((e.mode & Pe) !== He) {
          for (var o = e.selfBaseDuration, f = e.child; f !== null; )
            a |= f.lanes | f.childLanes, c |= f.subtreeFlags & 65011712, c |= f.flags & 65011712, o += f.treeBaseDuration, f = f.sibling;
          e.treeBaseDuration = o;
        } else
          for (o = e.child; o !== null; )
            a |= o.lanes | o.childLanes, c |= o.subtreeFlags & 65011712, c |= o.flags & 65011712, o.return = e, o = o.sibling;
      else if ((e.mode & Pe) !== He) {
        o = e.actualDuration, f = e.selfBaseDuration;
        for (var d = e.child; d !== null; )
          a |= d.lanes | d.childLanes, c |= d.subtreeFlags, c |= d.flags, o += d.actualDuration, f += d.treeBaseDuration, d = d.sibling;
        e.actualDuration = o, e.treeBaseDuration = f;
      } else
        for (o = e.child; o !== null; )
          a |= o.lanes | o.childLanes, c |= o.subtreeFlags, c |= o.flags, o.return = e, o = o.sibling;
      return e.subtreeFlags |= c, e.childLanes = a, t;
    }
    function zy(e, t, a) {
      var c = t.pendingProps;
      switch (Od(t), t.tag) {
        case 16:
        case 15:
        case 0:
        case 11:
        case 7:
        case 8:
        case 12:
        case 9:
        case 14:
          return xt(t), null;
        case 1:
          return xt(t), null;
        case 3:
          return a = t.stateNode, c = null, e !== null && (c = e.memoizedState.cache), t.memoizedState.cache !== c && (t.flags |= 2048), qn(Ll, t), R(t), a.pendingContext && (a.context = a.pendingContext, a.pendingContext = null), (e === null || e.child === null) && (ji(t) ? (Xc(), Ru(t)) : e === null || e.memoizedState.isDehydrated && (t.flags & 256) === 0 || (t.flags |= 1024, Ds())), xt(t), null;
        case 26:
          var o = t.type, f = t.memoizedState;
          return e === null ? (Ru(t), f !== null ? (xt(t), Ip(
            t,
            f
          )) : (xt(t), Fd(
            t,
            o,
            null,
            c,
            a
          ))) : f ? f !== e.memoizedState ? (Ru(t), xt(t), Ip(
            t,
            f
          )) : (xt(t), t.flags &= -16777217) : (e = e.memoizedProps, e !== c && Ru(t), xt(t), Fd(
            t,
            o,
            e,
            c,
            a
          )), null;
        case 27:
          if (ge(t), a = Kt(nn.current), o = t.type, e !== null && t.stateNode != null)
            e.memoizedProps !== c && Ru(t);
          else {
            if (!c) {
              if (t.stateNode === null)
                throw Error(
                  "We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue."
                );
              return xt(t), null;
            }
            e = Z(), ji(t) ? Wm(t) : (e = vc(
              o,
              c,
              a,
              e,
              !0
            ), t.stateNode = e, Ru(t));
          }
          return xt(t), null;
        case 5:
          if (ge(t), o = t.type, e !== null && t.stateNode != null)
            e.memoizedProps !== c && Ru(t);
          else {
            if (!c) {
              if (t.stateNode === null)
                throw Error(
                  "We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue."
                );
              return xt(t), null;
            }
            var d = Z();
            if (ji(t))
              Wm(t);
            else {
              switch (f = Kt(nn.current), gs(o, d.ancestorInfo), d = d.context, f = hr(f), d) {
                case bm:
                  f = f.createElementNS(
                    We,
                    o
                  );
                  break;
                case wv:
                  f = f.createElementNS(
                    Ve,
                    o
                  );
                  break;
                default:
                  switch (o) {
                    case "svg":
                      f = f.createElementNS(
                        We,
                        o
                      );
                      break;
                    case "math":
                      f = f.createElementNS(
                        Ve,
                        o
                      );
                      break;
                    case "script":
                      f = f.createElement("div"), f.innerHTML = "<script><\/script>", f = f.removeChild(
                        f.firstChild
                      );
                      break;
                    case "select":
                      f = typeof c.is == "string" ? f.createElement("select", {
                        is: c.is
                      }) : f.createElement("select"), c.multiple ? f.multiple = !0 : c.size && (f.size = c.size);
                      break;
                    default:
                      f = typeof c.is == "string" ? f.createElement(o, {
                        is: c.is
                      }) : f.createElement(o), o.indexOf("-") === -1 && (o !== o.toLowerCase() && console.error(
                        "<%s /> is using incorrect casing. Use PascalCase for React components, or lowercase for HTML elements.",
                        o
                      ), Object.prototype.toString.call(f) !== "[object HTMLUnknownElement]" || un.call(S2, o) || (S2[o] = !0, console.error(
                        "The tag <%s> is unrecognized in this browser. If you meant to render a React component, start its name with an uppercase letter.",
                        o
                      )));
                  }
              }
              f[el] = t, f[Da] = c;
              e: for (d = t.child; d !== null; ) {
                if (d.tag === 5 || d.tag === 6)
                  f.appendChild(d.stateNode);
                else if (d.tag !== 4 && d.tag !== 27 && d.child !== null) {
                  d.child.return = d, d = d.child;
                  continue;
                }
                if (d === t) break e;
                for (; d.sibling === null; ) {
                  if (d.return === null || d.return === t)
                    break e;
                  d = d.return;
                }
                d.sibling.return = d.return, d = d.sibling;
              }
              t.stateNode = f;
              e: switch (Pt(f, o, c), o) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  c = !!c.autoFocus;
                  break e;
                case "img":
                  c = !0;
                  break e;
                default:
                  c = !1;
              }
              c && Ru(t);
            }
          }
          return xt(t), Fd(
            t,
            t.type,
            e === null ? null : e.memoizedProps,
            t.pendingProps,
            a
          ), null;
        case 6:
          if (e && t.stateNode != null)
            e.memoizedProps !== c && Ru(t);
          else {
            if (typeof c != "string" && t.stateNode === null)
              throw Error(
                "We must have new props for new mounts. This error is likely caused by a bug in React. Please file an issue."
              );
            if (e = Kt(nn.current), a = Z(), ji(t)) {
              if (e = t.stateNode, a = t.memoizedProps, o = !yi, c = null, f = Ra, f !== null)
                switch (f.tag) {
                  case 3:
                    o && (o = Ug(
                      e,
                      a,
                      c
                    ), o !== null && (Hi(t, 0).serverProps = o));
                    break;
                  case 27:
                  case 5:
                    c = f.memoizedProps, o && (o = Ug(
                      e,
                      a,
                      c
                    ), o !== null && (Hi(
                      t,
                      0
                    ).serverProps = o));
                }
              e[el] = t, e = !!(e.nodeValue === a || c !== null && c.suppressHydrationWarning === !0 || Iy(e.nodeValue, a)), e || gn(t, !0);
            } else
              o = a.ancestorInfo.current, o != null && vs(
                c,
                o.tag,
                a.ancestorInfo.implicitRootScope
              ), e = hr(e).createTextNode(
                c
              ), e[el] = t, t.stateNode = e;
          }
          return xt(t), null;
        case 31:
          if (a = t.memoizedState, e === null || e.memoizedState !== null) {
            if (c = ji(t), a !== null) {
              if (e === null) {
                if (!c)
                  throw Error(
                    "A dehydrated suspense component was completed without a hydrated node. This is probably a bug in React."
                  );
                if (e = t.memoizedState, e = e !== null ? e.dehydrated : null, !e)
                  throw Error(
                    "Expected to have a hydrated activity instance. This error is likely caused by a bug in React. Please file an issue."
                  );
                e[el] = t, xt(t), (t.mode & Pe) !== He && a !== null && (e = t.child, e !== null && (t.treeBaseDuration -= e.treeBaseDuration));
              } else
                Xc(), Gc(), (t.flags & 128) === 0 && (a = t.memoizedState = null), t.flags |= 4, xt(t), (t.mode & Pe) !== He && a !== null && (e = t.child, e !== null && (t.treeBaseDuration -= e.treeBaseDuration));
              e = !1;
            } else
              a = Ds(), e !== null && e.memoizedState !== null && (e.memoizedState.hydrationErrors = a), e = !0;
            if (!e)
              return t.flags & 256 ? (Yl(t), t) : (Yl(t), null);
            if ((t.flags & 128) !== 0)
              throw Error(
                "Client rendering an Activity suspended it again. This is a bug in React."
              );
          }
          return xt(t), null;
        case 13:
          if (c = t.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
            if (o = c, f = ji(t), o !== null && o.dehydrated !== null) {
              if (e === null) {
                if (!f)
                  throw Error(
                    "A dehydrated suspense component was completed without a hydrated node. This is probably a bug in React."
                  );
                if (f = t.memoizedState, f = f !== null ? f.dehydrated : null, !f)
                  throw Error(
                    "Expected to have a hydrated suspense instance. This error is likely caused by a bug in React. Please file an issue."
                  );
                f[el] = t, xt(t), (t.mode & Pe) !== He && o !== null && (o = t.child, o !== null && (t.treeBaseDuration -= o.treeBaseDuration));
              } else
                Xc(), Gc(), (t.flags & 128) === 0 && (o = t.memoizedState = null), t.flags |= 4, xt(t), (t.mode & Pe) !== He && o !== null && (o = t.child, o !== null && (t.treeBaseDuration -= o.treeBaseDuration));
              o = !1;
            } else
              o = Ds(), e !== null && e.memoizedState !== null && (e.memoizedState.hydrationErrors = o), o = !0;
            if (!o)
              return t.flags & 256 ? (Yl(t), t) : (Yl(t), null);
          }
          return Yl(t), (t.flags & 128) !== 0 ? (t.lanes = a, (t.mode & Pe) !== He && qi(t), t) : (a = c !== null, e = e !== null && e.memoizedState !== null, a && (c = t.child, o = null, c.alternate !== null && c.alternate.memoizedState !== null && c.alternate.memoizedState.cachePool !== null && (o = c.alternate.memoizedState.cachePool.pool), f = null, c.memoizedState !== null && c.memoizedState.cachePool !== null && (f = c.memoizedState.cachePool.pool), f !== o && (c.flags |= 2048)), a !== e && a && (t.child.flags |= 8192), sf(t, t.updateQueue), xt(t), (t.mode & Pe) !== He && a && (e = t.child, e !== null && (t.treeBaseDuration -= e.treeBaseDuration)), null);
        case 4:
          return R(t), e === null && ci(
            t.stateNode.containerInfo
          ), xt(t), null;
        case 10:
          return qn(t.type, t), xt(t), null;
        case 19:
          if (pe(Ul, t), c = t.memoizedState, c === null) return xt(t), null;
          if (o = (t.flags & 128) !== 0, f = c.rendering, f === null)
            if (o) rf(c, !1);
            else {
              if (dl !== Ro || e !== null && (e.flags & 128) !== 0)
                for (e = t.child; e !== null; ) {
                  if (f = Gi(e), f !== null) {
                    for (t.flags |= 128, rf(c, !1), e = f.updateQueue, t.updateQueue = e, sf(t, e), t.subtreeFlags = 0, e = a, a = t.child; a !== null; )
                      Km(a, e), a = a.sibling;
                    return Xe(
                      Ul,
                      Ul.current & om | P0,
                      t
                    ), st && Yn(t, c.treeForkCount), t.child;
                  }
                  e = e.sibling;
                }
              c.tail !== null && Xl() > Dv && (t.flags |= 128, o = !0, rf(c, !1), t.lanes = 4194304);
            }
          else {
            if (!o)
              if (e = Gi(f), e !== null) {
                if (t.flags |= 128, o = !0, e = e.updateQueue, t.updateQueue = e, sf(t, e), rf(c, !0), c.tail === null && c.tailMode === "hidden" && !f.alternate && !st)
                  return xt(t), null;
              } else
                2 * Xl() - c.renderingStartTime > Dv && a !== 536870912 && (t.flags |= 128, o = !0, rf(c, !1), t.lanes = 4194304);
            c.isBackwards ? (f.sibling = t.child, t.child = f) : (e = c.last, e !== null ? e.sibling = f : t.child = f, c.last = f);
          }
          return c.tail !== null ? (e = c.tail, c.rendering = e, c.tail = e.sibling, c.renderingStartTime = Xl(), e.sibling = null, a = Ul.current, a = o ? a & om | P0 : a & om, Xe(Ul, a, t), st && Yn(t, c.treeForkCount), e) : (xt(t), null);
        case 22:
        case 23:
          return Yl(t), Ln(t), c = t.memoizedState !== null, e !== null ? e.memoizedState !== null !== c && (t.flags |= 8192) : c && (t.flags |= 8192), c ? (a & 536870912) !== 0 && (t.flags & 128) === 0 && (xt(t), t.subtreeFlags & 6 && (t.flags |= 8192)) : xt(t), a = t.updateQueue, a !== null && sf(t, a.retryQueue), a = null, e !== null && e.memoizedState !== null && e.memoizedState.cachePool !== null && (a = e.memoizedState.cachePool.pool), c = null, t.memoizedState !== null && t.memoizedState.cachePool !== null && (c = t.memoizedState.cachePool.pool), c !== a && (t.flags |= 2048), e !== null && pe(qr, t), null;
        case 24:
          return a = null, e !== null && (a = e.memoizedState.cache), t.memoizedState.cache !== a && (t.flags |= 2048), qn(Ll, t), xt(t), null;
        case 25:
          return null;
        case 30:
          return null;
      }
      throw Error(
        "Unknown unit of work tag (" + t.tag + "). This error is likely caused by a bug in React. Please file an issue."
      );
    }
    function Pp(e, t) {
      switch (Od(t), t.tag) {
        case 1:
          return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, (t.mode & Pe) !== He && qi(t), t) : null;
        case 3:
          return qn(Ll, t), R(t), e = t.flags, (e & 65536) !== 0 && (e & 128) === 0 ? (t.flags = e & -65537 | 128, t) : null;
        case 26:
        case 27:
        case 5:
          return ge(t), null;
        case 31:
          if (t.memoizedState !== null) {
            if (Yl(t), t.alternate === null)
              throw Error(
                "Threw in newly mounted dehydrated component. This is likely a bug in React. Please file an issue."
              );
            Gc();
          }
          return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, (t.mode & Pe) !== He && qi(t), t) : null;
        case 13:
          if (Yl(t), e = t.memoizedState, e !== null && e.dehydrated !== null) {
            if (t.alternate === null)
              throw Error(
                "Threw in newly mounted dehydrated component. This is likely a bug in React. Please file an issue."
              );
            Gc();
          }
          return e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, (t.mode & Pe) !== He && qi(t), t) : null;
        case 19:
          return pe(Ul, t), null;
        case 4:
          return R(t), null;
        case 10:
          return qn(t.type, t), null;
        case 22:
        case 23:
          return Yl(t), Ln(t), e !== null && pe(qr, t), e = t.flags, e & 65536 ? (t.flags = e & -65537 | 128, (t.mode & Pe) !== He && qi(t), t) : null;
        case 24:
          return qn(Ll, t), null;
        case 25:
          return null;
        default:
          return null;
      }
    }
    function Dy(e, t) {
      switch (Od(t), t.tag) {
        case 3:
          qn(Ll, t), R(t);
          break;
        case 26:
        case 27:
        case 5:
          ge(t);
          break;
        case 4:
          R(t);
          break;
        case 31:
          t.memoizedState !== null && Yl(t);
          break;
        case 13:
          Yl(t);
          break;
        case 19:
          pe(Ul, t);
          break;
        case 10:
          qn(t.type, t);
          break;
        case 22:
        case 23:
          Yl(t), Ln(t), e !== null && pe(qr, t);
          break;
        case 24:
          qn(Ll, t);
      }
    }
    function _u(e) {
      return (e.mode & Pe) !== He;
    }
    function eg(e, t) {
      _u(e) ? (ol(), hc(t, e), ma()) : hc(t, e);
    }
    function Id(e, t, a) {
      _u(e) ? (ol(), ei(
        a,
        e,
        t
      ), ma()) : ei(
        a,
        e,
        t
      );
    }
    function hc(e, t) {
      try {
        var a = t.updateQueue, c = a !== null ? a.lastEffect : null;
        if (c !== null) {
          var o = c.next;
          a = o;
          do {
            if ((a.tag & e) === e && (c = void 0, (e & sn) !== yv && (gm = !0), c = oe(
              t,
              PE,
              a
            ), (e & sn) !== yv && (gm = !1), c !== void 0 && typeof c != "function")) {
              var f = void 0;
              f = (a.tag & nu) !== 0 ? "useLayoutEffect" : (a.tag & sn) !== 0 ? "useInsertionEffect" : "useEffect";
              var d = void 0;
              d = c === null ? " You returned null. If your effect does not require clean up, return undefined (or nothing)." : typeof c.then == "function" ? `

It looks like you wrote ` + f + `(async () => ...) or returned a Promise. Instead, write the async function inside your effect and call it immediately:

` + f + `(() => {
  async function fetchData() {
    // You can await here
    const response = await MyAPI.getData(someId);
    // ...
  }
  fetchData();
}, [someId]); // Or [] if effect doesn't need props or state

Learn more about data fetching with Hooks: https://react.dev/link/hooks-data-fetching` : " You returned: " + c, oe(
                t,
                function(h, y) {
                  console.error(
                    "%s must not return anything besides a function, which is used for clean-up.%s",
                    h,
                    y
                  );
                },
                f,
                d
              );
            }
            a = a.next;
          } while (a !== o);
        }
      } catch (h) {
        ke(t, t.return, h);
      }
    }
    function ei(e, t, a) {
      try {
        var c = t.updateQueue, o = c !== null ? c.lastEffect : null;
        if (o !== null) {
          var f = o.next;
          c = f;
          do {
            if ((c.tag & e) === e) {
              var d = c.inst, h = d.destroy;
              h !== void 0 && (d.destroy = void 0, (e & sn) !== yv && (gm = !0), o = t, oe(
                o,
                eT,
                o,
                a,
                h
              ), (e & sn) !== yv && (gm = !1));
            }
            c = c.next;
          } while (c !== f);
        }
      } catch (y) {
        ke(t, t.return, y);
      }
    }
    function Ps(e, t) {
      _u(e) ? (ol(), hc(t, e), ma()) : hc(t, e);
    }
    function Pd(e, t, a) {
      _u(e) ? (ol(), ei(
        a,
        e,
        t
      ), ma()) : ei(
        a,
        e,
        t
      );
    }
    function Ry(e) {
      var t = e.updateQueue;
      if (t !== null) {
        var a = e.stateNode;
        e.type.defaultProps || "ref" in e.memoizedProps || dm || (a.props !== e.memoizedProps && console.error(
          "Expected %s props to match memoized props before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.",
          se(e) || "instance"
        ), a.state !== e.memoizedState && console.error(
          "Expected %s state to match memoized state before processing the update queue. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.",
          se(e) || "instance"
        ));
        try {
          oe(
            e,
            Io,
            t,
            a
          );
        } catch (c) {
          ke(e, e.return, c);
        }
      }
    }
    function er(e, t, a) {
      return e.getSnapshotBeforeUpdate(t, a);
    }
    function tg(e, t) {
      var a = t.memoizedProps, c = t.memoizedState;
      t = e.stateNode, e.type.defaultProps || "ref" in e.memoizedProps || dm || (t.props !== e.memoizedProps && console.error(
        "Expected %s props to match memoized props before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.",
        se(e) || "instance"
      ), t.state !== e.memoizedState && console.error(
        "Expected %s state to match memoized state before getSnapshotBeforeUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.",
        se(e) || "instance"
      ));
      try {
        var o = Du(
          e.type,
          a
        ), f = oe(
          e,
          er,
          t,
          o,
          c
        );
        a = Wb, f !== void 0 || a.has(e.type) || (a.add(e.type), oe(e, function() {
          console.error(
            "%s.getSnapshotBeforeUpdate(): A snapshot value (or null) must be returned. You have returned undefined.",
            se(e)
          );
        })), t.__reactInternalSnapshotBeforeUpdate = f;
      } catch (d) {
        ke(e, e.return, d);
      }
    }
    function eh(e, t, a) {
      a.props = Du(
        e.type,
        e.memoizedProps
      ), a.state = e.memoizedState, _u(e) ? (ol(), oe(
        e,
        yb,
        e,
        t,
        a
      ), ma()) : oe(
        e,
        yb,
        e,
        t,
        a
      );
    }
    function lg(e) {
      var t = e.ref;
      if (t !== null) {
        switch (e.tag) {
          case 26:
          case 27:
          case 5:
            var a = e.stateNode;
            break;
          case 30:
            a = e.stateNode;
            break;
          default:
            a = e.stateNode;
        }
        if (typeof t == "function")
          if (_u(e))
            try {
              ol(), e.refCleanup = t(a);
            } finally {
              ma();
            }
          else e.refCleanup = t(a);
        else
          typeof t == "string" ? console.error("String refs are no longer supported.") : t.hasOwnProperty("current") || console.error(
            "Unexpected ref object provided for %s. Use either a ref-setter function or React.createRef().",
            se(e)
          ), t.current = a;
      }
    }
    function Pi(e, t) {
      try {
        oe(e, lg, e);
      } catch (a) {
        ke(e, t, a);
      }
    }
    function An(e, t) {
      var a = e.ref, c = e.refCleanup;
      if (a !== null)
        if (typeof c == "function")
          try {
            if (_u(e))
              try {
                ol(), oe(e, c);
              } finally {
                ma(e);
              }
            else oe(e, c);
          } catch (o) {
            ke(e, t, o);
          } finally {
            e.refCleanup = null, e = e.alternate, e != null && (e.refCleanup = null);
          }
        else if (typeof a == "function")
          try {
            if (_u(e))
              try {
                ol(), oe(e, a, null);
              } finally {
                ma(e);
              }
            else oe(e, a, null);
          } catch (o) {
            ke(e, t, o);
          }
        else a.current = null;
    }
    function _y(e, t, a, c) {
      var o = e.memoizedProps, f = o.id, d = o.onCommit;
      o = o.onRender, t = t === null ? "mount" : "update", fv && (t = "nested-update"), typeof o == "function" && o(
        f,
        t,
        e.actualDuration,
        e.treeBaseDuration,
        e.actualStartTime,
        a
      ), typeof d == "function" && d(f, t, c, a);
    }
    function ag(e, t, a, c) {
      var o = e.memoizedProps;
      e = o.id, o = o.onPostCommit, t = t === null ? "mount" : "update", fv && (t = "nested-update"), typeof o == "function" && o(
        e,
        t,
        c,
        a
      );
    }
    function ti(e) {
      var t = e.type, a = e.memoizedProps, c = e.stateNode;
      try {
        oe(
          e,
          pg,
          c,
          t,
          a,
          e
        );
      } catch (o) {
        ke(e, e.return, o);
      }
    }
    function th(e, t, a) {
      try {
        oe(
          e,
          Eh,
          e.stateNode,
          e.type,
          a,
          t,
          e
        );
      } catch (c) {
        ke(e, e.return, c);
      }
    }
    function My(e) {
      return e.tag === 5 || e.tag === 3 || e.tag === 26 || e.tag === 27 && oi(e.type) || e.tag === 4;
    }
    function lh(e) {
      e: for (; ; ) {
        for (; e.sibling === null; ) {
          if (e.return === null || My(e.return)) return null;
          e = e.return;
        }
        for (e.sibling.return = e.return, e = e.sibling; e.tag !== 5 && e.tag !== 6 && e.tag !== 18; ) {
          if (e.tag === 27 && oi(e.type) || e.flags & 2 || e.child === null || e.tag === 4) continue e;
          e.child.return = e, e = e.child;
        }
        if (!(e.flags & 2)) return e.stateNode;
      }
    }
    function df(e, t, a) {
      var c = e.tag;
      if (c === 5 || c === 6)
        e = e.stateNode, t ? (vg(a), (a.nodeType === 9 ? a.body : a.nodeName === "HTML" ? a.ownerDocument.body : a).insertBefore(e, t)) : (vg(a), t = a.nodeType === 9 ? a.body : a.nodeName === "HTML" ? a.ownerDocument.body : a, t.appendChild(e), a = a._reactRootContainer, a != null || t.onclick !== null || (t.onclick = yn));
      else if (c !== 4 && (c === 27 && oi(e.type) && (a = e.stateNode, t = null), e = e.child, e !== null))
        for (df(e, t, a), e = e.sibling; e !== null; )
          df(e, t, a), e = e.sibling;
    }
    function tr(e, t, a) {
      var c = e.tag;
      if (c === 5 || c === 6)
        e = e.stateNode, t ? a.insertBefore(e, t) : a.appendChild(e);
      else if (c !== 4 && (c === 27 && oi(e.type) && (a = e.stateNode), e = e.child, e !== null))
        for (tr(e, t, a), e = e.sibling; e !== null; )
          tr(e, t, a), e = e.sibling;
    }
    function Cy(e) {
      for (var t, a = e.return; a !== null; ) {
        if (My(a)) {
          t = a;
          break;
        }
        a = a.return;
      }
      if (t == null)
        throw Error(
          "Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue."
        );
      switch (t.tag) {
        case 27:
          t = t.stateNode, a = lh(e), tr(
            e,
            a,
            t
          );
          break;
        case 5:
          a = t.stateNode, t.flags & 32 && (Th(a), t.flags &= -33), t = lh(e), tr(
            e,
            t,
            a
          );
          break;
        case 3:
        case 4:
          t = t.stateNode.containerInfo, a = lh(e), df(
            e,
            a,
            t
          );
          break;
        default:
          throw Error(
            "Invalid host parent fiber. This error is likely caused by a bug in React. Please file an issue."
          );
      }
    }
    function Uy(e) {
      var t = e.stateNode, a = e.memoizedProps;
      try {
        oe(
          e,
          Bu,
          e.type,
          a,
          t,
          e
        );
      } catch (c) {
        ke(e, e.return, c);
      }
    }
    function xy(e, t) {
      return t.tag === 31 ? (t = t.memoizedState, e.memoizedState !== null && t === null) : t.tag === 13 ? (e = e.memoizedState, t = t.memoizedState, e !== null && e.dehydrated !== null && (t === null || t.dehydrated === null)) : t.tag === 3 ? e.memoizedState.isDehydrated && (t.flags & 256) === 0 : !1;
    }
    function i1(e, t) {
      if (e = e.containerInfo, gS = Qv, e = gd(e), wm(e)) {
        if ("selectionStart" in e)
          var a = {
            start: e.selectionStart,
            end: e.selectionEnd
          };
        else
          e: {
            a = (a = e.ownerDocument) && a.defaultView || window;
            var c = a.getSelection && a.getSelection();
            if (c && c.rangeCount !== 0) {
              a = c.anchorNode;
              var o = c.anchorOffset, f = c.focusNode;
              c = c.focusOffset;
              try {
                a.nodeType, f.nodeType;
              } catch {
                a = null;
                break e;
              }
              var d = 0, h = -1, y = -1, p = 0, z = 0, _ = e, E = null;
              t: for (; ; ) {
                for (var Y; _ !== a || o !== 0 && _.nodeType !== 3 || (h = d + o), _ !== f || c !== 0 && _.nodeType !== 3 || (y = d + c), _.nodeType === 3 && (d += _.nodeValue.length), (Y = _.firstChild) !== null; )
                  E = _, _ = Y;
                for (; ; ) {
                  if (_ === e) break t;
                  if (E === a && ++p === o && (h = d), E === f && ++z === c && (y = d), (Y = _.nextSibling) !== null) break;
                  _ = E, E = _.parentNode;
                }
                _ = Y;
              }
              a = h === -1 || y === -1 ? null : { start: h, end: y };
            } else a = null;
          }
        a = a || { start: 0, end: 0 };
      } else a = null;
      for (vS = {
        focusedElem: e,
        selectionRange: a
      }, Qv = !1, fa = t; fa !== null; )
        if (t = fa, e = t.child, (t.subtreeFlags & 1028) !== 0 && e !== null)
          e.return = t, fa = e;
        else
          for (; fa !== null; ) {
            switch (e = t = fa, a = e.alternate, o = e.flags, e.tag) {
              case 0:
                if ((o & 4) !== 0 && (e = e.updateQueue, e = e !== null ? e.events : null, e !== null))
                  for (a = 0; a < e.length; a++)
                    o = e[a], o.ref.impl = o.nextImpl;
                break;
              case 11:
              case 15:
                break;
              case 1:
                (o & 1024) !== 0 && a !== null && tg(e, a);
                break;
              case 3:
                if ((o & 1024) !== 0) {
                  if (e = e.stateNode.containerInfo, a = e.nodeType, a === 9)
                    zf(e);
                  else if (a === 1)
                    switch (e.nodeName) {
                      case "HEAD":
                      case "HTML":
                      case "BODY":
                        zf(e);
                        break;
                      default:
                        e.textContent = "";
                    }
                }
                break;
              case 5:
              case 26:
              case 27:
              case 6:
              case 4:
              case 17:
                break;
              default:
                if ((o & 1024) !== 0)
                  throw Error(
                    "This unit of work tag should not have side-effects. This error is likely caused by a bug in React. Please file an issue."
                  );
            }
            if (e = t.sibling, e !== null) {
              e.return = t.return, fa = e;
              break;
            }
            fa = t.return;
          }
    }
    function ah(e, t, a) {
      var c = Ft(), o = Sn(), f = Ja(), d = bn(), h = a.flags;
      switch (a.tag) {
        case 0:
        case 11:
        case 15:
          Pa(e, a), h & 4 && eg(a, nu | ku);
          break;
        case 1:
          if (Pa(e, a), h & 4)
            if (e = a.stateNode, t === null)
              a.type.defaultProps || "ref" in a.memoizedProps || dm || (e.props !== a.memoizedProps && console.error(
                "Expected %s props to match memoized props before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.",
                se(a) || "instance"
              ), e.state !== a.memoizedState && console.error(
                "Expected %s state to match memoized state before componentDidMount. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.",
                se(a) || "instance"
              )), _u(a) ? (ol(), oe(
                a,
                w1,
                a,
                e
              ), ma()) : oe(
                a,
                w1,
                a,
                e
              );
            else {
              var y = Du(
                a.type,
                t.memoizedProps
              );
              t = t.memoizedState, a.type.defaultProps || "ref" in a.memoizedProps || dm || (e.props !== a.memoizedProps && console.error(
                "Expected %s props to match memoized props before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.props`. Please file an issue.",
                se(a) || "instance"
              ), e.state !== a.memoizedState && console.error(
                "Expected %s state to match memoized state before componentDidUpdate. This might either be because of a bug in React, or because a component reassigns its own `this.state`. Please file an issue.",
                se(a) || "instance"
              )), _u(a) ? (ol(), oe(
                a,
                db,
                a,
                e,
                y,
                t,
                e.__reactInternalSnapshotBeforeUpdate
              ), ma()) : oe(
                a,
                db,
                a,
                e,
                y,
                t,
                e.__reactInternalSnapshotBeforeUpdate
              );
            }
          h & 64 && Ry(a), h & 512 && Pi(a, a.return);
          break;
        case 3:
          if (t = gu(), Pa(e, a), h & 64 && (h = a.updateQueue, h !== null)) {
            if (y = null, a.child !== null)
              switch (a.child.tag) {
                case 27:
                case 5:
                  y = a.child.stateNode;
                  break;
                case 1:
                  y = a.child.stateNode;
              }
            try {
              oe(
                a,
                Io,
                h,
                y
              );
            } catch (z) {
              ke(a, a.return, z);
            }
          }
          e.effectDuration += $o(t);
          break;
        case 27:
          t === null && h & 4 && Uy(a);
        case 26:
        case 5:
          if (Pa(e, a), t === null) {
            if (h & 4) ti(a);
            else if (h & 64) {
              e = a.type, t = a.memoizedProps, y = a.stateNode;
              try {
                oe(
                  a,
                  gg,
                  y,
                  e,
                  t,
                  a
                );
              } catch (z) {
                ke(
                  a,
                  a.return,
                  z
                );
              }
            }
          }
          h & 512 && Pi(a, a.return);
          break;
        case 12:
          if (h & 4) {
            h = gu(), Pa(e, a), e = a.stateNode, e.effectDuration += ha(h);
            try {
              oe(
                a,
                _y,
                a,
                t,
                $f,
                e.effectDuration
              );
            } catch (z) {
              ke(a, a.return, z);
            }
          } else Pa(e, a);
          break;
        case 31:
          Pa(e, a), h & 4 && Hy(e, a);
          break;
        case 13:
          Pa(e, a), h & 4 && jy(e, a), h & 64 && (e = a.memoizedState, e !== null && (e = e.dehydrated, e !== null && (h = yc.bind(
            null,
            a
          ), Mg(e, h))));
          break;
        case 22:
          if (h = a.memoizedState !== null || Do, !h) {
            t = t !== null && t.memoizedState !== null || Jl, y = Do;
            var p = Jl;
            Do = h, (Jl = t) && !p ? (Jn(
              e,
              a,
              (a.subtreeFlags & 8772) !== 0
            ), (a.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && vd(
              a,
              ze,
              Ue
            )) : Pa(e, a), Do = y, Jl = p;
          }
          break;
        case 30:
          break;
        default:
          Pa(e, a);
      }
      (a.mode & Pe) !== He && 0 <= ze && 0 <= Ue && ((Sl || 0.05 < rl) && Bn(
        a,
        ze,
        Ue,
        rl,
        il
      ), a.alternate === null && a.return !== null && a.return.alternate !== null && 0.05 < Ue - ze && (xy(
        a.return.alternate,
        a.return
      ) || pn(
        a,
        ze,
        Ue,
        "Mount"
      ))), jl(c), Za(o), il = f, Sl = d;
    }
    function gl(e) {
      var t = e.alternate;
      t !== null && (e.alternate = null, gl(t)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (t = e.stateNode, t !== null && M(t)), e.stateNode = null, e._debugOwner = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
    }
    function kt(e, t, a) {
      for (a = a.child; a !== null; )
        Ny(
          e,
          t,
          a
        ), a = a.sibling;
    }
    function Ny(e, t, a) {
      if (Ml && typeof Ml.onCommitFiberUnmount == "function")
        try {
          Ml.onCommitFiberUnmount(ho, a);
        } catch (p) {
          qu || (qu = !0, console.error(
            "React instrumentation encountered an error: %o",
            p
          ));
        }
      var c = Ft(), o = Sn(), f = Ja(), d = bn();
      switch (a.tag) {
        case 26:
          Jl || An(a, t), kt(
            e,
            t,
            a
          ), a.memoizedState ? a.memoizedState.count-- : a.stateNode && (e = a.stateNode, e.parentNode.removeChild(e));
          break;
        case 27:
          Jl || An(a, t);
          var h = Kl, y = _n;
          oi(a.type) && (Kl = a.stateNode, _n = !1), kt(
            e,
            t,
            a
          ), oe(
            a,
            Sc,
            a.stateNode
          ), Kl = h, _n = y;
          break;
        case 5:
          Jl || An(a, t);
        case 6:
          if (h = Kl, y = _n, Kl = null, kt(
            e,
            t,
            a
          ), Kl = h, _n = y, Kl !== null)
            if (_n)
              try {
                oe(
                  a,
                  bg,
                  Kl,
                  a.stateNode
                );
              } catch (p) {
                ke(
                  a,
                  t,
                  p
                );
              }
            else
              try {
                oe(
                  a,
                  Sg,
                  Kl,
                  a.stateNode
                );
              } catch (p) {
                ke(
                  a,
                  t,
                  p
                );
              }
          break;
        case 18:
          Kl !== null && (_n ? (e = Kl, no(
            e.nodeType === 9 ? e.body : e.nodeName === "HTML" ? e.ownerDocument.body : e,
            a.stateNode
          ), oo(e)) : no(Kl, a.stateNode));
          break;
        case 4:
          h = Kl, y = _n, Kl = a.stateNode.containerInfo, _n = !0, kt(
            e,
            t,
            a
          ), Kl = h, _n = y;
          break;
        case 0:
        case 11:
        case 14:
        case 15:
          ei(
            sn,
            a,
            t
          ), Jl || Id(
            a,
            t,
            nu
          ), kt(
            e,
            t,
            a
          );
          break;
        case 1:
          Jl || (An(a, t), h = a.stateNode, typeof h.componentWillUnmount == "function" && eh(
            a,
            t,
            h
          )), kt(
            e,
            t,
            a
          );
          break;
        case 21:
          kt(
            e,
            t,
            a
          );
          break;
        case 22:
          Jl = (h = Jl) || a.memoizedState !== null, kt(
            e,
            t,
            a
          ), Jl = h;
          break;
        default:
          kt(
            e,
            t,
            a
          );
      }
      (a.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
        a,
        ze,
        Ue,
        rl,
        il
      ), jl(c), Za(o), il = f, Sl = d;
    }
    function Hy(e, t) {
      if (t.memoizedState === null && (e = t.alternate, e !== null && (e = e.memoizedState, e !== null))) {
        e = e.dehydrated;
        try {
          oe(
            t,
            Ah,
            e
          );
        } catch (a) {
          ke(t, t.return, a);
        }
      }
    }
    function jy(e, t) {
      if (t.memoizedState === null && (e = t.alternate, e !== null && (e = e.memoizedState, e !== null && (e = e.dehydrated, e !== null))))
        try {
          oe(
            t,
            l0,
            e
          );
        } catch (a) {
          ke(t, t.return, a);
        }
    }
    function ng(e) {
      switch (e.tag) {
        case 31:
        case 13:
        case 19:
          var t = e.stateNode;
          return t === null && (t = e.stateNode = new Fb()), t;
        case 22:
          return e = e.stateNode, t = e._retryCache, t === null && (t = e._retryCache = new Fb()), t;
        default:
          throw Error(
            "Unexpected Suspense handler tag (" + e.tag + "). This is a bug in React."
          );
      }
    }
    function li(e, t) {
      var a = ng(e);
      t.forEach(function(c) {
        if (!a.has(c)) {
          if (a.add(c), wu)
            if (hm !== null && mm !== null)
              vf(mm, hm);
            else
              throw Error(
                "Expected finished root and lanes to be set. This is a bug in React."
              );
          var o = lo.bind(null, e, c);
          c.then(o, o);
        }
      });
    }
    function Sa(e, t) {
      var a = t.deletions;
      if (a !== null)
        for (var c = 0; c < a.length; c++) {
          var o = e, f = t, d = a[c], h = Ft(), y = f;
          e: for (; y !== null; ) {
            switch (y.tag) {
              case 27:
                if (oi(y.type)) {
                  Kl = y.stateNode, _n = !1;
                  break e;
                }
                break;
              case 5:
                Kl = y.stateNode, _n = !1;
                break e;
              case 3:
              case 4:
                Kl = y.stateNode.containerInfo, _n = !0;
                break e;
            }
            y = y.return;
          }
          if (Kl === null)
            throw Error(
              "Expected to find a host parent. This error is likely caused by a bug in React. Please file an issue."
            );
          Ny(o, f, d), Kl = null, _n = !1, (d.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && pn(
            d,
            ze,
            Ue,
            "Unmount"
          ), jl(h), o = d, f = o.alternate, f !== null && (f.return = null), o.return = null;
        }
      if (t.subtreeFlags & 13886)
        for (t = t.child; t !== null; )
          lr(t, e), t = t.sibling;
    }
    function lr(e, t) {
      var a = Ft(), c = Sn(), o = Ja(), f = bn(), d = e.alternate, h = e.flags;
      switch (e.tag) {
        case 0:
        case 11:
        case 14:
        case 15:
          Sa(t, e), ba(e), h & 4 && (ei(
            sn | ku,
            e,
            e.return
          ), hc(sn | ku, e), Id(
            e,
            e.return,
            nu | ku
          ));
          break;
        case 1:
          if (Sa(t, e), ba(e), h & 512 && (Jl || d === null || An(d, d.return)), h & 64 && Do && (h = e.updateQueue, h !== null && (d = h.callbacks, d !== null))) {
            var y = h.shared.hiddenCallbacks;
            h.shared.hiddenCallbacks = y === null ? d : y.concat(d);
          }
          break;
        case 26:
          if (y = zc, Sa(t, e), ba(e), h & 512 && (Jl || d === null || An(d, d.return)), h & 4) {
            var p = d !== null ? d.memoizedState : null;
            if (h = e.memoizedState, d === null)
              if (h === null)
                if (e.stateNode === null) {
                  e: {
                    h = e.type, d = e.memoizedProps, y = y.ownerDocument || y;
                    t: switch (h) {
                      case "title":
                        p = y.getElementsByTagName(
                          "title"
                        )[0], (!p || p[Gf] || p[el] || p.namespaceURI === We || p.hasAttribute("itemprop")) && (p = y.createElement(h), y.head.insertBefore(
                          p,
                          y.querySelector(
                            "head > title"
                          )
                        )), Pt(p, h, d), p[el] = e, me(p), h = p;
                        break e;
                      case "link":
                        var z = _f(
                          "link",
                          "href",
                          y
                        ).get(h + (d.href || ""));
                        if (z) {
                          for (var _ = 0; _ < z.length; _++)
                            if (p = z[_], p.getAttribute("href") === (d.href == null || d.href === "" ? null : d.href) && p.getAttribute("rel") === (d.rel == null ? null : d.rel) && p.getAttribute("title") === (d.title == null ? null : d.title) && p.getAttribute("crossorigin") === (d.crossOrigin == null ? null : d.crossOrigin)) {
                              z.splice(_, 1);
                              break t;
                            }
                        }
                        p = y.createElement(h), Pt(p, h, d), y.head.appendChild(
                          p
                        );
                        break;
                      case "meta":
                        if (z = _f(
                          "meta",
                          "content",
                          y
                        ).get(h + (d.content || ""))) {
                          for (_ = 0; _ < z.length; _++)
                            if (p = z[_], vt(
                              d.content,
                              "content"
                            ), p.getAttribute("content") === (d.content == null ? null : "" + d.content) && p.getAttribute("name") === (d.name == null ? null : d.name) && p.getAttribute("property") === (d.property == null ? null : d.property) && p.getAttribute("http-equiv") === (d.httpEquiv == null ? null : d.httpEquiv) && p.getAttribute("charset") === (d.charSet == null ? null : d.charSet)) {
                              z.splice(_, 1);
                              break t;
                            }
                        }
                        p = y.createElement(h), Pt(p, h, d), y.head.appendChild(
                          p
                        );
                        break;
                      default:
                        throw Error(
                          'getNodesForType encountered a type it did not expect: "' + h + '". This is a bug in React.'
                        );
                    }
                    p[el] = e, me(p), h = p;
                  }
                  e.stateNode = h;
                } else
                  Ng(
                    y,
                    e.type,
                    e.stateNode
                  );
              else
                e.stateNode = Dh(
                  y,
                  h,
                  e.memoizedProps
                );
            else
              p !== h ? (p === null ? d.stateNode !== null && (d = d.stateNode, d.parentNode.removeChild(d)) : p.count--, h === null ? Ng(
                y,
                e.type,
                e.stateNode
              ) : Dh(
                y,
                h,
                e.memoizedProps
              )) : h === null && e.stateNode !== null && th(
                e,
                e.memoizedProps,
                d.memoizedProps
              );
          }
          break;
        case 27:
          Sa(t, e), ba(e), h & 512 && (Jl || d === null || An(d, d.return)), d !== null && h & 4 && th(
            e,
            e.memoizedProps,
            d.memoizedProps
          );
          break;
        case 5:
          if (Sa(t, e), ba(e), h & 512 && (Jl || d === null || An(d, d.return)), e.flags & 32) {
            y = e.stateNode;
            try {
              oe(
                e,
                Th,
                y
              );
            } catch (fe) {
              ke(e, e.return, fe);
            }
          }
          h & 4 && e.stateNode != null && (y = e.memoizedProps, th(
            e,
            y,
            d !== null ? d.memoizedProps : y
          )), h & 1024 && (I1 = !0, e.type !== "form" && console.error(
            "Unexpected host component type. Expected a form. This is a bug in React."
          ));
          break;
        case 6:
          if (Sa(t, e), ba(e), h & 4) {
            if (e.stateNode === null)
              throw Error(
                "This should have a text node initialized. This error is likely caused by a bug in React. Please file an issue."
              );
            h = e.memoizedProps, d = d !== null ? d.memoizedProps : h, y = e.stateNode;
            try {
              oe(
                e,
                o1,
                y,
                d,
                h
              );
            } catch (fe) {
              ke(e, e.return, fe);
            }
          }
          break;
        case 3:
          if (y = gu(), Gv = null, p = zc, zc = Oh(t.containerInfo), Sa(t, e), zc = p, ba(e), h & 4 && d !== null && d.memoizedState.isDehydrated)
            try {
              oe(
                e,
                t0,
                t.containerInfo
              );
            } catch (fe) {
              ke(e, e.return, fe);
            }
          I1 && (I1 = !1, ug(e)), t.effectDuration += $o(
            y
          );
          break;
        case 4:
          h = zc, zc = Oh(
            e.stateNode.containerInfo
          ), Sa(t, e), ba(e), zc = h;
          break;
        case 12:
          h = gu(), Sa(t, e), ba(e), e.stateNode.effectDuration += ha(h);
          break;
        case 31:
          Sa(t, e), ba(e), h & 4 && (h = e.updateQueue, h !== null && (e.updateQueue = null, li(e, h)));
          break;
        case 13:
          Sa(t, e), ba(e), e.child.flags & 8192 && e.memoizedState !== null != (d !== null && d.memoizedState !== null) && (zv = Xl()), h & 4 && (h = e.updateQueue, h !== null && (e.updateQueue = null, li(e, h)));
          break;
        case 22:
          y = e.memoizedState !== null;
          var E = d !== null && d.memoizedState !== null, Y = Do, ue = Jl;
          if (Do = Y || y, Jl = ue || E, Sa(t, e), Jl = ue, Do = Y, E && !y && !Y && !ue && (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && vd(
            e,
            ze,
            Ue
          ), ba(e), h & 8192)
            e: for (t = e.stateNode, t._visibility = y ? t._visibility & ~Y0 : t._visibility | Y0, !y || d === null || E || Do || Jl || (ai(e), (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && pn(
              e,
              ze,
              Ue,
              "Disconnect"
            )), d = null, t = e; ; ) {
              if (t.tag === 5 || t.tag === 26) {
                if (d === null) {
                  E = d = t;
                  try {
                    p = E.stateNode, y ? oe(
                      E,
                      Tg,
                      p
                    ) : oe(
                      E,
                      zg,
                      E.stateNode,
                      E.memoizedProps
                    );
                  } catch (fe) {
                    ke(E, E.return, fe);
                  }
                }
              } else if (t.tag === 6) {
                if (d === null) {
                  E = t;
                  try {
                    z = E.stateNode, y ? oe(
                      E,
                      Ag,
                      z
                    ) : oe(
                      E,
                      Dg,
                      z,
                      E.memoizedProps
                    );
                  } catch (fe) {
                    ke(E, E.return, fe);
                  }
                }
              } else if (t.tag === 18) {
                if (d === null) {
                  E = t;
                  try {
                    _ = E.stateNode, y ? oe(
                      E,
                      Eg,
                      _
                    ) : oe(
                      E,
                      Og,
                      E.stateNode
                    );
                  } catch (fe) {
                    ke(E, E.return, fe);
                  }
                }
              } else if ((t.tag !== 22 && t.tag !== 23 || t.memoizedState === null || t === e) && t.child !== null) {
                t.child.return = t, t = t.child;
                continue;
              }
              if (t === e) break e;
              for (; t.sibling === null; ) {
                if (t.return === null || t.return === e)
                  break e;
                d === t && (d = null), t = t.return;
              }
              d === t && (d = null), t.sibling.return = t.return, t = t.sibling;
            }
          h & 4 && (h = e.updateQueue, h !== null && (d = h.retryQueue, d !== null && (h.retryQueue = null, li(e, d))));
          break;
        case 19:
          Sa(t, e), ba(e), h & 4 && (h = e.updateQueue, h !== null && (e.updateQueue = null, li(e, h)));
          break;
        case 30:
          break;
        case 21:
          break;
        default:
          Sa(t, e), ba(e);
      }
      (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && ((Sl || 0.05 < rl) && Bn(
        e,
        ze,
        Ue,
        rl,
        il
      ), e.alternate === null && e.return !== null && e.return.alternate !== null && 0.05 < Ue - ze && (xy(
        e.return.alternate,
        e.return
      ) || pn(
        e,
        ze,
        Ue,
        "Mount"
      ))), jl(a), Za(c), il = o, Sl = f;
    }
    function ba(e) {
      var t = e.flags;
      if (t & 2) {
        try {
          oe(e, Cy, e);
        } catch (a) {
          ke(e, e.return, a);
        }
        e.flags &= -3;
      }
      t & 4096 && (e.flags &= -4097);
    }
    function ug(e) {
      if (e.subtreeFlags & 1024)
        for (e = e.child; e !== null; ) {
          var t = e;
          ug(t), t.tag === 5 && t.flags & 1024 && t.stateNode.reset(), e = e.sibling;
        }
    }
    function Pa(e, t) {
      if (t.subtreeFlags & 8772)
        for (t = t.child; t !== null; )
          ah(e, t.alternate, t), t = t.sibling;
    }
    function nh(e) {
      var t = Ft(), a = Sn(), c = Ja(), o = bn();
      switch (e.tag) {
        case 0:
        case 11:
        case 14:
        case 15:
          Id(
            e,
            e.return,
            nu
          ), ai(e);
          break;
        case 1:
          An(e, e.return);
          var f = e.stateNode;
          typeof f.componentWillUnmount == "function" && eh(
            e,
            e.return,
            f
          ), ai(e);
          break;
        case 27:
          oe(
            e,
            Sc,
            e.stateNode
          );
        case 26:
        case 5:
          An(e, e.return), ai(e);
          break;
        case 22:
          e.memoizedState === null && ai(e);
          break;
        case 30:
          ai(e);
          break;
        default:
          ai(e);
      }
      (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
        e,
        ze,
        Ue,
        rl,
        il
      ), jl(t), Za(a), il = c, Sl = o;
    }
    function ai(e) {
      for (e = e.child; e !== null; )
        nh(e), e = e.sibling;
    }
    function By(e, t, a, c) {
      var o = Ft(), f = Sn(), d = Ja(), h = bn(), y = a.flags;
      switch (a.tag) {
        case 0:
        case 11:
        case 15:
          Jn(
            e,
            a,
            c
          ), eg(a, nu);
          break;
        case 1:
          if (Jn(
            e,
            a,
            c
          ), t = a.stateNode, typeof t.componentDidMount == "function" && oe(
            a,
            w1,
            a,
            t
          ), t = a.updateQueue, t !== null) {
            e = a.stateNode;
            try {
              oe(
                a,
                ay,
                t,
                e
              );
            } catch (p) {
              ke(a, a.return, p);
            }
          }
          c && y & 64 && Ry(a), Pi(a, a.return);
          break;
        case 27:
          Uy(a);
        case 26:
        case 5:
          Jn(
            e,
            a,
            c
          ), c && t === null && y & 4 && ti(a), Pi(a, a.return);
          break;
        case 12:
          if (c && y & 4) {
            y = gu(), Jn(
              e,
              a,
              c
            ), c = a.stateNode, c.effectDuration += ha(y);
            try {
              oe(
                a,
                _y,
                a,
                t,
                $f,
                c.effectDuration
              );
            } catch (p) {
              ke(a, a.return, p);
            }
          } else
            Jn(
              e,
              a,
              c
            );
          break;
        case 31:
          Jn(
            e,
            a,
            c
          ), c && y & 4 && Hy(e, a);
          break;
        case 13:
          Jn(
            e,
            a,
            c
          ), c && y & 4 && jy(e, a);
          break;
        case 22:
          a.memoizedState === null && Jn(
            e,
            a,
            c
          ), Pi(a, a.return);
          break;
        case 30:
          break;
        default:
          Jn(
            e,
            a,
            c
          );
      }
      (a.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
        a,
        ze,
        Ue,
        rl,
        il
      ), jl(o), Za(f), il = d, Sl = h;
    }
    function Jn(e, t, a) {
      for (a = a && (t.subtreeFlags & 8772) !== 0, t = t.child; t !== null; )
        By(
          e,
          t.alternate,
          t,
          a
        ), t = t.sibling;
    }
    function ar(e, t) {
      var a = null;
      e !== null && e.memoizedState !== null && e.memoizedState.cachePool !== null && (a = e.memoizedState.cachePool.pool), e = null, t.memoizedState !== null && t.memoizedState.cachePool !== null && (e = t.memoizedState.cachePool.pool), e !== a && (e != null && Bi(e), a != null && Ms(a));
    }
    function nr(e, t) {
      e = null, t.alternate !== null && (e = t.alternate.memoizedState.cache), t = t.memoizedState.cache, t !== e && (Bi(t), e != null && Ms(e));
    }
    function en(e, t, a, c, o) {
      if (t.subtreeFlags & 10256 || t.actualDuration !== 0 && (t.alternate === null || t.alternate.child !== t.child))
        for (t = t.child; t !== null; ) {
          var f = t.sibling;
          Yy(
            e,
            t,
            a,
            c,
            f !== null ? f.actualStartTime : o
          ), t = f;
        }
    }
    function Yy(e, t, a, c, o) {
      var f = Ft(), d = Sn(), h = Ja(), y = bn(), p = Vf, z = t.flags;
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          (t.mode & Pe) !== He && 0 < t.actualStartTime && (t.flags & 1) !== 0 && Sd(
            t,
            t.actualStartTime,
            o,
            Pl,
            a
          ), en(
            e,
            t,
            a,
            c,
            o
          ), z & 2048 && Ps(t, rn | ku);
          break;
        case 1:
          (t.mode & Pe) !== He && 0 < t.actualStartTime && ((t.flags & 128) !== 0 ? Xm(
            t,
            t.actualStartTime,
            o,
            []
          ) : (t.flags & 1) !== 0 && Sd(
            t,
            t.actualStartTime,
            o,
            Pl,
            a
          )), en(
            e,
            t,
            a,
            c,
            o
          );
          break;
        case 3:
          var _ = gu(), E = Pl;
          Pl = t.alternate !== null && t.alternate.memoizedState.isDehydrated && (t.flags & 256) === 0, en(
            e,
            t,
            a,
            c,
            o
          ), Pl = E, z & 2048 && (a = null, t.alternate !== null && (a = t.alternate.memoizedState.cache), c = t.memoizedState.cache, c !== a && (Bi(c), a != null && Ms(a))), e.passiveEffectDuration += $o(
            _
          );
          break;
        case 12:
          if (z & 2048) {
            z = gu(), en(
              e,
              t,
              a,
              c,
              o
            ), e = t.stateNode, e.passiveEffectDuration += ha(z);
            try {
              oe(
                t,
                ag,
                t,
                t.alternate,
                $f,
                e.passiveEffectDuration
              );
            } catch (Y) {
              ke(t, t.return, Y);
            }
          } else
            en(
              e,
              t,
              a,
              c,
              o
            );
          break;
        case 31:
          z = Pl, _ = t.alternate !== null ? t.alternate.memoizedState : null, E = t.memoizedState, _ !== null && E === null ? (E = t.deletions, E !== null && 0 < E.length && E[0].tag === 18 ? (Pl = !1, _ = _.hydrationErrors, _ !== null && Xm(
            t,
            t.actualStartTime,
            o,
            _
          )) : Pl = !0) : Pl = !1, en(
            e,
            t,
            a,
            c,
            o
          ), Pl = z;
          break;
        case 13:
          z = Pl, _ = t.alternate !== null ? t.alternate.memoizedState : null, E = t.memoizedState, _ === null || _.dehydrated === null || E !== null && E.dehydrated !== null ? Pl = !1 : (E = t.deletions, E !== null && 0 < E.length && E[0].tag === 18 ? (Pl = !1, _ = _.hydrationErrors, _ !== null && Xm(
            t,
            t.actualStartTime,
            o,
            _
          )) : Pl = !0), en(
            e,
            t,
            a,
            c,
            o
          ), Pl = z;
          break;
        case 23:
          break;
        case 22:
          E = t.stateNode, _ = t.alternate, t.memoizedState !== null ? E._visibility & po ? en(
            e,
            t,
            a,
            c,
            o
          ) : eo(
            e,
            t,
            a,
            c,
            o
          ) : E._visibility & po ? en(
            e,
            t,
            a,
            c,
            o
          ) : (E._visibility |= po, ni(
            e,
            t,
            a,
            c,
            (t.subtreeFlags & 10256) !== 0 || t.actualDuration !== 0 && (t.alternate === null || t.alternate.child !== t.child),
            o
          ), (t.mode & Pe) === He || Pl || (e = t.actualStartTime, 0 <= e && 0.05 < o - e && vd(t, e, o), 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && vd(
            t,
            ze,
            Ue
          ))), z & 2048 && ar(
            _,
            t
          );
          break;
        case 24:
          en(
            e,
            t,
            a,
            c,
            o
          ), z & 2048 && nr(t.alternate, t);
          break;
        default:
          en(
            e,
            t,
            a,
            c,
            o
          );
      }
      (t.mode & Pe) !== He && ((e = !Pl && t.alternate === null && t.return !== null && t.return.alternate !== null) && (a = t.actualStartTime, 0 <= a && 0.05 < o - a && pn(
        t,
        a,
        o,
        "Mount"
      )), 0 <= ze && 0 <= Ue && ((Sl || 0.05 < rl) && Bn(
        t,
        ze,
        Ue,
        rl,
        il
      ), e && 0.05 < Ue - ze && pn(
        t,
        ze,
        Ue,
        "Mount"
      ))), jl(f), Za(d), il = h, Sl = y, Vf = p;
    }
    function ni(e, t, a, c, o, f) {
      for (o = o && ((t.subtreeFlags & 10256) !== 0 || t.actualDuration !== 0 && (t.alternate === null || t.alternate.child !== t.child)), t = t.child; t !== null; ) {
        var d = t.sibling;
        ur(
          e,
          t,
          a,
          c,
          o,
          d !== null ? d.actualStartTime : f
        ), t = d;
      }
    }
    function ur(e, t, a, c, o, f) {
      var d = Ft(), h = Sn(), y = Ja(), p = bn(), z = Vf;
      o && (t.mode & Pe) !== He && 0 < t.actualStartTime && (t.flags & 1) !== 0 && Sd(
        t,
        t.actualStartTime,
        f,
        Pl,
        a
      );
      var _ = t.flags;
      switch (t.tag) {
        case 0:
        case 11:
        case 15:
          ni(
            e,
            t,
            a,
            c,
            o,
            f
          ), Ps(t, rn);
          break;
        case 23:
          break;
        case 22:
          var E = t.stateNode;
          t.memoizedState !== null ? E._visibility & po ? ni(
            e,
            t,
            a,
            c,
            o,
            f
          ) : eo(
            e,
            t,
            a,
            c,
            f
          ) : (E._visibility |= po, ni(
            e,
            t,
            a,
            c,
            o,
            f
          )), o && _ & 2048 && ar(
            t.alternate,
            t
          );
          break;
        case 24:
          ni(
            e,
            t,
            a,
            c,
            o,
            f
          ), o && _ & 2048 && nr(t.alternate, t);
          break;
        default:
          ni(
            e,
            t,
            a,
            c,
            o,
            f
          );
      }
      (t.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
        t,
        ze,
        Ue,
        rl,
        il
      ), jl(d), Za(h), il = y, Sl = p, Vf = z;
    }
    function eo(e, t, a, c, o) {
      if (t.subtreeFlags & 10256 || t.actualDuration !== 0 && (t.alternate === null || t.alternate.child !== t.child))
        for (var f = t.child; f !== null; ) {
          t = f.sibling;
          var d = e, h = a, y = c, p = t !== null ? t.actualStartTime : o, z = Vf;
          (f.mode & Pe) !== He && 0 < f.actualStartTime && (f.flags & 1) !== 0 && Sd(
            f,
            f.actualStartTime,
            p,
            Pl,
            h
          );
          var _ = f.flags;
          switch (f.tag) {
            case 22:
              eo(
                d,
                f,
                h,
                y,
                p
              ), _ & 2048 && ar(f.alternate, f);
              break;
            case 24:
              eo(
                d,
                f,
                h,
                y,
                p
              ), _ & 2048 && nr(f.alternate, f);
              break;
            default:
              eo(
                d,
                f,
                h,
                y,
                p
              );
          }
          Vf = z, f = t;
        }
    }
    function to(e, t, a) {
      if (e.subtreeFlags & ap)
        for (e = e.child; e !== null; )
          uh(
            e,
            t,
            a
          ), e = e.sibling;
    }
    function uh(e, t, a) {
      switch (e.tag) {
        case 26:
          to(
            e,
            t,
            a
          ), e.flags & ap && e.memoizedState !== null && i0(
            a,
            zc,
            e.memoizedState,
            e.memoizedProps
          );
          break;
        case 5:
          to(
            e,
            t,
            a
          );
          break;
        case 3:
        case 4:
          var c = zc;
          zc = Oh(
            e.stateNode.containerInfo
          ), to(
            e,
            t,
            a
          ), zc = c;
          break;
        case 22:
          e.memoizedState === null && (c = e.alternate, c !== null && c.memoizedState !== null ? (c = ap, ap = 16777216, to(
            e,
            t,
            a
          ), ap = c) : to(
            e,
            t,
            a
          ));
          break;
        default:
          to(
            e,
            t,
            a
          );
      }
    }
    function qy(e) {
      var t = e.alternate;
      if (t !== null && (e = t.child, e !== null)) {
        t.child = null;
        do
          t = e.sibling, e.sibling = null, e = t;
        while (e !== null);
      }
    }
    function tn(e) {
      var t = e.deletions;
      if ((e.flags & 16) !== 0) {
        if (t !== null)
          for (var a = 0; a < t.length; a++) {
            var c = t[a], o = Ft();
            fa = c, Mu(
              c,
              e
            ), (c.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && pn(
              c,
              ze,
              Ue,
              "Unmount"
            ), jl(o);
          }
        qy(e);
      }
      if (e.subtreeFlags & 10256)
        for (e = e.child; e !== null; )
          ch(e), e = e.sibling;
    }
    function ch(e) {
      var t = Ft(), a = Sn(), c = Ja(), o = bn();
      switch (e.tag) {
        case 0:
        case 11:
        case 15:
          tn(e), e.flags & 2048 && Pd(
            e,
            e.return,
            rn | ku
          );
          break;
        case 3:
          var f = gu();
          tn(e), e.stateNode.passiveEffectDuration += $o(f);
          break;
        case 12:
          f = gu(), tn(e), e.stateNode.passiveEffectDuration += ha(f);
          break;
        case 22:
          f = e.stateNode, e.memoizedState !== null && f._visibility & po && (e.return === null || e.return.tag !== 13) ? (f._visibility &= ~po, ih(e), (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && pn(
            e,
            ze,
            Ue,
            "Disconnect"
          )) : tn(e);
          break;
        default:
          tn(e);
      }
      (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
        e,
        ze,
        Ue,
        rl,
        il
      ), jl(t), Za(a), Sl = o, il = c;
    }
    function ih(e) {
      var t = e.deletions;
      if ((e.flags & 16) !== 0) {
        if (t !== null)
          for (var a = 0; a < t.length; a++) {
            var c = t[a], o = Ft();
            fa = c, Mu(
              c,
              e
            ), (c.mode & Pe) !== He && 0 <= ze && 0 <= Ue && 0.05 < Ue - ze && pn(
              c,
              ze,
              Ue,
              "Unmount"
            ), jl(o);
          }
        qy(e);
      }
      for (e = e.child; e !== null; )
        wy(e), e = e.sibling;
    }
    function wy(e) {
      var t = Ft(), a = Sn(), c = Ja(), o = bn();
      switch (e.tag) {
        case 0:
        case 11:
        case 15:
          Pd(
            e,
            e.return,
            rn
          ), ih(e);
          break;
        case 22:
          var f = e.stateNode;
          f._visibility & po && (f._visibility &= ~po, ih(e));
          break;
        default:
          ih(e);
      }
      (e.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
        e,
        ze,
        Ue,
        rl,
        il
      ), jl(t), Za(a), Sl = o, il = c;
    }
    function Mu(e, t) {
      for (; fa !== null; ) {
        var a = fa, c = a, o = t, f = Ft(), d = Sn(), h = Ja(), y = bn();
        switch (c.tag) {
          case 0:
          case 11:
          case 15:
            Pd(
              c,
              o,
              rn
            );
            break;
          case 23:
          case 22:
            c.memoizedState !== null && c.memoizedState.cachePool !== null && (o = c.memoizedState.cachePool.pool, o != null && Bi(o));
            break;
          case 24:
            Ms(c.memoizedState.cache);
        }
        if ((c.mode & Pe) !== He && 0 <= ze && 0 <= Ue && (Sl || 0.05 < rl) && Bn(
          c,
          ze,
          Ue,
          rl,
          il
        ), jl(f), Za(d), Sl = y, il = h, c = a.child, c !== null) c.return = a, fa = c;
        else
          e: for (a = e; fa !== null; ) {
            if (c = fa, f = c.sibling, d = c.return, gl(c), c === a) {
              fa = null;
              break e;
            }
            if (f !== null) {
              f.return = d, fa = f;
              break e;
            }
            fa = d;
          }
      }
    }
    function Gy() {
      uT.forEach(function(e) {
        return e();
      });
    }
    function Xy() {
      var e = typeof IS_REACT_ACT_ENVIRONMENT < "u" ? IS_REACT_ACT_ENVIRONMENT : void 0;
      return e || G.actQueue === null || console.error(
        "The current testing environment is not configured to support act(...)"
      ), e;
    }
    function ua(e) {
      if ((pt & ea) !== sa && tt !== 0)
        return tt & -tt;
      var t = G.T;
      return t !== null ? (t._updatedFibers || (t._updatedFibers = /* @__PURE__ */ new Set()), t._updatedFibers.add(e), Fy()) : Uc();
    }
    function hf() {
      if (Cn === 0)
        if ((tt & 536870912) === 0 || st) {
          var e = _r;
          _r <<= 1, (_r & 3932160) === 0 && (_r = 262144), Cn = e;
        } else Cn = 536870912;
      return e = au.current, e !== null && (e.flags |= 32), Cn;
    }
    function je(e, t, a) {
      if (gm && console.error("useInsertionEffect must not schedule updates."), fS && (Mv = !0), (e === Jt && (Bt === Vr || Bt === Zr) || e.cancelPendingCommit !== null) && (Cu(e, 0), On(
        e,
        tt,
        Cn,
        !1
      )), Un(e, a), (pt & ea) !== sa && e === Jt) {
        if (Yu)
          switch (t.tag) {
            case 0:
            case 11:
            case 15:
              e = nt && se(nt) || "Unknown", d2.has(e) || (d2.add(e), t = se(t) || "Unknown", console.error(
                "Cannot update a component (`%s`) while rendering a different component (`%s`). To locate the bad setState() call inside `%s`, follow the stack trace as described in https://react.dev/link/setstate-in-render",
                t,
                e,
                e
              ));
              break;
            case 1:
              r2 || (console.error(
                "Cannot update during an existing state transition (such as within `render`). Render methods should be a pure function of props and state."
              ), r2 = !0);
          }
      } else
        wu && zl(e, t, a), fr(t), e === Jt && ((pt & ea) === sa && (ls |= a), dl === Pf && On(
          e,
          tt,
          Cn,
          !1
        )), Ua(e);
    }
    function cg(e, t, a) {
      if ((pt & (ea | uu)) !== sa)
        throw Error("Should not already be working.");
      if (tt !== 0 && nt !== null) {
        var c = nt, o = Xl();
        switch (nb) {
          case cp:
          case Vr:
            var f = Q0;
            tl && ((c = c._debugTask) ? c.run(
              console.timeStamp.bind(
                console,
                "Suspended",
                f,
                o,
                Xu,
                void 0,
                "primary-light"
              )
            ) : console.timeStamp(
              "Suspended",
              f,
              o,
              Xu,
              void 0,
              "primary-light"
            ));
            break;
          case Zr:
            f = Q0, tl && ((c = c._debugTask) ? c.run(
              console.timeStamp.bind(
                console,
                "Action",
                f,
                o,
                Xu,
                void 0,
                "primary-light"
              )
            ) : console.timeStamp(
              "Action",
              f,
              o,
              Xu,
              void 0,
              "primary-light"
            ));
            break;
          default:
            tl && (c = o - Q0, 3 > c || console.timeStamp(
              "Blocked",
              Q0,
              o,
              Xu,
              void 0,
              5 > c ? "primary-light" : 10 > c ? "primary" : 100 > c ? "primary-dark" : "error"
            ));
        }
      }
      f = (a = !a && (t & 127) === 0 && (t & e.expiredLanes) === 0 || bl(e, t)) ? mc(e, t) : pf(e, t, !0);
      var d = a;
      do {
        if (f === Ro) {
          ym && !a && On(e, t, 0, !1), t = Bt, Q0 = Ql(), nb = t;
          break;
        } else {
          if (c = Xl(), o = e.current.alternate, d && !og(o)) {
            jn(t), o = oa, f = c, !tl || f <= o || (Ol ? Ol.run(
              console.timeStamp.bind(
                console,
                "Teared Render",
                o,
                f,
                ht,
                rt,
                "error"
              )
            ) : console.timeStamp(
              "Teared Render",
              o,
              f,
              ht,
              rt,
              "error"
            )), ui(t, c), f = pf(e, t, !1), d = !1;
            continue;
          }
          if (f === Qr) {
            if (d = t, e.errorRecoveryDisabledLanes & d)
              var h = 0;
            else
              h = e.pendingLanes & -536870913, h = h !== 0 ? h : h & 536870912 ? 536870912 : 0;
            if (h !== 0) {
              jn(t), Lm(
                oa,
                c,
                t,
                Ol
              ), ui(t, c), t = h;
              e: {
                c = e, f = d, d = op;
                var y = c.current.memoizedState.isDehydrated;
                if (y && (Cu(c, h).flags |= 256), h = pf(
                  c,
                  h,
                  !1
                ), h !== Qr) {
                  if (tS && !y) {
                    c.errorRecoveryDisabledLanes |= f, ls |= f, f = Pf;
                    break e;
                  }
                  c = dn, dn = d, c !== null && (dn === null ? dn = c : dn.push.apply(
                    dn,
                    c
                  ));
                }
                f = h;
              }
              if (d = !1, f !== Qr) continue;
              c = Xl();
            }
          }
          if (f === up) {
            jn(t), Lm(
              oa,
              c,
              t,
              Ol
            ), ui(t, c), Cu(e, 0), On(e, t, 0, !0);
            break;
          }
          e: {
            switch (a = e, f) {
              case Ro:
              case up:
                throw Error("Root did not complete. This is a bug in React.");
              case Pf:
                if ((t & 4194048) !== t) break;
              case Ev:
                jn(t), Bp(
                  oa,
                  c,
                  t,
                  Ol
                ), ui(t, c), o = t, (o & 127) !== 0 ? cv = c : (o & 4194048) !== 0 && (iv = c), On(
                  a,
                  t,
                  Cn,
                  !es
                );
                break e;
              case Qr:
                dn = null;
                break;
              case bv:
              case Ib:
                break;
              default:
                throw Error("Unknown root exit status.");
            }
            if (G.actQueue !== null)
              Qt(
                a,
                o,
                t,
                dn,
                fp,
                Ov,
                Cn,
                ls,
                Jr,
                f,
                null,
                null,
                oa,
                c
              );
            else {
              if ((t & 62914560) === t && (d = zv + t2 - Xl(), 10 < d)) {
                if (On(
                  a,
                  t,
                  Cn,
                  !es
                ), bi(a, 0, !0) !== 0) break e;
                Dc = t, a.timeoutHandle = b2(
                  ig.bind(
                    null,
                    a,
                    o,
                    dn,
                    fp,
                    Ov,
                    t,
                    Cn,
                    ls,
                    Jr,
                    es,
                    f,
                    "Throttled",
                    oa,
                    c
                  ),
                  d
                );
                break e;
              }
              ig(
                a,
                o,
                dn,
                fp,
                Ov,
                t,
                Cn,
                ls,
                Jr,
                es,
                f,
                null,
                oa,
                c
              );
            }
          }
        }
        break;
      } while (!0);
      Ua(e);
    }
    function ig(e, t, a, c, o, f, d, h, y, p, z, _, E, Y) {
      e.timeoutHandle = Fr;
      var ue = t.subtreeFlags, fe = null;
      if ((ue & 8192 || (ue & 16785408) === 16785408) && (fe = {
        stylesheets: null,
        count: 0,
        imgCount: 0,
        imgBytes: 0,
        suspenseyImages: [],
        waitingForImages: !0,
        waitingForViewTransition: !1,
        unsuspend: yn
      }, uh(t, f, fe), ue = (f & 62914560) === f ? zv - Xl() : (f & 4194048) === f ? e2 - Xl() : 0, ue = Rh(fe, ue), ue !== null)) {
        Dc = f, e.cancelPendingCommit = ue(
          Qt.bind(
            null,
            e,
            t,
            f,
            a,
            c,
            o,
            d,
            h,
            y,
            z,
            fe,
            fe.waitingForViewTransition ? "Waiting for the previous Animation" : 0 < fe.count ? 0 < fe.imgCount ? "Suspended on CSS and Images" : "Suspended on CSS" : fe.imgCount === 1 ? "Suspended on an Image" : 0 < fe.imgCount ? "Suspended on Images" : null,
            E,
            Y
          )
        ), On(
          e,
          f,
          d,
          !p
        );
        return;
      }
      Qt(
        e,
        t,
        f,
        a,
        c,
        o,
        d,
        h,
        y,
        z,
        fe,
        _,
        E,
        Y
      );
    }
    function og(e) {
      for (var t = e; ; ) {
        var a = t.tag;
        if ((a === 0 || a === 11 || a === 15) && t.flags & 16384 && (a = t.updateQueue, a !== null && (a = a.stores, a !== null)))
          for (var c = 0; c < a.length; c++) {
            var o = a[c], f = o.getSnapshot;
            o = o.value;
            try {
              if (!on(f(), o)) return !1;
            } catch {
              return !1;
            }
          }
        if (a = t.child, t.subtreeFlags & 16384 && a !== null)
          a.return = t, t = a;
        else {
          if (t === e) break;
          for (; t.sibling === null; ) {
            if (t.return === null || t.return === e) return !0;
            t = t.return;
          }
          t.sibling.return = t.return, t = t.sibling;
        }
      }
      return !0;
    }
    function On(e, t, a, c) {
      t &= ~lS, t &= ~ls, e.suspendedLanes |= t, e.pingedLanes &= ~t, c && (e.warmLanes |= t), c = e.expirationTimes;
      for (var o = t; 0 < o; ) {
        var f = 31 - Fl(o), d = 1 << f;
        c[f] = -1, o &= ~d;
      }
      a !== 0 && No(e, a, t);
    }
    function ln() {
      return (pt & (ea | uu)) === sa ? (xu(0), !1) : !0;
    }
    function oh() {
      if (nt !== null) {
        if (Bt === Mn)
          var e = nt.return;
        else
          e = nt, Jo(), Vc(e), cm = null, I0 = 0, e = nt;
        for (; e !== null; )
          Dy(e.alternate, e), e = e.return;
        nt = null;
      }
    }
    function ui(e, t) {
      (e & 127) !== 0 && (Hr = t), (e & 4194048) !== 0 && (Eo = t), (e & 62914560) !== 0 && (lb = t), (e & 2080374784) !== 0 && (ab = t);
    }
    function Cu(e, t) {
      tl && (console.timeStamp(
        "Blocking Track",
        3e-3,
        3e-3,
        "Blocking",
        rt,
        "primary-light"
      ), console.timeStamp(
        "Transition Track",
        3e-3,
        3e-3,
        "Transition",
        rt,
        "primary-light"
      ), console.timeStamp(
        "Suspense Track",
        3e-3,
        3e-3,
        "Suspense",
        rt,
        "primary-light"
      ), console.timeStamp(
        "Idle Track",
        3e-3,
        3e-3,
        "Idle",
        rt,
        "primary-light"
      ));
      var a = oa;
      if (oa = Ql(), tt !== 0 && 0 < a) {
        if (jn(tt), dl === bv || dl === Pf)
          Bp(
            a,
            oa,
            t,
            Ol
          );
        else {
          var c = oa, o = Ol;
          if (tl && !(c <= a)) {
            var f = (t & 738197653) === t ? "tertiary-dark" : "primary-dark", d = (t & 536870912) === t ? "Prewarm" : (t & 201326741) === t ? "Interrupted Hydration" : "Interrupted Render";
            o ? o.run(
              console.timeStamp.bind(
                console,
                d,
                a,
                c,
                ht,
                rt,
                f
              )
            ) : console.timeStamp(
              d,
              a,
              c,
              ht,
              rt,
              f
            );
          }
        }
        ui(tt, oa);
      }
      if (a = Ol, Ol = null, (t & 127) !== 0) {
        Ol = G0, o = 0 <= pi && pi < Hr ? Hr : pi, c = 0 <= jr && jr < Hr ? Hr : jr, f = 0 <= c ? c : 0 <= o ? o : oa, 0 <= cv ? (jn(2), Yp(
          cv,
          f,
          t,
          a
        )) : ov & 127, a = o;
        var h = c, y = X0, p = 0 < am, z = kf === w0, _ = kf === uv;
        if (o = oa, c = G0, f = H1, d = j1, tl) {
          if (ht = "Blocking", 0 < a ? a > o && (a = o) : a = o, 0 < h ? h > a && (h = a) : h = a, y !== null && a > h) {
            var E = p ? "secondary-light" : "warning";
            c ? c.run(
              console.timeStamp.bind(
                console,
                p ? "Consecutive" : "Event: " + y,
                h,
                a,
                ht,
                rt,
                E
              )
            ) : console.timeStamp(
              p ? "Consecutive" : "Event: " + y,
              h,
              a,
              ht,
              rt,
              E
            );
          }
          o > a && (h = z ? "error" : (t & 738197653) === t ? "tertiary-light" : "primary-light", z = _ ? "Promise Resolved" : z ? "Cascading Update" : 5 < o - a ? "Update Blocked" : "Update", _ = [], d != null && _.push(["Component name", d]), f != null && _.push(["Method name", f]), a = {
            start: a,
            end: o,
            detail: {
              devtools: {
                properties: _,
                track: ht,
                trackGroup: rt,
                color: h
              }
            }
          }, c ? c.run(
            performance.measure.bind(
              performance,
              z,
              a
            )
          ) : performance.measure(z, a));
        }
        pi = -1.1, kf = 0, j1 = H1 = null, cv = -1.1, am = jr, jr = -1.1, Hr = Ql();
      }
      if ((t & 4194048) !== 0 && (Ol = L0, o = 0 <= To && To < Eo ? Eo : To, a = 0 <= Ku && Ku < Eo ? Eo : Ku, c = 0 <= Wf && Wf < Eo ? Eo : Wf, f = 0 <= c ? c : 0 <= a ? a : oa, 0 <= iv ? (jn(256), Yp(
        iv,
        f,
        t,
        Ol
      )) : ov & 4194048, _ = c, h = Br, y = 0 < Ff, p = B1 === uv, f = oa, c = L0, d = eb, z = tb, tl && (ht = "Transition", 0 < a ? a > f && (a = f) : a = f, 0 < o ? o > a && (o = a) : o = a, 0 < _ ? _ > o && (_ = o) : _ = o, o > _ && h !== null && (E = y ? "secondary-light" : "warning", c ? c.run(
        console.timeStamp.bind(
          console,
          y ? "Consecutive" : "Event: " + h,
          _,
          o,
          ht,
          rt,
          E
        )
      ) : console.timeStamp(
        y ? "Consecutive" : "Event: " + h,
        _,
        o,
        ht,
        rt,
        E
      )), a > o && (c ? c.run(
        console.timeStamp.bind(
          console,
          "Action",
          o,
          a,
          ht,
          rt,
          "primary-dark"
        )
      ) : console.timeStamp(
        "Action",
        o,
        a,
        ht,
        rt,
        "primary-dark"
      )), f > a && (o = p ? "Promise Resolved" : 5 < f - a ? "Update Blocked" : "Update", _ = [], z != null && _.push(["Component name", z]), d != null && _.push(["Method name", d]), a = {
        start: a,
        end: f,
        detail: {
          devtools: {
            properties: _,
            track: ht,
            trackGroup: rt,
            color: "primary-light"
          }
        }
      }, c ? c.run(
        performance.measure.bind(
          performance,
          o,
          a
        )
      ) : performance.measure(o, a))), Ku = To = -1.1, B1 = 0, iv = -1.1, Ff = Wf, Wf = -1.1, Eo = Ql()), (t & 62914560) !== 0 && (ov & 62914560) !== 0 && (jn(4194304), Qm(lb, oa)), (t & 2080374784) !== 0 && (ov & 2080374784) !== 0 && (jn(268435456), Qm(ab, oa)), a = e.timeoutHandle, a !== Fr && (e.timeoutHandle = Fr, vT(a)), a = e.cancelPendingCommit, a !== null && (e.cancelPendingCommit = null, a()), Dc = 0, oh(), Jt = e, nt = a = yu(
        e.current,
        null
      ), tt = t, Bt = Mn, cu = null, es = !1, ym = bl(e, t), tS = !1, dl = Ro, Jr = Cn = lS = ls = ts = 0, dn = op = null, Ov = !1, (t & 8) !== 0 && (t |= t & 32), c = e.entangledLanes, c !== 0)
        for (e = e.entanglements, c &= t; 0 < c; )
          o = 31 - Fl(c), f = 1 << o, t |= e[o], c &= ~f;
      return vi = t, bd(), e = $S(), 1e3 < e - KS && (G.recentlyCreatedOwnerStacks = 0, KS = e), Ac.discardPendingWarnings(), a;
    }
    function Kn(e, t) {
      qe = null, G.H = lp, G.getCurrentStack = null, Yu = !1, ja = null, t === um || t === dv ? (t = wi(), Bt = cp) : t === G1 ? (t = wi(), Bt = Pb) : Bt = t === W1 ? eS : t !== null && typeof t == "object" && typeof t.then == "function" ? ip : Tv, cu = t;
      var a = nt;
      a === null ? (dl = up, $s(
        e,
        da(t, e.current)
      )) : a.mode & Pe && Rd(a);
    }
    function Ly() {
      var e = au.current;
      return e === null ? !0 : (tt & 4194048) === tt ? $u === null : (tt & 62914560) === tt || (tt & 536870912) !== 0 ? e === $u : !1;
    }
    function fh() {
      var e = G.H;
      return G.H = lp, e === null ? lp : e;
    }
    function Qy() {
      var e = G.A;
      return G.A = nT, e;
    }
    function mf(e) {
      Ol === null && (Ol = e._debugTask == null ? null : e._debugTask);
    }
    function yf() {
      dl = Pf, es || (tt & 4194048) !== tt && au.current !== null || (ym = !0), (ts & 134217727) === 0 && (ls & 134217727) === 0 || Jt === null || On(
        Jt,
        tt,
        Cn,
        !1
      );
    }
    function pf(e, t, a) {
      var c = pt;
      pt |= ea;
      var o = fh(), f = Qy();
      if (Jt !== e || tt !== t) {
        if (wu) {
          var d = e.memoizedUpdaters;
          0 < d.size && (vf(e, tt), d.clear()), Xa(e, t);
        }
        fp = null, Cu(e, t);
      }
      t = !1, d = dl;
      e: do
        try {
          if (Bt !== Mn && nt !== null) {
            var h = nt, y = cu;
            switch (Bt) {
              case eS:
                oh(), d = Ev;
                break e;
              case cp:
              case Vr:
              case Zr:
              case ip:
                au.current === null && (t = !0);
                var p = Bt;
                if (Bt = Mn, cu = null, gf(e, h, y, p), a && ym) {
                  d = Ro;
                  break e;
                }
                break;
              default:
                p = Bt, Bt = Mn, cu = null, gf(e, h, y, p);
            }
          }
          Vy(), d = dl;
          break;
        } catch (z) {
          Kn(e, z);
        }
      while (!0);
      return t && e.shellSuspendCounter++, Jo(), pt = c, G.H = o, G.A = f, nt === null && (Jt = null, tt = 0, bd()), d;
    }
    function Vy() {
      for (; nt !== null; ) sh(nt);
    }
    function mc(e, t) {
      var a = pt;
      pt |= ea;
      var c = fh(), o = Qy();
      if (Jt !== e || tt !== t) {
        if (wu) {
          var f = e.memoizedUpdaters;
          0 < f.size && (vf(e, tt), f.clear()), Xa(e, t);
        }
        fp = null, Dv = Xl() + l2, Cu(e, t);
      } else
        ym = bl(
          e,
          t
        );
      e: do
        try {
          if (Bt !== Mn && nt !== null)
            t: switch (t = nt, f = cu, Bt) {
              case Tv:
                Bt = Mn, cu = null, gf(
                  e,
                  t,
                  f,
                  Tv
                );
                break;
              case Vr:
              case Zr:
                if (ty(f)) {
                  Bt = Mn, cu = null, Zy(t);
                  break;
                }
                t = function() {
                  Bt !== Vr && Bt !== Zr || Jt !== e || (Bt = Av), Ua(e);
                }, f.then(t, t);
                break e;
              case cp:
                Bt = Av;
                break e;
              case Pb:
                Bt = P1;
                break e;
              case Av:
                ty(f) ? (Bt = Mn, cu = null, Zy(t)) : (Bt = Mn, cu = null, gf(
                  e,
                  t,
                  f,
                  Av
                ));
                break;
              case P1:
                var d = null;
                switch (nt.tag) {
                  case 26:
                    d = nt.memoizedState;
                  case 5:
                  case 27:
                    var h = nt;
                    if (d ? ct(d) : h.stateNode.complete) {
                      Bt = Mn, cu = null;
                      var y = h.sibling;
                      if (y !== null) nt = y;
                      else {
                        var p = h.return;
                        p !== null ? (nt = p, cr(p)) : nt = null;
                      }
                      break t;
                    }
                    break;
                  default:
                    console.error(
                      "Unexpected type of fiber triggered a suspensey commit. This is a bug in React."
                    );
                }
                Bt = Mn, cu = null, gf(
                  e,
                  t,
                  f,
                  P1
                );
                break;
              case ip:
                Bt = Mn, cu = null, gf(
                  e,
                  t,
                  f,
                  ip
                );
                break;
              case eS:
                oh(), dl = Ev;
                break e;
              default:
                throw Error(
                  "Unexpected SuspendedReason. This is a bug in React."
                );
            }
          G.actQueue !== null ? Vy() : Tl();
          break;
        } catch (z) {
          Kn(e, z);
        }
      while (!0);
      return Jo(), G.H = c, G.A = o, pt = a, nt !== null ? Ro : (Jt = null, tt = 0, bd(), dl);
    }
    function Tl() {
      for (; nt !== null && !qh(); )
        sh(nt);
    }
    function sh(e) {
      var t = e.alternate;
      (e.mode & Pe) !== He ? (ac(e), t = oe(
        e,
        Is,
        t,
        e,
        vi
      ), Rd(e)) : t = oe(
        e,
        Is,
        t,
        e,
        vi
      ), e.memoizedProps = e.pendingProps, t === null ? cr(e) : nt = t;
    }
    function Zy(e) {
      var t = oe(e, Gl, e);
      e.memoizedProps = e.pendingProps, t === null ? cr(e) : nt = t;
    }
    function Gl(e) {
      var t = e.alternate, a = (e.mode & Pe) !== He;
      switch (a && ac(e), e.tag) {
        case 15:
        case 0:
          t = by(
            t,
            e,
            e.pendingProps,
            e.type,
            void 0,
            tt
          );
          break;
        case 11:
          t = by(
            t,
            e,
            e.pendingProps,
            e.type.render,
            e.ref,
            tt
          );
          break;
        case 5:
          Vc(e);
        default:
          Dy(t, e), e = nt = Km(e, vi), t = Is(t, e, vi);
      }
      return a && Rd(e), t;
    }
    function gf(e, t, a, c) {
      Jo(), Vc(t), cm = null, I0 = 0;
      var o = t.return;
      try {
        if (hy(
          e,
          o,
          t,
          a,
          tt
        )) {
          dl = up, $s(
            e,
            da(a, e.current)
          ), nt = null;
          return;
        }
      } catch (f) {
        if (o !== null) throw nt = o, f;
        dl = up, $s(
          e,
          da(a, e.current)
        ), nt = null;
        return;
      }
      t.flags & 32768 ? (st || c === Tv ? e = !0 : ym || (tt & 536870912) !== 0 ? e = !1 : (es = e = !0, (c === Vr || c === Zr || c === cp || c === ip) && (c = au.current, c !== null && c.tag === 13 && (c.flags |= 16384))), Jy(t, e)) : cr(t);
    }
    function cr(e) {
      var t = e;
      do {
        if ((t.flags & 32768) !== 0) {
          Jy(
            t,
            es
          );
          return;
        }
        var a = t.alternate;
        if (e = t.return, ac(t), a = oe(
          t,
          zy,
          a,
          t,
          vi
        ), (t.mode & Pe) !== He && Cs(t), a !== null) {
          nt = a;
          return;
        }
        if (t = t.sibling, t !== null) {
          nt = t;
          return;
        }
        nt = t = e;
      } while (t !== null);
      dl === Ro && (dl = Ib);
    }
    function Jy(e, t) {
      do {
        var a = Pp(e.alternate, e);
        if (a !== null) {
          a.flags &= 32767, nt = a;
          return;
        }
        if ((e.mode & Pe) !== He) {
          Cs(e), a = e.actualDuration;
          for (var c = e.child; c !== null; )
            a += c.actualDuration, c = c.sibling;
          e.actualDuration = a;
        }
        if (a = e.return, a !== null && (a.flags |= 32768, a.subtreeFlags = 0, a.deletions = null), !t && (e = e.sibling, e !== null)) {
          nt = e;
          return;
        }
        nt = e = a;
      } while (e !== null);
      dl = Ev, nt = null;
    }
    function Qt(e, t, a, c, o, f, d, h, y, p, z, _, E, Y) {
      e.cancelPendingCommit = null;
      do
        ir();
      while ($l !== ns);
      if (Ac.flushLegacyContextWarning(), Ac.flushPendingUnsafeLifecycleWarnings(), (pt & (ea | uu)) !== sa)
        throw Error("Should not already be working.");
      if (jn(a), p === Qr ? Lm(
        E,
        Y,
        a,
        Ol
      ) : c !== null ? a1(
        E,
        Y,
        a,
        c,
        t !== null && t.alternate !== null && t.alternate.memoizedState.isDehydrated && (t.flags & 256) !== 0,
        Ol
      ) : l1(
        E,
        Y,
        a,
        Ol
      ), t !== null) {
        if (a === 0 && console.error(
          "finishedLanes should not be empty during a commit. This is a bug in React."
        ), t === e.current)
          throw Error(
            "Cannot commit the same tree as before. This error is likely caused by a bug in React. Please file an issue."
          );
        if (f = t.lanes | t.childLanes, f |= M1, ld(
          e,
          a,
          f,
          d,
          h,
          y
        ), e === Jt && (nt = Jt = null, tt = 0), pm = t, us = e, Dc = a, uS = f, iS = o, o2 = c, cS = Y, f2 = _, Rc = Rv, s2 = null, t.actualDuration !== 0 || (t.subtreeFlags & 10256) !== 0 || (t.flags & 10256) !== 0 ? (e.callbackNode = null, e.callbackPriority = 0, Sf(ro, function() {
          return yp = window.event, Rc === Rv && (Rc = nS), or(), null;
        })) : (e.callbackNode = null, e.callbackPriority = 0), bo = null, $f = Ql(), _ !== null && n1(
          Y,
          $f,
          _,
          Ol
        ), c = (t.flags & 13878) !== 0, (t.subtreeFlags & 13878) !== 0 || c) {
          c = G.T, G.T = null, o = At.p, At.p = Cl, d = pt, pt |= uu;
          try {
            i1(e, t, a);
          } finally {
            pt = d, At.p = o, G.T = c;
          }
        }
        $l = n2, Ea(), Uu(), Ky();
      }
    }
    function Ea() {
      if ($l === n2) {
        $l = ns;
        var e = us, t = pm, a = Dc, c = (t.flags & 13878) !== 0;
        if ((t.subtreeFlags & 13878) !== 0 || c) {
          c = G.T, G.T = null;
          var o = At.p;
          At.p = Cl;
          var f = pt;
          pt |= uu;
          try {
            hm = a, mm = e, Yi(), lr(t, e), mm = hm = null, a = vS;
            var d = gd(e.containerInfo), h = a.focusedElem, y = a.selectionRange;
            if (d !== h && h && h.ownerDocument && xp(
              h.ownerDocument.documentElement,
              h
            )) {
              if (y !== null && wm(h)) {
                var p = y.start, z = y.end;
                if (z === void 0 && (z = p), "selectionStart" in h)
                  h.selectionStart = p, h.selectionEnd = Math.min(
                    z,
                    h.value.length
                  );
                else {
                  var _ = h.ownerDocument || document, E = _ && _.defaultView || window;
                  if (E.getSelection) {
                    var Y = E.getSelection(), ue = h.textContent.length, fe = Math.min(
                      y.start,
                      ue
                    ), Wt = y.end === void 0 ? fe : Math.min(y.end, ue);
                    !Y.extend && fe > Wt && (d = Wt, Wt = fe, fe = d);
                    var dt = Up(
                      h,
                      fe
                    ), b = Up(
                      h,
                      Wt
                    );
                    if (dt && b && (Y.rangeCount !== 1 || Y.anchorNode !== dt.node || Y.anchorOffset !== dt.offset || Y.focusNode !== b.node || Y.focusOffset !== b.offset)) {
                      var T = _.createRange();
                      T.setStart(dt.node, dt.offset), Y.removeAllRanges(), fe > Wt ? (Y.addRange(T), Y.extend(b.node, b.offset)) : (T.setEnd(b.node, b.offset), Y.addRange(T));
                    }
                  }
                }
              }
              for (_ = [], Y = h; Y = Y.parentNode; )
                Y.nodeType === 1 && _.push({
                  element: Y,
                  left: Y.scrollLeft,
                  top: Y.scrollTop
                });
              for (typeof h.focus == "function" && h.focus(), h = 0; h < _.length; h++) {
                var O = _[h];
                O.element.scrollLeft = O.left, O.element.scrollTop = O.top;
              }
            }
            Qv = !!gS, vS = gS = null;
          } finally {
            pt = f, At.p = o, G.T = c;
          }
        }
        e.current = t, $l = u2;
      }
    }
    function Uu() {
      if ($l === u2) {
        $l = ns;
        var e = s2;
        if (e !== null) {
          $f = Ql();
          var t = So, a = $f;
          !tl || a <= t || console.timeStamp(
            e,
            t,
            a,
            ht,
            rt,
            "secondary-light"
          );
        }
        e = us, t = pm, a = Dc;
        var c = (t.flags & 8772) !== 0;
        if ((t.subtreeFlags & 8772) !== 0 || c) {
          c = G.T, G.T = null;
          var o = At.p;
          At.p = Cl;
          var f = pt;
          pt |= uu;
          try {
            hm = a, mm = e, Yi(), ah(
              e,
              t.alternate,
              t
            ), mm = hm = null;
          } finally {
            pt = f, At.p = o, G.T = c;
          }
        }
        e = cS, t = f2, So = Ql(), e = t === null ? e : $f, t = So, a = Rc === aS, c = Ol, bo !== null ? qp(
          e,
          t,
          bo,
          !1,
          c
        ) : !tl || t <= e || (c ? c.run(
          console.timeStamp.bind(
            console,
            a ? "Commit Interrupted View Transition" : "Commit",
            e,
            t,
            ht,
            rt,
            a ? "error" : "secondary-dark"
          )
        ) : console.timeStamp(
          a ? "Commit Interrupted View Transition" : "Commit",
          e,
          t,
          ht,
          rt,
          a ? "error" : "secondary-dark"
        )), $l = c2;
      }
    }
    function Ky() {
      if ($l === i2 || $l === c2) {
        if ($l === i2) {
          var e = So;
          So = Ql();
          var t = So, a = Rc === aS;
          !tl || t <= e || console.timeStamp(
            a ? "Interrupted View Transition" : "Starting Animation",
            e,
            t,
            ht,
            rt,
            a ? " error" : "secondary-light"
          ), Rc !== aS && (Rc = a2);
        }
        $l = ns, wh(), e = us;
        var c = pm;
        t = Dc, a = o2;
        var o = c.actualDuration !== 0 || (c.subtreeFlags & 10256) !== 0 || (c.flags & 10256) !== 0;
        o ? $l = _v : ($l = ns, pm = us = null, $y(
          e,
          e.pendingLanes
        ), Kr = 0, rp = null);
        var f = e.pendingLanes;
        if (f === 0 && (as = null), o || hh(e), f = Nl(t), c = c.stateNode, Ml && typeof Ml.onCommitFiberRoot == "function")
          try {
            var d = (c.current.flags & 128) === 128;
            switch (f) {
              case Cl:
                var h = O0;
                break;
              case Il:
                h = Gh;
                break;
              case ia:
                h = ro;
                break;
              case hi:
                h = Xh;
                break;
              default:
                h = ro;
            }
            Ml.onCommitFiberRoot(
              ho,
              c,
              h,
              d
            );
          } catch (_) {
            qu || (qu = !0, console.error(
              "React instrumentation encountered an error: %o",
              _
            ));
          }
        if (wu && e.memoizedUpdaters.clear(), Gy(), a !== null) {
          d = G.T, h = At.p, At.p = Cl, G.T = null;
          try {
            var y = e.onRecoverableError;
            for (c = 0; c < a.length; c++) {
              var p = a[c], z = fg(p.stack);
              oe(
                p.source,
                y,
                p.value,
                z
              );
            }
          } finally {
            G.T = d, At.p = h;
          }
        }
        (Dc & 3) !== 0 && ir(), Ua(e), f = e.pendingLanes, (t & 261930) !== 0 && (f & 42) !== 0 ? (sv = !0, e === oS ? sp++ : (sp = 0, oS = e)) : sp = 0, o || ui(t, So), xu(0);
      }
    }
    function fg(e) {
      return e = { componentStack: e }, Object.defineProperty(e, "digest", {
        get: function() {
          console.error(
            'You are accessing "digest" from the errorInfo object passed to onRecoverableError. This property is no longer provided as part of errorInfo but can be accessed as a property of the Error instance itself.'
          );
        }
      }), e;
    }
    function $y(e, t) {
      (e.pooledCacheLanes &= t) === 0 && (t = e.pooledCache, t != null && (e.pooledCache = null, Ms(t)));
    }
    function ir() {
      return Ea(), Uu(), Ky(), or();
    }
    function or() {
      if ($l !== _v) return !1;
      var e = us, t = uS;
      uS = 0;
      var a = Nl(Dc), c = ia > a ? ia : a;
      a = G.T;
      var o = At.p;
      try {
        At.p = c, G.T = null;
        var f = iS;
        iS = null, c = us;
        var d = Dc;
        if ($l = ns, pm = us = null, Dc = 0, (pt & (ea | uu)) !== sa)
          throw Error("Cannot flush passive effects while already rendering.");
        jn(d), fS = !0, Mv = !1;
        var h = 0;
        if (bo = null, h = Xl(), Rc === a2)
          Qm(
            So,
            h,
            FE
          );
        else {
          var y = So, p = h, z = Rc === nS;
          !tl || p <= y || (Ol ? Ol.run(
            console.timeStamp.bind(
              console,
              z ? "Waiting for Paint" : "Waiting",
              y,
              p,
              ht,
              rt,
              "secondary-light"
            )
          ) : console.timeStamp(
            z ? "Waiting for Paint" : "Waiting",
            y,
            p,
            ht,
            rt,
            "secondary-light"
          ));
        }
        y = pt, pt |= uu;
        var _ = c.current;
        Yi(), ch(_);
        var E = c.current;
        _ = cS, Yi(), Yy(
          c,
          E,
          d,
          f,
          _
        ), hh(c), pt = y;
        var Y = Xl();
        if (E = h, _ = Ol, bo !== null ? qp(
          E,
          Y,
          bo,
          !0,
          _
        ) : !tl || Y <= E || (_ ? _.run(
          console.timeStamp.bind(
            console,
            "Remaining Effects",
            E,
            Y,
            ht,
            rt,
            "secondary-dark"
          )
        ) : console.timeStamp(
          "Remaining Effects",
          E,
          Y,
          ht,
          rt,
          "secondary-dark"
        )), ui(d, Y), xu(0, !1), Mv ? c === rp ? Kr++ : (Kr = 0, rp = c) : Kr = 0, Mv = fS = !1, Ml && typeof Ml.onPostCommitFiberRoot == "function")
          try {
            Ml.onPostCommitFiberRoot(ho, c);
          } catch (fe) {
            qu || (qu = !0, console.error(
              "React instrumentation encountered an error: %o",
              fe
            ));
          }
        var ue = c.current.stateNode;
        return ue.effectDuration = 0, ue.passiveEffectDuration = 0, !0;
      } finally {
        At.p = o, G.T = a, $y(e, t);
      }
    }
    function Ta(e, t, a) {
      t = da(a, t), Vp(t), t = Qd(e.stateNode, t, 2), e = Su(e, t, 2), e !== null && (Un(e, 2), Ua(e));
    }
    function ke(e, t, a) {
      if (gm = !1, e.tag === 3)
        Ta(e, e, a);
      else {
        for (; t !== null; ) {
          if (t.tag === 3) {
            Ta(
              t,
              e,
              a
            );
            return;
          }
          if (t.tag === 1) {
            var c = t.stateNode;
            if (typeof t.type.getDerivedStateFromError == "function" || typeof c.componentDidCatch == "function" && (as === null || !as.has(c))) {
              e = da(a, e), Vp(e), a = Vd(2), c = Su(t, a, 2), c !== null && (Zd(
                a,
                c,
                t,
                e
              ), Un(c, 2), Ua(c));
              return;
            }
          }
          t = t.return;
        }
        console.error(
          `Internal React error: Attempted to capture a commit phase error inside a detached tree. This indicates a bug in React. Potential causes include deleting the same fiber more than once, committing an already-finished tree, or an inconsistent return pointer.

Error message:

%s`,
          a
        );
      }
    }
    function rh(e, t, a) {
      var c = e.pingCache;
      if (c === null) {
        c = e.pingCache = new cT();
        var o = /* @__PURE__ */ new Set();
        c.set(t, o);
      } else
        o = c.get(t), o === void 0 && (o = /* @__PURE__ */ new Set(), c.set(t, o));
      o.has(a) || (tS = !0, o.add(a), c = Ca.bind(null, e, t, a), wu && vf(e, a), t.then(c, c));
    }
    function Ca(e, t, a) {
      var c = e.pingCache;
      c !== null && c.delete(t), e.pingedLanes |= e.suspendedLanes & a, e.warmLanes &= ~a, (a & 127) !== 0 ? 0 > pi && (Hr = pi = Ql(), G0 = nv("Promise Resolved"), kf = uv) : (a & 4194048) !== 0 && 0 > Ku && (Eo = Ku = Ql(), L0 = nv("Promise Resolved"), B1 = uv), Xy() && G.actQueue === null && console.error(
        `A suspended resource finished loading inside a test, but the event was not wrapped in act(...).

When testing, code that resolves suspended data should be wrapped into act(...):

act(() => {
  /* finish loading suspended data */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act`
      ), Jt === e && (tt & a) === a && (dl === Pf || dl === bv && (tt & 62914560) === tt && Xl() - zv < t2 ? (pt & ea) === sa && Cu(e, 0) : lS |= a, Jr === tt && (Jr = 0)), Ua(e);
    }
    function ky(e, t) {
      t === 0 && (t = Uo()), e = aa(e, t), e !== null && (Un(e, t), Ua(e));
    }
    function yc(e) {
      var t = e.memoizedState, a = 0;
      t !== null && (a = t.retryLane), ky(e, a);
    }
    function lo(e, t) {
      var a = 0;
      switch (e.tag) {
        case 31:
        case 13:
          var c = e.stateNode, o = e.memoizedState;
          o !== null && (a = o.retryLane);
          break;
        case 19:
          c = e.stateNode;
          break;
        case 22:
          c = e.stateNode._retryCache;
          break;
        default:
          throw Error(
            "Pinged unknown suspense boundary type. This is probably a bug in React."
          );
      }
      c !== null && c.delete(t), ky(e, a);
    }
    function $n(e, t, a) {
      if ((t.subtreeFlags & 67117056) !== 0)
        for (t = t.child; t !== null; ) {
          var c = e, o = t, f = o.type === za;
          f = a || f, o.tag !== 22 ? o.flags & 67108864 ? f && oe(
            o,
            dh,
            c,
            o
          ) : $n(
            c,
            o,
            f
          ) : o.memoizedState === null && (f && o.flags & 8192 ? oe(
            o,
            dh,
            c,
            o
          ) : o.subtreeFlags & 67108864 && oe(
            o,
            $n,
            c,
            o,
            f
          )), t = t.sibling;
        }
    }
    function dh(e, t) {
      de(!0);
      try {
        nh(t), wy(t), By(e, t.alternate, t, !1), ur(e, t, 0, null, !1, 0);
      } finally {
        de(!1);
      }
    }
    function hh(e) {
      var t = !0;
      e.current.mode & (Ba | Tc) || (t = !1), $n(
        e,
        e.current,
        t
      );
    }
    function zn(e) {
      if ((pt & ea) === sa) {
        var t = e.tag;
        if (t === 3 || t === 1 || t === 0 || t === 11 || t === 14 || t === 15) {
          if (t = se(e) || "ReactComponent", Cv !== null) {
            if (Cv.has(t)) return;
            Cv.add(t);
          } else Cv = /* @__PURE__ */ new Set([t]);
          oe(e, function() {
            console.error(
              "Can't perform a React state update on a component that hasn't mounted yet. This indicates that you have a side-effect in your render function that asynchronously tries to update the component. Move this work to useEffect instead."
            );
          });
        }
      }
    }
    function vf(e, t) {
      wu && e.memoizedUpdaters.forEach(function(a) {
        zl(e, a, t);
      });
    }
    function Sf(e, t) {
      var a = G.actQueue;
      return a !== null ? (a.push(t), fT) : A0(e, t);
    }
    function fr(e) {
      Xy() && G.actQueue === null && oe(e, function() {
        console.error(
          `An update to %s inside a test was not wrapped in act(...).

When testing, code that causes React state updates should be wrapped into act(...):

act(() => {
  /* fire events that update state */
});
/* assert on the output */

This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act`,
          se(e)
        );
      });
    }
    function Ua(e) {
      e !== vm && e.next === null && (vm === null ? Uv = vm = e : vm = vm.next = e), xv = !0, G.actQueue !== null ? rS || (rS = !0, rg()) : sS || (sS = !0, rg());
    }
    function xu(e, t) {
      if (!dS && xv) {
        dS = !0;
        do
          for (var a = !1, c = Uv; c !== null; ) {
            if (e !== 0) {
              var o = c.pendingLanes;
              if (o === 0) var f = 0;
              else {
                var d = c.suspendedLanes, h = c.pingedLanes;
                f = (1 << 31 - Fl(42 | e) + 1) - 1, f &= o & ~(d & ~h), f = f & 201326741 ? f & 201326741 | 1 : f ? f | 2 : 0;
              }
              f !== 0 && (a = !0, sr(c, f));
            } else
              f = tt, f = bi(
                c,
                c === Jt ? f : 0,
                c.cancelPendingCommit !== null || c.timeoutHandle !== Fr
              ), (f & 3) === 0 || bl(c, f) || (a = !0, sr(c, f));
            c = c.next;
          }
        while (a);
        dS = !1;
      }
    }
    function sg() {
      yp = window.event, mh();
    }
    function mh() {
      xv = rS = sS = !1;
      var e = 0;
      cs !== 0 && Py() && (e = cs);
      for (var t = Xl(), a = null, c = Uv; c !== null; ) {
        var o = c.next, f = bf(c, t);
        f === 0 ? (c.next = null, a === null ? Uv = o : a.next = o, o === null && (vm = a)) : (a = c, (e !== 0 || (f & 3) !== 0) && (xv = !0)), c = o;
      }
      $l !== ns && $l !== _v || xu(e), cs !== 0 && (cs = 0);
    }
    function bf(e, t) {
      for (var a = e.suspendedLanes, c = e.pingedLanes, o = e.expirationTimes, f = e.pendingLanes & -62914561; 0 < f; ) {
        var d = 31 - Fl(f), h = 1 << d, y = o[d];
        y === -1 ? ((h & a) === 0 || (h & c) !== 0) && (o[d] = td(h, t)) : y <= t && (e.expiredLanes |= h), f &= ~h;
      }
      if (t = Jt, a = tt, a = bi(
        e,
        e === t ? a : 0,
        e.cancelPendingCommit !== null || e.timeoutHandle !== Fr
      ), c = e.callbackNode, a === 0 || e === t && (Bt === Vr || Bt === Zr) || e.cancelPendingCommit !== null)
        return c !== null && yh(c), e.callbackNode = null, e.callbackPriority = 0;
      if ((a & 3) === 0 || bl(e, a)) {
        if (t = a & -a, t !== e.callbackPriority || G.actQueue !== null && c !== hS)
          yh(c);
        else return t;
        switch (Nl(a)) {
          case Cl:
          case Il:
            a = Gh;
            break;
          case ia:
            a = ro;
            break;
          case hi:
            a = Xh;
            break;
          default:
            a = ro;
        }
        return c = Wy.bind(null, e), G.actQueue !== null ? (G.actQueue.push(c), a = hS) : a = A0(a, c), e.callbackPriority = t, e.callbackNode = a, t;
      }
      return c !== null && yh(c), e.callbackPriority = 2, e.callbackNode = null, 2;
    }
    function Wy(e, t) {
      if (sv = fv = !1, yp = window.event, $l !== ns && $l !== _v)
        return e.callbackNode = null, e.callbackPriority = 0, null;
      var a = e.callbackNode;
      if (Rc === Rv && (Rc = nS), ir() && e.callbackNode !== a)
        return null;
      var c = tt;
      return c = bi(
        e,
        e === Jt ? c : 0,
        e.cancelPendingCommit !== null || e.timeoutHandle !== Fr
      ), c === 0 ? null : (cg(
        e,
        c,
        t
      ), bf(e, Xl()), e.callbackNode != null && e.callbackNode === a ? Wy.bind(null, e) : null);
    }
    function sr(e, t) {
      if (ir()) return null;
      fv = sv, sv = !1, cg(e, t, !0);
    }
    function yh(e) {
      e !== hS && e !== null && Yh(e);
    }
    function rg() {
      G.actQueue !== null && G.actQueue.push(function() {
        return mh(), null;
      }), ST(function() {
        (pt & (ea | uu)) !== sa ? A0(
          O0,
          sg
        ) : mh();
      });
    }
    function Fy() {
      if (cs === 0) {
        var e = Yr;
        e === 0 && (e = qf, qf <<= 1, (qf & 261888) === 0 && (qf = 256)), cs = e;
      }
      return cs;
    }
    function St(e) {
      return e == null || typeof e == "symbol" || typeof e == "boolean" ? null : typeof e == "function" ? e : (vt(e, "action"), Ss("" + e));
    }
    function Nt(e, t) {
      var a = t.ownerDocument.createElement("input");
      return a.name = t.name, a.value = t.value, e.id && a.setAttribute("form", e.id), t.parentNode.insertBefore(a, t), e = new FormData(e), a.parentNode.removeChild(a), e;
    }
    function ft(e, t, a, c, o) {
      if (t === "submit" && a && a.stateNode === o) {
        var f = St(
          (o[Da] || null).action
        ), d = c.submitter;
        d && (t = (t = d[Da] || null) ? St(t.formAction) : d.getAttribute("formAction"), t !== null && (f = t, d = null));
        var h = new Fg(
          "action",
          "action",
          null,
          c,
          o
        );
        e.push({
          event: h,
          listeners: [
            {
              instance: null,
              listener: function() {
                if (c.defaultPrevented) {
                  if (cs !== 0) {
                    var y = d ? Nt(
                      o,
                      d
                    ) : new FormData(o), p = {
                      pending: !0,
                      data: y,
                      method: o.method,
                      action: f
                    };
                    Object.freeze(p), rc(
                      a,
                      p,
                      null,
                      y
                    );
                  }
                } else
                  typeof f == "function" && (h.preventDefault(), y = d ? Nt(
                    o,
                    d
                  ) : new FormData(o), p = {
                    pending: !0,
                    data: y,
                    method: o.method,
                    action: f
                  }, Object.freeze(p), rc(
                    a,
                    p,
                    f,
                    y
                  ));
              },
              currentTarget: o
            }
          ]
        });
      }
    }
    function at(e, t, a) {
      e.currentTarget = a;
      try {
        t(e);
      } catch (c) {
        z1(c);
      }
      e.currentTarget = null;
    }
    function _t(e, t) {
      t = (t & 4) !== 0;
      for (var a = 0; a < e.length; a++) {
        var c = e[a];
        e: {
          var o = void 0, f = c.event;
          if (c = c.listeners, t)
            for (var d = c.length - 1; 0 <= d; d--) {
              var h = c[d], y = h.instance, p = h.currentTarget;
              if (h = h.listener, y !== o && f.isPropagationStopped())
                break e;
              y !== null ? oe(
                y,
                at,
                f,
                h,
                p
              ) : at(f, h, p), o = y;
            }
          else
            for (d = 0; d < c.length; d++) {
              if (h = c[d], y = h.instance, p = h.currentTarget, h = h.listener, y !== o && f.isPropagationStopped())
                break e;
              y !== null ? oe(
                y,
                at,
                f,
                h,
                p
              ) : at(f, h, p), o = y;
            }
        }
      }
    }
    function xe(e, t) {
      mS.has(e) || console.error(
        'Did not expect a listenToNonDelegatedEvent() call for "%s". This is a bug in React. Please file an issue.',
        e
      );
      var a = t[mo];
      a === void 0 && (a = t[mo] = /* @__PURE__ */ new Set());
      var c = e + "__bubble";
      a.has(c) || (ph(t, e, 2, !1), a.add(c));
    }
    function Nu(e, t, a) {
      mS.has(e) && !t && console.error(
        'Did not expect a listenToNativeEvent() call for "%s" in the bubble phase. This is a bug in React. Please file an issue.',
        e
      );
      var c = 0;
      t && (c |= 4), ph(
        a,
        e,
        c,
        t
      );
    }
    function ci(e) {
      if (!e[Nv]) {
        e[Nv] = !0, Jg.forEach(function(a) {
          a !== "selectionchange" && (mS.has(a) || Nu(a, !1, e), Nu(a, !0, e));
        });
        var t = e.nodeType === 9 ? e : e.ownerDocument;
        t === null || t[Nv] || (t[Nv] = !0, Nu("selectionchange", !1, t));
      }
    }
    function ph(e, t, a, c) {
      switch (Ch(t)) {
        case Cl:
          var o = d0;
          break;
        case Il:
          o = Wl;
          break;
        default:
          o = h0;
      }
      a = o.bind(
        null,
        t,
        a,
        e
      ), o = void 0, !y1 || t !== "touchstart" && t !== "touchmove" && t !== "wheel" || (o = !0), c ? o !== void 0 ? e.addEventListener(t, a, {
        capture: !0,
        passive: o
      }) : e.addEventListener(t, a, !0) : o !== void 0 ? e.addEventListener(t, a, {
        passive: o
      }) : e.addEventListener(
        t,
        a,
        !1
      );
    }
    function kn(e, t, a, c, o) {
      var f = c;
      if ((t & 1) === 0 && (t & 2) === 0 && c !== null)
        e: for (; ; ) {
          if (c === null) return;
          var d = c.tag;
          if (d === 3 || d === 4) {
            var h = c.stateNode.containerInfo;
            if (h === o) break;
            if (d === 4)
              for (d = c.return; d !== null; ) {
                var y = d.tag;
                if ((y === 3 || y === 4) && d.stateNode.containerInfo === o)
                  return;
                d = d.return;
              }
            for (; h !== null; ) {
              if (d = P(h), d === null) return;
              if (y = d.tag, y === 5 || y === 6 || y === 26 || y === 27) {
                c = f = d;
                continue e;
              }
              h = h.parentNode;
            }
          }
          c = c.return;
        }
      hd(function() {
        var p = f, z = Nn(a), _ = [];
        e: {
          var E = JS.get(e);
          if (E !== void 0) {
            var Y = Fg, ue = e;
            switch (e) {
              case "keypress":
                if (bs(a) === 0) break e;
              case "keydown":
              case "keyup":
                Y = OE;
                break;
              case "focusin":
                ue = "focus", Y = S1;
                break;
              case "focusout":
                ue = "blur", Y = S1;
                break;
              case "beforeblur":
              case "afterblur":
                Y = S1;
                break;
              case "click":
                if (a.button === 2) break e;
              case "auxclick":
              case "dblclick":
              case "mousedown":
              case "mousemove":
              case "mouseup":
              case "mouseout":
              case "mouseover":
              case "contextmenu":
                Y = xS;
                break;
              case "drag":
              case "dragend":
              case "dragenter":
              case "dragexit":
              case "dragleave":
              case "dragover":
              case "dragstart":
              case "drop":
                Y = dE;
                break;
              case "touchcancel":
              case "touchend":
              case "touchmove":
              case "touchstart":
                Y = RE;
                break;
              case LS:
              case QS:
              case VS:
                Y = yE;
                break;
              case ZS:
                Y = ME;
                break;
              case "scroll":
              case "scrollend":
                Y = sE;
                break;
              case "wheel":
                Y = UE;
                break;
              case "copy":
              case "cut":
              case "paste":
                Y = gE;
                break;
              case "gotpointercapture":
              case "lostpointercapture":
              case "pointercancel":
              case "pointerdown":
              case "pointermove":
              case "pointerout":
              case "pointerover":
              case "pointerup":
                Y = HS;
                break;
              case "toggle":
              case "beforetoggle":
                Y = NE;
            }
            var fe = (t & 4) !== 0, Wt = !fe && (e === "scroll" || e === "scrollend"), dt = fe ? E !== null ? E + "Capture" : null : E;
            fe = [];
            for (var b = p, T; b !== null; ) {
              var O = b;
              if (T = O.stateNode, O = O.tag, O !== 5 && O !== 26 && O !== 27 || T === null || dt === null || (O = hu(b, dt), O != null && fe.push(
                Vt(
                  b,
                  O,
                  T
                )
              )), Wt) break;
              b = b.return;
            }
            0 < fe.length && (E = new Y(
              E,
              ue,
              null,
              a,
              z
            ), _.push({
              event: E,
              listeners: fe
            }));
          }
        }
        if ((t & 7) === 0) {
          e: {
            if (E = e === "mouseover" || e === "pointerover", Y = e === "mouseout" || e === "pointerout", E && a !== M0 && (ue = a.relatedTarget || a.fromElement) && (P(ue) || ue[Ec]))
              break e;
            if ((Y || E) && (E = z.window === z ? z : (E = z.ownerDocument) ? E.defaultView || E.parentWindow : window, Y ? (ue = a.relatedTarget || a.toElement, Y = p, ue = ue ? P(ue) : null, ue !== null && (Wt = Ze(ue), fe = ue.tag, ue !== Wt || fe !== 5 && fe !== 27 && fe !== 6) && (ue = null)) : (Y = null, ue = p), Y !== ue)) {
              if (fe = xS, O = "onMouseLeave", dt = "onMouseEnter", b = "mouse", (e === "pointerout" || e === "pointerover") && (fe = HS, O = "onPointerLeave", dt = "onPointerEnter", b = "pointer"), Wt = Y == null ? E : he(Y), T = ue == null ? E : he(ue), E = new fe(
                O,
                b + "leave",
                Y,
                a,
                z
              ), E.target = Wt, E.relatedTarget = T, O = null, P(z) === p && (fe = new fe(
                dt,
                b + "enter",
                ue,
                a,
                z
              ), fe.target = T, fe.relatedTarget = Wt, O = fe), Wt = O, Y && ue)
                t: {
                  for (fe = ao, dt = Y, b = ue, T = 0, O = dt; O; O = fe(O))
                    T++;
                  O = 0;
                  for (var J = b; J; J = fe(J))
                    O++;
                  for (; 0 < T - O; )
                    dt = fe(dt), T--;
                  for (; 0 < O - T; )
                    b = fe(b), O--;
                  for (; T--; ) {
                    if (dt === b || b !== null && dt === b.alternate) {
                      fe = dt;
                      break t;
                    }
                    dt = fe(dt), b = fe(b);
                  }
                  fe = null;
                }
              else fe = null;
              Y !== null && gh(
                _,
                E,
                Y,
                fe,
                !1
              ), ue !== null && Wt !== null && gh(
                _,
                Wt,
                ue,
                fe,
                !0
              );
            }
          }
          e: {
            if (E = p ? he(p) : window, Y = E.nodeName && E.nodeName.toLowerCase(), Y === "select" || Y === "input" && E.type === "file")
              var ie = Bc;
            else if (Bm(E))
              if (GS)
                ie = Os;
              else {
                ie = Ym;
                var we = t1;
              }
            else
              Y = E.nodeName, !Y || Y.toLowerCase() !== "input" || E.type !== "checkbox" && E.type !== "radio" ? p && du(p.elementType) && (ie = Bc) : ie = qm;
            if (ie && (ie = ie(e, p))) {
              Ts(
                _,
                ie,
                a,
                z
              );
              break e;
            }
            we && we(e, E, p), e === "focusout" && p && E.type === "number" && p.memoizedProps.value != null && Rm(E, "number", E.value);
          }
          switch (we = p ? he(p) : window, e) {
            case "focusin":
              (Bm(we) || we.contentEditable === "true") && (kh = we, E1 = p, B0 = null);
              break;
            case "focusout":
              B0 = E1 = kh = null;
              break;
            case "mousedown":
              T1 = !0;
              break;
            case "contextmenu":
            case "mouseup":
            case "dragend":
              T1 = !1, Np(
                _,
                a,
                z
              );
              break;
            case "selectionchange":
              if (YE) break;
            case "keydown":
            case "keyup":
              Np(
                _,
                a,
                z
              );
          }
          var Te;
          if (b1)
            e: {
              switch (e) {
                case "compositionstart":
                  var ve = "onCompositionStart";
                  break e;
                case "compositionend":
                  ve = "onCompositionEnd";
                  break e;
                case "compositionupdate":
                  ve = "onCompositionUpdate";
                  break e;
              }
              ve = void 0;
            }
          else
            $h ? Xo(e, a) && (ve = "onCompositionEnd") : e === "keydown" && a.keyCode === jS && (ve = "onCompositionStart");
          ve && (BS && a.locale !== "ko" && ($h || ve !== "onCompositionStart" ? ve === "onCompositionEnd" && $h && (Te = Ri()) : (Qf = z, p1 = "value" in Qf ? Qf.value : Qf.textContent, $h = !0)), we = Wn(
            p,
            ve
          ), 0 < we.length && (ve = new NS(
            ve,
            e,
            null,
            a,
            z
          ), _.push({
            event: ve,
            listeners: we
          }), Te ? ve.data = Te : (Te = tc(a), Te !== null && (ve.data = Te)))), (Te = jE ? jm(e, a) : md(e, a)) && (ve = Wn(
            p,
            "onBeforeInput"
          ), 0 < ve.length && (we = new SE(
            "onBeforeInput",
            "beforeinput",
            null,
            a,
            z
          ), _.push({
            event: we,
            listeners: ve
          }), we.data = Te)), ft(
            _,
            e,
            p,
            a,
            z
          );
        }
        _t(_, t);
      });
    }
    function Vt(e, t, a) {
      return {
        instance: e,
        listener: t,
        currentTarget: a
      };
    }
    function Wn(e, t) {
      for (var a = t + "Capture", c = []; e !== null; ) {
        var o = e, f = o.stateNode;
        if (o = o.tag, o !== 5 && o !== 26 && o !== 27 || f === null || (o = hu(e, a), o != null && c.unshift(
          Vt(e, o, f)
        ), o = hu(e, t), o != null && c.push(
          Vt(e, o, f)
        )), e.tag === 3) return c;
        e = e.return;
      }
      return [];
    }
    function ao(e) {
      if (e === null) return null;
      do
        e = e.return;
      while (e && e.tag !== 5 && e.tag !== 27);
      return e || null;
    }
    function gh(e, t, a, c, o) {
      for (var f = t._reactName, d = []; a !== null && a !== c; ) {
        var h = a, y = h.alternate, p = h.stateNode;
        if (h = h.tag, y !== null && y === c) break;
        h !== 5 && h !== 26 && h !== 27 || p === null || (y = p, o ? (p = hu(a, f), p != null && d.unshift(
          Vt(a, p, y)
        )) : o || (p = hu(a, f), p != null && d.push(
          Vt(a, p, y)
        ))), a = a.return;
      }
      d.length !== 0 && e.push({ event: t, listeners: d });
    }
    function Aa(e, t) {
      _p(e, t), e !== "input" && e !== "textarea" && e !== "select" || t == null || t.value !== null || CS || (CS = !0, e === "select" && t.multiple ? console.error(
        "`value` prop on `%s` should not be null. Consider using an empty array when `multiple` is set to `true` to clear the component or `undefined` for uncontrolled components.",
        e
      ) : console.error(
        "`value` prop on `%s` should not be null. Consider using an empty string to clear the component or `undefined` for uncontrolled components.",
        e
      ));
      var a = {
        registrationNameDependencies: Gu,
        possibleRegistrationNames: Xf
      };
      du(e) || typeof t.is == "string" || e1(e, t, a), t.contentEditable && !t.suppressContentEditableWarning && t.children != null && console.error(
        "A component is `contentEditable` and contains `children` managed by React. It is now your responsibility to guarantee that none of those nodes are unexpectedly modified or duplicated. This is probably not intentional."
      );
    }
    function ul(e, t, a, c) {
      t !== a && (a = Fn(a), Fn(t) !== a && (c[e] = t));
    }
    function rr(e, t, a) {
      t.forEach(function(c) {
        a[pc(c)] = c === "style" ? ii(e) : e.getAttribute(c);
      });
    }
    function cl(e, t) {
      t === !1 ? console.error(
        "Expected `%s` listener to be a function, instead got `false`.\n\nIf you used to conditionally omit it with %s={condition && value}, pass %s={condition ? value : undefined} instead.",
        e,
        e,
        e
      ) : console.error(
        "Expected `%s` listener to be a function, instead got a value of `%s` type.",
        e,
        typeof t
      );
    }
    function vh(e, t) {
      return e = e.namespaceURI === Ve || e.namespaceURI === We ? e.ownerDocument.createElementNS(
        e.namespaceURI,
        e.tagName
      ) : e.ownerDocument.createElement(e.tagName), e.innerHTML = t, e.innerHTML;
    }
    function Fn(e) {
      return Ga(e) && (console.error(
        "The provided HTML markup uses a value of unsupported type %s. This value must be coerced to a string before using it here.",
        Mc(e)
      ), iu(e)), (typeof e == "string" ? e : "" + e).replace(sT, `
`).replace(rT, "");
    }
    function Iy(e, t) {
      return t = Fn(t), Fn(e) === t;
    }
    function Tt(e, t, a, c, o, f) {
      switch (a) {
        case "children":
          typeof c == "string" ? (vs(c, t, !1), t === "body" || t === "textarea" && c === "" || Di(e, c)) : (typeof c == "number" || typeof c == "bigint") && (vs("" + c, t, !1), t !== "body" && Di(e, "" + c));
          break;
        case "className":
          ys(e, "class", c);
          break;
        case "tabIndex":
          ys(e, "tabindex", c);
          break;
        case "dir":
        case "role":
        case "viewBox":
        case "width":
        case "height":
          ys(e, a, c);
          break;
        case "style":
          xm(e, c, f);
          break;
        case "data":
          if (t !== "object") {
            ys(e, "data", c);
            break;
          }
        case "src":
        case "href":
          if (c === "" && (t !== "a" || a !== "href")) {
            console.error(
              a === "src" ? 'An empty string ("") was passed to the %s attribute. This may cause the browser to download the whole page again over the network. To fix this, either do not render the element at all or pass null to %s instead of an empty string.' : 'An empty string ("") was passed to the %s attribute. To fix this, either do not render the element at all or pass null to %s instead of an empty string.',
              a,
              a
            ), e.removeAttribute(a);
            break;
          }
          if (c == null || typeof c == "function" || typeof c == "symbol" || typeof c == "boolean") {
            e.removeAttribute(a);
            break;
          }
          vt(c, a), c = Ss("" + c), e.setAttribute(a, c);
          break;
        case "action":
        case "formAction":
          if (c != null && (t === "form" ? a === "formAction" ? console.error(
            "You can only pass the formAction prop to <input> or <button>. Use the action prop on <form>."
          ) : typeof c == "function" && (o.encType == null && o.method == null || Bv || (Bv = !0, console.error(
            "Cannot specify a encType or method for a form that specifies a function as the action. React provides those automatically. They will get overridden."
          )), o.target == null || jv || (jv = !0, console.error(
            "Cannot specify a target for a form that specifies a function as the action. The function will always be executed in the same window."
          ))) : t === "input" || t === "button" ? a === "action" ? console.error(
            "You can only pass the action prop to <form>. Use the formAction prop on <input> or <button>."
          ) : t !== "input" || o.type === "submit" || o.type === "image" || Hv ? t !== "button" || o.type == null || o.type === "submit" || Hv ? typeof c == "function" && (o.name == null || y2 || (y2 = !0, console.error(
            'Cannot specify a "name" prop for a button that specifies a function as a formAction. React needs it to encode which action should be invoked. It will get overridden.'
          )), o.formEncType == null && o.formMethod == null || Bv || (Bv = !0, console.error(
            "Cannot specify a formEncType or formMethod for a button that specifies a function as a formAction. React provides those automatically. They will get overridden."
          )), o.formTarget == null || jv || (jv = !0, console.error(
            "Cannot specify a formTarget for a button that specifies a function as a formAction. The function will always be executed in the same window."
          ))) : (Hv = !0, console.error(
            'A button can only specify a formAction along with type="submit" or no type.'
          )) : (Hv = !0, console.error(
            'An input can only specify a formAction along with type="submit" or type="image".'
          )) : console.error(
            a === "action" ? "You can only pass the action prop to <form>." : "You can only pass the formAction prop to <input> or <button>."
          )), typeof c == "function") {
            e.setAttribute(
              a,
              "javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')"
            );
            break;
          } else
            typeof f == "function" && (a === "formAction" ? (t !== "input" && Tt(e, t, "name", o.name, o, null), Tt(
              e,
              t,
              "formEncType",
              o.formEncType,
              o,
              null
            ), Tt(
              e,
              t,
              "formMethod",
              o.formMethod,
              o,
              null
            ), Tt(
              e,
              t,
              "formTarget",
              o.formTarget,
              o,
              null
            )) : (Tt(
              e,
              t,
              "encType",
              o.encType,
              o,
              null
            ), Tt(e, t, "method", o.method, o, null), Tt(
              e,
              t,
              "target",
              o.target,
              o,
              null
            )));
          if (c == null || typeof c == "symbol" || typeof c == "boolean") {
            e.removeAttribute(a);
            break;
          }
          vt(c, a), c = Ss("" + c), e.setAttribute(a, c);
          break;
        case "onClick":
          c != null && (typeof c != "function" && cl(a, c), e.onclick = yn);
          break;
        case "onScroll":
          c != null && (typeof c != "function" && cl(a, c), xe("scroll", e));
          break;
        case "onScrollEnd":
          c != null && (typeof c != "function" && cl(a, c), xe("scrollend", e));
          break;
        case "dangerouslySetInnerHTML":
          if (c != null) {
            if (typeof c != "object" || !("__html" in c))
              throw Error(
                "`props.dangerouslySetInnerHTML` must be in the form `{__html: ...}`. Please visit https://react.dev/link/dangerously-set-inner-html for more information."
              );
            if (a = c.__html, a != null) {
              if (o.children != null)
                throw Error(
                  "Can only set one of `children` or `props.dangerouslySetInnerHTML`."
                );
              e.innerHTML = a;
            }
          }
          break;
        case "multiple":
          e.multiple = c && typeof c != "function" && typeof c != "symbol";
          break;
        case "muted":
          e.muted = c && typeof c != "function" && typeof c != "symbol";
          break;
        case "suppressContentEditableWarning":
        case "suppressHydrationWarning":
        case "defaultValue":
        case "defaultChecked":
        case "innerHTML":
        case "ref":
          break;
        case "autoFocus":
          break;
        case "xlinkHref":
          if (c == null || typeof c == "function" || typeof c == "boolean" || typeof c == "symbol") {
            e.removeAttribute("xlink:href");
            break;
          }
          vt(c, a), a = Ss("" + c), e.setAttributeNS($r, "xlink:href", a);
          break;
        case "contentEditable":
        case "spellCheck":
        case "draggable":
        case "value":
        case "autoReverse":
        case "externalResourcesRequired":
        case "focusable":
        case "preserveAlpha":
          c != null && typeof c != "function" && typeof c != "symbol" ? (vt(c, a), e.setAttribute(a, "" + c)) : e.removeAttribute(a);
          break;
        case "inert":
          c !== "" || Yv[a] || (Yv[a] = !0, console.error(
            "Received an empty string for a boolean attribute `%s`. This will treat the attribute as if it were false. Either pass `false` to silence this warning, or pass `true` if you used an empty string in earlier versions of React to indicate this attribute is true.",
            a
          ));
        case "allowFullScreen":
        case "async":
        case "autoPlay":
        case "controls":
        case "default":
        case "defer":
        case "disabled":
        case "disablePictureInPicture":
        case "disableRemotePlayback":
        case "formNoValidate":
        case "hidden":
        case "loop":
        case "noModule":
        case "noValidate":
        case "open":
        case "playsInline":
        case "readOnly":
        case "required":
        case "reversed":
        case "scoped":
        case "seamless":
        case "itemScope":
          c && typeof c != "function" && typeof c != "symbol" ? e.setAttribute(a, "") : e.removeAttribute(a);
          break;
        case "capture":
        case "download":
          c === !0 ? e.setAttribute(a, "") : c !== !1 && c != null && typeof c != "function" && typeof c != "symbol" ? (vt(c, a), e.setAttribute(a, c)) : e.removeAttribute(a);
          break;
        case "cols":
        case "rows":
        case "size":
        case "span":
          c != null && typeof c != "function" && typeof c != "symbol" && !isNaN(c) && 1 <= c ? (vt(c, a), e.setAttribute(a, c)) : e.removeAttribute(a);
          break;
        case "rowSpan":
        case "start":
          c == null || typeof c == "function" || typeof c == "symbol" || isNaN(c) ? e.removeAttribute(a) : (vt(c, a), e.setAttribute(a, c));
          break;
        case "popover":
          xe("beforetoggle", e), xe("toggle", e), Ho(e, "popover", c);
          break;
        case "xlinkActuate":
          fu(
            e,
            $r,
            "xlink:actuate",
            c
          );
          break;
        case "xlinkArcrole":
          fu(
            e,
            $r,
            "xlink:arcrole",
            c
          );
          break;
        case "xlinkRole":
          fu(
            e,
            $r,
            "xlink:role",
            c
          );
          break;
        case "xlinkShow":
          fu(
            e,
            $r,
            "xlink:show",
            c
          );
          break;
        case "xlinkTitle":
          fu(
            e,
            $r,
            "xlink:title",
            c
          );
          break;
        case "xlinkType":
          fu(
            e,
            $r,
            "xlink:type",
            c
          );
          break;
        case "xmlBase":
          fu(
            e,
            yS,
            "xml:base",
            c
          );
          break;
        case "xmlLang":
          fu(
            e,
            yS,
            "xml:lang",
            c
          );
          break;
        case "xmlSpace":
          fu(
            e,
            yS,
            "xml:space",
            c
          );
          break;
        case "is":
          f != null && console.error(
            'Cannot update the "is" prop after it has been initialized.'
          ), Ho(e, "is", c);
          break;
        case "innerText":
        case "textContent":
          break;
        case "popoverTarget":
          p2 || c == null || typeof c != "object" || (p2 = !0, console.error(
            "The `popoverTarget` prop expects the ID of an Element as a string. Received %s instead.",
            c
          ));
        default:
          !(2 < a.length) || a[0] !== "o" && a[0] !== "O" || a[1] !== "n" && a[1] !== "N" ? (a = Dp(a), Ho(e, a, c)) : Gu.hasOwnProperty(a) && c != null && typeof c != "function" && cl(a, c);
      }
    }
    function Ef(e, t, a, c, o, f) {
      switch (a) {
        case "style":
          xm(e, c, f);
          break;
        case "dangerouslySetInnerHTML":
          if (c != null) {
            if (typeof c != "object" || !("__html" in c))
              throw Error(
                "`props.dangerouslySetInnerHTML` must be in the form `{__html: ...}`. Please visit https://react.dev/link/dangerously-set-inner-html for more information."
              );
            if (a = c.__html, a != null) {
              if (o.children != null)
                throw Error(
                  "Can only set one of `children` or `props.dangerouslySetInnerHTML`."
                );
              e.innerHTML = a;
            }
          }
          break;
        case "children":
          typeof c == "string" ? Di(e, c) : (typeof c == "number" || typeof c == "bigint") && Di(e, "" + c);
          break;
        case "onScroll":
          c != null && (typeof c != "function" && cl(a, c), xe("scroll", e));
          break;
        case "onScrollEnd":
          c != null && (typeof c != "function" && cl(a, c), xe("scrollend", e));
          break;
        case "onClick":
          c != null && (typeof c != "function" && cl(a, c), e.onclick = yn);
          break;
        case "suppressContentEditableWarning":
        case "suppressHydrationWarning":
        case "innerHTML":
        case "ref":
          break;
        case "innerText":
        case "textContent":
          break;
        default:
          if (Gu.hasOwnProperty(a))
            c != null && typeof c != "function" && cl(a, c);
          else
            e: {
              if (a[0] === "o" && a[1] === "n" && (o = a.endsWith("Capture"), t = a.slice(2, o ? a.length - 7 : void 0), f = e[Da] || null, f = f != null ? f[a] : null, typeof f == "function" && e.removeEventListener(t, f, o), typeof c == "function")) {
                typeof f != "function" && f !== null && (a in e ? e[a] = null : e.hasAttribute(a) && e.removeAttribute(a)), e.addEventListener(t, c, o);
                break e;
              }
              a in e ? e[a] = c : c === !0 ? e.setAttribute(a, "") : Ho(e, a, c);
            }
      }
    }
    function Pt(e, t, a) {
      switch (Aa(t, a), t) {
        case "div":
        case "span":
        case "svg":
        case "path":
        case "a":
        case "g":
        case "p":
        case "li":
          break;
        case "img":
          xe("error", e), xe("load", e);
          var c = !1, o = !1, f;
          for (f in a)
            if (a.hasOwnProperty(f)) {
              var d = a[f];
              if (d != null)
                switch (f) {
                  case "src":
                    c = !0;
                    break;
                  case "srcSet":
                    o = !0;
                    break;
                  case "children":
                  case "dangerouslySetInnerHTML":
                    throw Error(
                      t + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`."
                    );
                  default:
                    Tt(e, t, f, d, a, null);
                }
            }
          o && Tt(e, t, "srcSet", a.srcSet, a, null), c && Tt(e, t, "src", a.src, a, null);
          return;
        case "input":
          la("input", a), xe("invalid", e);
          var h = f = d = o = null, y = null, p = null;
          for (c in a)
            if (a.hasOwnProperty(c)) {
              var z = a[c];
              if (z != null)
                switch (c) {
                  case "name":
                    o = z;
                    break;
                  case "type":
                    d = z;
                    break;
                  case "checked":
                    y = z;
                    break;
                  case "defaultChecked":
                    p = z;
                    break;
                  case "value":
                    f = z;
                    break;
                  case "defaultValue":
                    h = z;
                    break;
                  case "children":
                  case "dangerouslySetInnerHTML":
                    if (z != null)
                      throw Error(
                        t + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`."
                      );
                    break;
                  default:
                    Tt(e, t, c, z, a, null);
                }
            }
          ra(e, a), ud(
            e,
            f,
            h,
            y,
            p,
            d,
            o,
            !1
          );
          return;
        case "select":
          la("select", a), xe("invalid", e), c = d = f = null;
          for (o in a)
            if (a.hasOwnProperty(o) && (h = a[o], h != null))
              switch (o) {
                case "value":
                  f = h;
                  break;
                case "defaultValue":
                  d = h;
                  break;
                case "multiple":
                  c = h;
                default:
                  Tt(
                    e,
                    t,
                    o,
                    h,
                    a,
                    null
                  );
              }
          cd(e, a), t = f, a = d, e.multiple = !!c, t != null ? su(e, !!c, t, !1) : a != null && su(e, !!c, a, !0);
          return;
        case "textarea":
          la("textarea", a), xe("invalid", e), f = o = c = null;
          for (d in a)
            if (a.hasOwnProperty(d) && (h = a[d], h != null))
              switch (d) {
                case "value":
                  c = h;
                  break;
                case "defaultValue":
                  o = h;
                  break;
                case "children":
                  f = h;
                  break;
                case "dangerouslySetInnerHTML":
                  if (h != null)
                    throw Error(
                      "`dangerouslySetInnerHTML` does not make sense on <textarea>."
                    );
                  break;
                default:
                  Tt(
                    e,
                    t,
                    d,
                    h,
                    a,
                    null
                  );
              }
          Ti(e, a), jo(e, c, o, f);
          return;
        case "option":
          zp(e, a);
          for (y in a)
            a.hasOwnProperty(y) && (c = a[y], c != null) && (y === "selected" ? e.selected = c && typeof c != "function" && typeof c != "symbol" : Tt(e, t, y, c, a, null));
          return;
        case "dialog":
          xe("beforetoggle", e), xe("toggle", e), xe("cancel", e), xe("close", e);
          break;
        case "iframe":
        case "object":
          xe("load", e);
          break;
        case "video":
        case "audio":
          for (c = 0; c < dp.length; c++)
            xe(dp[c], e);
          break;
        case "image":
          xe("error", e), xe("load", e);
          break;
        case "details":
          xe("toggle", e);
          break;
        case "embed":
        case "source":
        case "link":
          xe("error", e), xe("load", e);
        case "area":
        case "base":
        case "br":
        case "col":
        case "hr":
        case "keygen":
        case "meta":
        case "param":
        case "track":
        case "wbr":
        case "menuitem":
          for (p in a)
            if (a.hasOwnProperty(p) && (c = a[p], c != null))
              switch (p) {
                case "children":
                case "dangerouslySetInnerHTML":
                  throw Error(
                    t + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`."
                  );
                default:
                  Tt(e, t, p, c, a, null);
              }
          return;
        default:
          if (du(t)) {
            for (z in a)
              a.hasOwnProperty(z) && (c = a[z], c !== void 0 && Ef(
                e,
                t,
                z,
                c,
                a,
                void 0
              ));
            return;
          }
      }
      for (h in a)
        a.hasOwnProperty(h) && (c = a[h], c != null && Tt(e, t, h, c, a, null));
    }
    function _l(e, t, a, c) {
      switch (Aa(t, c), t) {
        case "div":
        case "span":
        case "svg":
        case "path":
        case "a":
        case "g":
        case "p":
        case "li":
          break;
        case "input":
          var o = null, f = null, d = null, h = null, y = null, p = null, z = null;
          for (Y in a) {
            var _ = a[Y];
            if (a.hasOwnProperty(Y) && _ != null)
              switch (Y) {
                case "checked":
                  break;
                case "value":
                  break;
                case "defaultValue":
                  y = _;
                default:
                  c.hasOwnProperty(Y) || Tt(
                    e,
                    t,
                    Y,
                    null,
                    c,
                    _
                  );
              }
          }
          for (var E in c) {
            var Y = c[E];
            if (_ = a[E], c.hasOwnProperty(E) && (Y != null || _ != null))
              switch (E) {
                case "type":
                  f = Y;
                  break;
                case "name":
                  o = Y;
                  break;
                case "checked":
                  p = Y;
                  break;
                case "defaultChecked":
                  z = Y;
                  break;
                case "value":
                  d = Y;
                  break;
                case "defaultValue":
                  h = Y;
                  break;
                case "children":
                case "dangerouslySetInnerHTML":
                  if (Y != null)
                    throw Error(
                      t + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`."
                    );
                  break;
                default:
                  Y !== _ && Tt(
                    e,
                    t,
                    E,
                    Y,
                    c,
                    _
                  );
              }
          }
          t = a.type === "checkbox" || a.type === "radio" ? a.checked != null : a.value != null, c = c.type === "checkbox" || c.type === "radio" ? c.checked != null : c.value != null, t || !c || m2 || (console.error(
            "A component is changing an uncontrolled input to be controlled. This is likely caused by the value changing from undefined to a defined value, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://react.dev/link/controlled-components"
          ), m2 = !0), !t || c || h2 || (console.error(
            "A component is changing a controlled input to be uncontrolled. This is likely caused by the value changing from a defined to undefined, which should not happen. Decide between using a controlled or uncontrolled input element for the lifetime of the component. More info: https://react.dev/link/controlled-components"
          ), h2 = !0), Nc(
            e,
            d,
            h,
            y,
            p,
            z,
            f,
            o
          );
          return;
        case "select":
          Y = d = h = E = null;
          for (f in a)
            if (y = a[f], a.hasOwnProperty(f) && y != null)
              switch (f) {
                case "value":
                  break;
                case "multiple":
                  Y = y;
                default:
                  c.hasOwnProperty(f) || Tt(
                    e,
                    t,
                    f,
                    null,
                    c,
                    y
                  );
              }
          for (o in c)
            if (f = c[o], y = a[o], c.hasOwnProperty(o) && (f != null || y != null))
              switch (o) {
                case "value":
                  E = f;
                  break;
                case "defaultValue":
                  h = f;
                  break;
                case "multiple":
                  d = f;
                default:
                  f !== y && Tt(
                    e,
                    t,
                    o,
                    f,
                    c,
                    y
                  );
              }
          c = h, t = d, a = Y, E != null ? su(e, !!t, E, !1) : !!a != !!t && (c != null ? su(e, !!t, c, !0) : su(e, !!t, t ? [] : "", !1));
          return;
        case "textarea":
          Y = E = null;
          for (h in a)
            if (o = a[h], a.hasOwnProperty(h) && o != null && !c.hasOwnProperty(h))
              switch (h) {
                case "value":
                  break;
                case "children":
                  break;
                default:
                  Tt(e, t, h, null, c, o);
              }
          for (d in c)
            if (o = c[d], f = a[d], c.hasOwnProperty(d) && (o != null || f != null))
              switch (d) {
                case "value":
                  E = o;
                  break;
                case "defaultValue":
                  Y = o;
                  break;
                case "children":
                  break;
                case "dangerouslySetInnerHTML":
                  if (o != null)
                    throw Error(
                      "`dangerouslySetInnerHTML` does not make sense on <textarea>."
                    );
                  break;
                default:
                  o !== f && Tt(e, t, d, o, c, f);
              }
          Ai(e, E, Y);
          return;
        case "option":
          for (var ue in a)
            E = a[ue], a.hasOwnProperty(ue) && E != null && !c.hasOwnProperty(ue) && (ue === "selected" ? e.selected = !1 : Tt(
              e,
              t,
              ue,
              null,
              c,
              E
            ));
          for (y in c)
            E = c[y], Y = a[y], c.hasOwnProperty(y) && E !== Y && (E != null || Y != null) && (y === "selected" ? e.selected = E && typeof E != "function" && typeof E != "symbol" : Tt(
              e,
              t,
              y,
              E,
              c,
              Y
            ));
          return;
        case "img":
        case "link":
        case "area":
        case "base":
        case "br":
        case "col":
        case "embed":
        case "hr":
        case "keygen":
        case "meta":
        case "param":
        case "source":
        case "track":
        case "wbr":
        case "menuitem":
          for (var fe in a)
            E = a[fe], a.hasOwnProperty(fe) && E != null && !c.hasOwnProperty(fe) && Tt(
              e,
              t,
              fe,
              null,
              c,
              E
            );
          for (p in c)
            if (E = c[p], Y = a[p], c.hasOwnProperty(p) && E !== Y && (E != null || Y != null))
              switch (p) {
                case "children":
                case "dangerouslySetInnerHTML":
                  if (E != null)
                    throw Error(
                      t + " is a void element tag and must neither have `children` nor use `dangerouslySetInnerHTML`."
                    );
                  break;
                default:
                  Tt(
                    e,
                    t,
                    p,
                    E,
                    c,
                    Y
                  );
              }
          return;
        default:
          if (du(t)) {
            for (var Wt in a)
              E = a[Wt], a.hasOwnProperty(Wt) && E !== void 0 && !c.hasOwnProperty(Wt) && Ef(
                e,
                t,
                Wt,
                void 0,
                c,
                E
              );
            for (z in c)
              E = c[z], Y = a[z], !c.hasOwnProperty(z) || E === Y || E === void 0 && Y === void 0 || Ef(
                e,
                t,
                z,
                E,
                c,
                Y
              );
            return;
          }
      }
      for (var dt in a)
        E = a[dt], a.hasOwnProperty(dt) && E != null && !c.hasOwnProperty(dt) && Tt(e, t, dt, null, c, E);
      for (_ in c)
        E = c[_], Y = a[_], !c.hasOwnProperty(_) || E === Y || E == null && Y == null || Tt(e, t, _, E, c, Y);
    }
    function pc(e) {
      switch (e) {
        case "class":
          return "className";
        case "for":
          return "htmlFor";
        default:
          return e;
      }
    }
    function ii(e) {
      var t = {};
      e = e.style;
      for (var a = 0; a < e.length; a++) {
        var c = e[a];
        t[c] = e.getPropertyValue(c);
      }
      return t;
    }
    function Hu(e, t, a) {
      if (t != null && typeof t != "object")
        console.error(
          "The `style` prop expects a mapping from style properties to values, not a string. For example, style={{marginRight: spacing + 'em'}} when using JSX."
        );
      else {
        var c, o = c = "", f;
        for (f in t)
          if (t.hasOwnProperty(f)) {
            var d = t[f];
            d != null && typeof d != "boolean" && d !== "" && (f.indexOf("--") === 0 ? (ta(d, f), c += o + f + ":" + ("" + d).trim()) : typeof d != "number" || d === 0 || ye.has(f) ? (ta(d, f), c += o + f.replace(X, "-$1").toLowerCase().replace(re, "-ms-") + ":" + ("" + d).trim()) : c += o + f.replace(X, "-$1").toLowerCase().replace(re, "-ms-") + ":" + d + "px", o = ";");
          }
        c = c || null, t = e.getAttribute("style"), t !== c && (c = Fn(c), Fn(t) !== c && (a.style = ii(e)));
      }
    }
    function xa(e, t, a, c, o, f) {
      if (o.delete(a), e = e.getAttribute(a), e === null)
        switch (typeof c) {
          case "undefined":
          case "function":
          case "symbol":
          case "boolean":
            return;
        }
      else if (c != null)
        switch (typeof c) {
          case "function":
          case "symbol":
          case "boolean":
            break;
          default:
            if (vt(c, t), e === "" + c)
              return;
        }
      ul(t, e, c, f);
    }
    function Sh(e, t, a, c, o, f) {
      if (o.delete(a), e = e.getAttribute(a), e === null) {
        switch (typeof c) {
          case "function":
          case "symbol":
            return;
        }
        if (!c) return;
      } else
        switch (typeof c) {
          case "function":
          case "symbol":
            break;
          default:
            if (c) return;
        }
      ul(t, e, c, f);
    }
    function bh(e, t, a, c, o, f) {
      if (o.delete(a), e = e.getAttribute(a), e === null)
        switch (typeof c) {
          case "undefined":
          case "function":
          case "symbol":
            return;
        }
      else if (c != null)
        switch (typeof c) {
          case "function":
          case "symbol":
            break;
          default:
            if (vt(c, a), e === "" + c)
              return;
        }
      ul(t, e, c, f);
    }
    function Tf(e, t, a, c, o, f) {
      if (o.delete(a), e = e.getAttribute(a), e === null)
        switch (typeof c) {
          case "undefined":
          case "function":
          case "symbol":
          case "boolean":
            return;
          default:
            if (isNaN(c)) return;
        }
      else if (c != null)
        switch (typeof c) {
          case "function":
          case "symbol":
          case "boolean":
            break;
          default:
            if (!isNaN(c) && (vt(c, t), e === "" + c))
              return;
        }
      ul(t, e, c, f);
    }
    function dr(e, t, a, c, o, f) {
      if (o.delete(a), e = e.getAttribute(a), e === null)
        switch (typeof c) {
          case "undefined":
          case "function":
          case "symbol":
          case "boolean":
            return;
        }
      else if (c != null)
        switch (typeof c) {
          case "function":
          case "symbol":
          case "boolean":
            break;
          default:
            if (vt(c, t), a = Ss("" + c), e === a)
              return;
        }
      ul(t, e, c, f);
    }
    function Na(e, t, a, c) {
      for (var o = {}, f = /* @__PURE__ */ new Set(), d = e.attributes, h = 0; h < d.length; h++)
        switch (d[h].name.toLowerCase()) {
          case "value":
            break;
          case "checked":
            break;
          case "selected":
            break;
          default:
            f.add(d[h].name);
        }
      if (du(t)) {
        for (var y in a)
          if (a.hasOwnProperty(y)) {
            var p = a[y];
            if (p != null) {
              if (Gu.hasOwnProperty(y))
                typeof p != "function" && cl(y, p);
              else if (a.suppressHydrationWarning !== !0)
                switch (y) {
                  case "children":
                    typeof p != "string" && typeof p != "number" || ul(
                      "children",
                      e.textContent,
                      p,
                      o
                    );
                    continue;
                  case "suppressContentEditableWarning":
                  case "suppressHydrationWarning":
                  case "defaultValue":
                  case "defaultChecked":
                  case "innerHTML":
                  case "ref":
                    continue;
                  case "dangerouslySetInnerHTML":
                    d = e.innerHTML, p = p ? p.__html : void 0, p != null && (p = vh(e, p), ul(
                      y,
                      d,
                      p,
                      o
                    ));
                    continue;
                  case "style":
                    f.delete(y), Hu(e, p, o);
                    continue;
                  case "offsetParent":
                  case "offsetTop":
                  case "offsetLeft":
                  case "offsetWidth":
                  case "offsetHeight":
                  case "isContentEditable":
                  case "outerText":
                  case "outerHTML":
                    f.delete(y.toLowerCase()), console.error(
                      "Assignment to read-only property will result in a no-op: `%s`",
                      y
                    );
                    continue;
                  case "className":
                    f.delete("class"), d = xc(
                      e,
                      "class",
                      p
                    ), ul(
                      "className",
                      d,
                      p,
                      o
                    );
                    continue;
                  default:
                    c.context === _o && t !== "svg" && t !== "math" ? f.delete(y.toLowerCase()) : f.delete(y), d = xc(
                      e,
                      y,
                      p
                    ), ul(
                      y,
                      d,
                      p,
                      o
                    );
                }
            }
          }
      } else
        for (p in a)
          if (a.hasOwnProperty(p) && (y = a[p], y != null)) {
            if (Gu.hasOwnProperty(p))
              typeof y != "function" && cl(p, y);
            else if (a.suppressHydrationWarning !== !0)
              switch (p) {
                case "children":
                  typeof y != "string" && typeof y != "number" || ul(
                    "children",
                    e.textContent,
                    y,
                    o
                  );
                  continue;
                case "suppressContentEditableWarning":
                case "suppressHydrationWarning":
                case "value":
                case "checked":
                case "selected":
                case "defaultValue":
                case "defaultChecked":
                case "innerHTML":
                case "ref":
                  continue;
                case "dangerouslySetInnerHTML":
                  d = e.innerHTML, y = y ? y.__html : void 0, y != null && (y = vh(e, y), d !== y && (o[p] = { __html: d }));
                  continue;
                case "className":
                  xa(
                    e,
                    p,
                    "class",
                    y,
                    f,
                    o
                  );
                  continue;
                case "tabIndex":
                  xa(
                    e,
                    p,
                    "tabindex",
                    y,
                    f,
                    o
                  );
                  continue;
                case "style":
                  f.delete(p), Hu(e, y, o);
                  continue;
                case "multiple":
                  f.delete(p), ul(
                    p,
                    e.multiple,
                    y,
                    o
                  );
                  continue;
                case "muted":
                  f.delete(p), ul(
                    p,
                    e.muted,
                    y,
                    o
                  );
                  continue;
                case "autoFocus":
                  f.delete("autofocus"), ul(
                    p,
                    e.autofocus,
                    y,
                    o
                  );
                  continue;
                case "data":
                  if (t !== "object") {
                    f.delete(p), d = e.getAttribute("data"), ul(
                      p,
                      d,
                      y,
                      o
                    );
                    continue;
                  }
                case "src":
                case "href":
                  if (!(y !== "" || t === "a" && p === "href" || t === "object" && p === "data")) {
                    console.error(
                      p === "src" ? 'An empty string ("") was passed to the %s attribute. This may cause the browser to download the whole page again over the network. To fix this, either do not render the element at all or pass null to %s instead of an empty string.' : 'An empty string ("") was passed to the %s attribute. To fix this, either do not render the element at all or pass null to %s instead of an empty string.',
                      p,
                      p
                    );
                    continue;
                  }
                  dr(
                    e,
                    p,
                    p,
                    y,
                    f,
                    o
                  );
                  continue;
                case "action":
                case "formAction":
                  if (d = e.getAttribute(p), typeof y == "function") {
                    f.delete(p.toLowerCase()), p === "formAction" ? (f.delete("name"), f.delete("formenctype"), f.delete("formmethod"), f.delete("formtarget")) : (f.delete("enctype"), f.delete("method"), f.delete("target"));
                    continue;
                  } else if (d === dT) {
                    f.delete(p.toLowerCase()), ul(
                      p,
                      "function",
                      y,
                      o
                    );
                    continue;
                  }
                  dr(
                    e,
                    p,
                    p.toLowerCase(),
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkHref":
                  dr(
                    e,
                    p,
                    "xlink:href",
                    y,
                    f,
                    o
                  );
                  continue;
                case "contentEditable":
                  bh(
                    e,
                    p,
                    "contenteditable",
                    y,
                    f,
                    o
                  );
                  continue;
                case "spellCheck":
                  bh(
                    e,
                    p,
                    "spellcheck",
                    y,
                    f,
                    o
                  );
                  continue;
                case "draggable":
                case "autoReverse":
                case "externalResourcesRequired":
                case "focusable":
                case "preserveAlpha":
                  bh(
                    e,
                    p,
                    p,
                    y,
                    f,
                    o
                  );
                  continue;
                case "allowFullScreen":
                case "async":
                case "autoPlay":
                case "controls":
                case "default":
                case "defer":
                case "disabled":
                case "disablePictureInPicture":
                case "disableRemotePlayback":
                case "formNoValidate":
                case "hidden":
                case "loop":
                case "noModule":
                case "noValidate":
                case "open":
                case "playsInline":
                case "readOnly":
                case "required":
                case "reversed":
                case "scoped":
                case "seamless":
                case "itemScope":
                  Sh(
                    e,
                    p,
                    p.toLowerCase(),
                    y,
                    f,
                    o
                  );
                  continue;
                case "capture":
                case "download":
                  e: {
                    h = e;
                    var z = d = p, _ = o;
                    if (f.delete(z), h = h.getAttribute(z), h === null)
                      switch (typeof y) {
                        case "undefined":
                        case "function":
                        case "symbol":
                          break e;
                        default:
                          if (y === !1) break e;
                      }
                    else if (y != null)
                      switch (typeof y) {
                        case "function":
                        case "symbol":
                          break;
                        case "boolean":
                          if (y === !0 && h === "") break e;
                          break;
                        default:
                          if (vt(y, d), h === "" + y)
                            break e;
                      }
                    ul(
                      d,
                      h,
                      y,
                      _
                    );
                  }
                  continue;
                case "cols":
                case "rows":
                case "size":
                case "span":
                  e: {
                    if (h = e, z = d = p, _ = o, f.delete(z), h = h.getAttribute(z), h === null)
                      switch (typeof y) {
                        case "undefined":
                        case "function":
                        case "symbol":
                        case "boolean":
                          break e;
                        default:
                          if (isNaN(y) || 1 > y) break e;
                      }
                    else if (y != null)
                      switch (typeof y) {
                        case "function":
                        case "symbol":
                        case "boolean":
                          break;
                        default:
                          if (!(isNaN(y) || 1 > y) && (vt(y, d), h === "" + y))
                            break e;
                      }
                    ul(
                      d,
                      h,
                      y,
                      _
                    );
                  }
                  continue;
                case "rowSpan":
                  Tf(
                    e,
                    p,
                    "rowspan",
                    y,
                    f,
                    o
                  );
                  continue;
                case "start":
                  Tf(
                    e,
                    p,
                    p,
                    y,
                    f,
                    o
                  );
                  continue;
                case "xHeight":
                  xa(
                    e,
                    p,
                    "x-height",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkActuate":
                  xa(
                    e,
                    p,
                    "xlink:actuate",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkArcrole":
                  xa(
                    e,
                    p,
                    "xlink:arcrole",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkRole":
                  xa(
                    e,
                    p,
                    "xlink:role",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkShow":
                  xa(
                    e,
                    p,
                    "xlink:show",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkTitle":
                  xa(
                    e,
                    p,
                    "xlink:title",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xlinkType":
                  xa(
                    e,
                    p,
                    "xlink:type",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xmlBase":
                  xa(
                    e,
                    p,
                    "xml:base",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xmlLang":
                  xa(
                    e,
                    p,
                    "xml:lang",
                    y,
                    f,
                    o
                  );
                  continue;
                case "xmlSpace":
                  xa(
                    e,
                    p,
                    "xml:space",
                    y,
                    f,
                    o
                  );
                  continue;
                case "inert":
                  y !== "" || Yv[p] || (Yv[p] = !0, console.error(
                    "Received an empty string for a boolean attribute `%s`. This will treat the attribute as if it were false. Either pass `false` to silence this warning, or pass `true` if you used an empty string in earlier versions of React to indicate this attribute is true.",
                    p
                  )), Sh(
                    e,
                    p,
                    p,
                    y,
                    f,
                    o
                  );
                  continue;
                default:
                  if (!(2 < p.length) || p[0] !== "o" && p[0] !== "O" || p[1] !== "n" && p[1] !== "N") {
                    h = Dp(p), d = !1, c.context === _o && t !== "svg" && t !== "math" ? f.delete(h.toLowerCase()) : (z = p.toLowerCase(), z = tu.hasOwnProperty(
                      z
                    ) && tu[z] || null, z !== null && z !== p && (d = !0, f.delete(z)), f.delete(h));
                    e: if (z = e, _ = h, h = y, mn(_))
                      if (z.hasAttribute(_))
                        z = z.getAttribute(
                          _
                        ), vt(
                          h,
                          _
                        ), h = z === "" + h ? h : z;
                      else {
                        switch (typeof h) {
                          case "function":
                          case "symbol":
                            break e;
                          case "boolean":
                            if (z = _.toLowerCase().slice(0, 5), z !== "data-" && z !== "aria-")
                              break e;
                        }
                        h = h === void 0 ? void 0 : null;
                      }
                    else h = void 0;
                    d || ul(
                      p,
                      h,
                      y,
                      o
                    );
                  }
              }
          }
      return 0 < f.size && a.suppressHydrationWarning !== !0 && rr(e, f, o), Object.keys(o).length === 0 ? null : o;
    }
    function dg(e, t) {
      switch (e.length) {
        case 0:
          return "";
        case 1:
          return e[0];
        case 2:
          return e[0] + " " + t + " " + e[1];
        default:
          return e.slice(0, -1).join(", ") + ", " + t + " " + e[e.length - 1];
      }
    }
    function Oa(e) {
      switch (e) {
        case "css":
        case "script":
        case "font":
        case "img":
        case "image":
        case "input":
        case "link":
          return !0;
        default:
          return !1;
      }
    }
    function hg() {
      if (typeof performance.getEntriesByType == "function") {
        for (var e = 0, t = 0, a = performance.getEntriesByType("resource"), c = 0; c < a.length; c++) {
          var o = a[c], f = o.transferSize, d = o.initiatorType, h = o.duration;
          if (f && h && Oa(d)) {
            for (d = 0, h = o.responseEnd, c += 1; c < a.length; c++) {
              var y = a[c], p = y.startTime;
              if (p > h) break;
              var z = y.transferSize, _ = y.initiatorType;
              z && Oa(_) && (y = y.responseEnd, d += z * (y < h ? 1 : (h - p) / (y - p)));
            }
            if (--c, t += 8 * (f + d) / (o.duration / 1e3), e++, 10 < e) break;
          }
        }
        if (0 < e) return t / e / 1e6;
      }
      return navigator.connection && (e = navigator.connection.downlink, typeof e == "number") ? e : 5;
    }
    function hr(e) {
      return e.nodeType === 9 ? e : e.ownerDocument;
    }
    function mg(e) {
      switch (e) {
        case We:
          return bm;
        case Ve:
          return wv;
        default:
          return _o;
      }
    }
    function gc(e, t) {
      if (e === _o)
        switch (t) {
          case "svg":
            return bm;
          case "math":
            return wv;
          default:
            return _o;
        }
      return e === bm && t === "foreignObject" ? _o : e;
    }
    function Af(e, t) {
      return e === "textarea" || e === "noscript" || typeof t.children == "string" || typeof t.children == "number" || typeof t.children == "bigint" || typeof t.dangerouslySetInnerHTML == "object" && t.dangerouslySetInnerHTML !== null && t.dangerouslySetInnerHTML.__html != null;
    }
    function Py() {
      var e = window.event;
      return e && e.type === "popstate" ? e === SS ? !1 : (SS = e, !0) : (SS = null, !1);
    }
    function ju() {
      var e = window.event;
      return e && e !== yp ? e.type : null;
    }
    function Of() {
      var e = window.event;
      return e && e !== yp ? e.timeStamp : -1.1;
    }
    function yg(e) {
      setTimeout(function() {
        throw e;
      });
    }
    function pg(e, t, a) {
      switch (t) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          a.autoFocus && e.focus();
          break;
        case "img":
          a.src ? e.src = a.src : a.srcSet && (e.srcset = a.srcSet);
      }
    }
    function gg() {
    }
    function Eh(e, t, a, c) {
      _l(e, t, a, c), e[Da] = c;
    }
    function Th(e) {
      Di(e, "");
    }
    function o1(e, t, a) {
      e.nodeValue = a;
    }
    function vg(e) {
      if (!e.__reactWarnedAboutChildrenConflict) {
        var t = e[Da] || null;
        if (t !== null) {
          var a = ae(e);
          a !== null && (typeof t.children == "string" || typeof t.children == "number" ? (e.__reactWarnedAboutChildrenConflict = !0, oe(a, function() {
            console.error(
              'Cannot use a ref on a React element as a container to `createRoot` or `createPortal` if that element also sets "children" text content using React. It should be a leaf with no children. Otherwise it\'s ambiguous which children should be used.'
            );
          })) : t.dangerouslySetInnerHTML != null && (e.__reactWarnedAboutChildrenConflict = !0, oe(a, function() {
            console.error(
              'Cannot use a ref on a React element as a container to `createRoot` or `createPortal` if that element also sets "dangerouslySetInnerHTML" using React. It should be a leaf with no children. Otherwise it\'s ambiguous which children should be used.'
            );
          })));
        }
      }
    }
    function oi(e) {
      return e === "head";
    }
    function Sg(e, t) {
      e.removeChild(t);
    }
    function bg(e, t) {
      (e.nodeType === 9 ? e.body : e.nodeName === "HTML" ? e.ownerDocument.body : e).removeChild(t);
    }
    function no(e, t) {
      var a = t, c = 0;
      do {
        var o = a.nextSibling;
        if (e.removeChild(a), o && o.nodeType === 8)
          if (a = o.data, a === mp || a === qv) {
            if (c === 0) {
              e.removeChild(o), oo(t);
              return;
            }
            c--;
          } else if (a === hp || a === is || a === Wr || a === Sm || a === kr)
            c++;
          else if (a === mT)
            Sc(
              e.ownerDocument.documentElement
            );
          else if (a === pT) {
            a = e.ownerDocument.head, Sc(a);
            for (var f = a.firstChild; f; ) {
              var d = f.nextSibling, h = f.nodeName;
              f[Gf] || h === "SCRIPT" || h === "STYLE" || h === "LINK" && f.rel.toLowerCase() === "stylesheet" || a.removeChild(f), f = d;
            }
          } else
            a === yT && Sc(e.ownerDocument.body);
        a = o;
      } while (a);
      oo(t);
    }
    function mr(e, t) {
      var a = e;
      e = 0;
      do {
        var c = a.nextSibling;
        if (a.nodeType === 1 ? t ? (a._stashedDisplay = a.style.display, a.style.display = "none") : (a.style.display = a._stashedDisplay || "", a.getAttribute("style") === "" && a.removeAttribute("style")) : a.nodeType === 3 && (t ? (a._stashedText = a.nodeValue, a.nodeValue = "") : a.nodeValue = a._stashedText || ""), c && c.nodeType === 8)
          if (a = c.data, a === mp) {
            if (e === 0) break;
            e--;
          } else
            a !== hp && a !== is && a !== Wr && a !== Sm || e++;
        a = c;
      } while (a);
    }
    function Eg(e) {
      mr(e, !0);
    }
    function Tg(e) {
      e = e.style, typeof e.setProperty == "function" ? e.setProperty("display", "none", "important") : e.display = "none";
    }
    function Ag(e) {
      e.nodeValue = "";
    }
    function Og(e) {
      mr(e, !1);
    }
    function zg(e, t) {
      t = t[gT], t = t != null && t.hasOwnProperty("display") ? t.display : null, e.style.display = t == null || typeof t == "boolean" ? "" : ("" + t).trim();
    }
    function Dg(e, t) {
      e.nodeValue = t;
    }
    function zf(e) {
      var t = e.firstChild;
      for (t && t.nodeType === 10 && (t = t.nextSibling); t; ) {
        var a = t;
        switch (t = t.nextSibling, a.nodeName) {
          case "HTML":
          case "HEAD":
          case "BODY":
            zf(a), M(a);
            continue;
          case "SCRIPT":
          case "STYLE":
            continue;
          case "LINK":
            if (a.rel.toLowerCase() === "stylesheet") continue;
        }
        e.removeChild(a);
      }
    }
    function Rg(e, t, a, c) {
      for (; e.nodeType === 1; ) {
        var o = a;
        if (e.nodeName.toLowerCase() !== t.toLowerCase()) {
          if (!c && (e.nodeName !== "INPUT" || e.type !== "hidden"))
            break;
        } else if (c) {
          if (!e[Gf])
            switch (t) {
              case "meta":
                if (!e.hasAttribute("itemprop")) break;
                return e;
              case "link":
                if (f = e.getAttribute("rel"), f === "stylesheet" && e.hasAttribute("data-precedence"))
                  break;
                if (f !== o.rel || e.getAttribute("href") !== (o.href == null || o.href === "" ? null : o.href) || e.getAttribute("crossorigin") !== (o.crossOrigin == null ? null : o.crossOrigin) || e.getAttribute("title") !== (o.title == null ? null : o.title))
                  break;
                return e;
              case "style":
                if (e.hasAttribute("data-precedence")) break;
                return e;
              case "script":
                if (f = e.getAttribute("src"), (f !== (o.src == null ? null : o.src) || e.getAttribute("type") !== (o.type == null ? null : o.type) || e.getAttribute("crossorigin") !== (o.crossOrigin == null ? null : o.crossOrigin)) && f && e.hasAttribute("async") && !e.hasAttribute("itemprop"))
                  break;
                return e;
              default:
                return e;
            }
        } else if (t === "input" && e.type === "hidden") {
          vt(o.name, "name");
          var f = o.name == null ? null : "" + o.name;
          if (o.type === "hidden" && e.getAttribute("name") === f)
            return e;
        } else return e;
        if (e = an(e.nextSibling), e === null) break;
      }
      return null;
    }
    function _g(e, t, a) {
      if (t === "") return null;
      for (; e.nodeType !== 3; )
        if ((e.nodeType !== 1 || e.nodeName !== "INPUT" || e.type !== "hidden") && !a || (e = an(e.nextSibling), e === null)) return null;
      return e;
    }
    function Mt(e, t) {
      for (; e.nodeType !== 8; )
        if ((e.nodeType !== 1 || e.nodeName !== "INPUT" || e.type !== "hidden") && !t || (e = an(e.nextSibling), e === null)) return null;
      return e;
    }
    function yr(e) {
      return e.data === is || e.data === Wr;
    }
    function e0(e) {
      return e.data === Sm || e.data === is && e.ownerDocument.readyState !== v2;
    }
    function Mg(e, t) {
      var a = e.ownerDocument;
      if (e.data === Wr)
        e._reactRetry = t;
      else if (e.data !== is || a.readyState !== v2)
        t();
      else {
        var c = function() {
          t(), a.removeEventListener("DOMContentLoaded", c);
        };
        a.addEventListener("DOMContentLoaded", c), e._reactRetry = c;
      }
    }
    function an(e) {
      for (; e != null; e = e.nextSibling) {
        var t = e.nodeType;
        if (t === 1 || t === 3) break;
        if (t === 8) {
          if (t = e.data, t === hp || t === Sm || t === is || t === Wr || t === kr || t === pS || t === g2)
            break;
          if (t === mp || t === qv)
            return null;
        }
      }
      return e;
    }
    function Cg(e) {
      if (e.nodeType === 1) {
        for (var t = e.nodeName.toLowerCase(), a = {}, c = e.attributes, o = 0; o < c.length; o++) {
          var f = c[o];
          a[pc(f.name)] = f.name.toLowerCase() === "style" ? ii(e) : f.value;
        }
        return { type: t, props: a };
      }
      return e.nodeType === 8 ? e.data === kr ? { type: "Activity", props: {} } : { type: "Suspense", props: {} } : e.nodeValue;
    }
    function Ug(e, t, a) {
      return a === null || a[hT] !== !0 ? (e.nodeValue === t ? e = null : (t = Fn(t), e = Fn(e.nodeValue) === t ? null : e.nodeValue), e) : null;
    }
    function Df(e) {
      e = e.nextSibling;
      for (var t = 0; e; ) {
        if (e.nodeType === 8) {
          var a = e.data;
          if (a === mp || a === qv) {
            if (t === 0)
              return an(e.nextSibling);
            t--;
          } else
            a !== hp && a !== Sm && a !== is && a !== Wr && a !== kr || t++;
        }
        e = e.nextSibling;
      }
      return null;
    }
    function uo(e) {
      e = e.previousSibling;
      for (var t = 0; e; ) {
        if (e.nodeType === 8) {
          var a = e.data;
          if (a === hp || a === Sm || a === is || a === Wr || a === kr) {
            if (t === 0) return e;
            t--;
          } else
            a !== mp && a !== qv || t++;
        }
        e = e.previousSibling;
      }
      return null;
    }
    function t0(e) {
      oo(e);
    }
    function Ah(e) {
      oo(e);
    }
    function l0(e) {
      oo(e);
    }
    function vc(e, t, a, c, o) {
      switch (o && gs(e, c.ancestorInfo), t = hr(a), e) {
        case "html":
          if (e = t.documentElement, !e)
            throw Error(
              "React expected an <html> element (document.documentElement) to exist in the Document but one was not found. React never removes the documentElement for any Document it renders into so the cause is likely in some other script running on this page."
            );
          return e;
        case "head":
          if (e = t.head, !e)
            throw Error(
              "React expected a <head> element (document.head) to exist in the Document but one was not found. React never removes the head for any Document it renders into so the cause is likely in some other script running on this page."
            );
          return e;
        case "body":
          if (e = t.body, !e)
            throw Error(
              "React expected a <body> element (document.body) to exist in the Document but one was not found. React never removes the body for any Document it renders into so the cause is likely in some other script running on this page."
            );
          return e;
        default:
          throw Error(
            "resolveSingletonInstance was called with an element type that is not supported. This is a bug in React."
          );
      }
    }
    function Bu(e, t, a, c) {
      if (!a[Ec] && ae(a)) {
        var o = a.tagName.toLowerCase();
        console.error(
          "You are mounting a new %s component when a previous one has not first unmounted. It is an error to render more than one %s component at a time and attributes and children of these components will likely fail in unpredictable ways. Please only render a single instance of <%s> and if you need to mount a new one, ensure any previous ones have unmounted first.",
          o,
          o,
          o
        );
      }
      switch (e) {
        case "html":
        case "head":
        case "body":
          break;
        default:
          console.error(
            "acquireSingletonInstance was called with an element type that is not supported. This is a bug in React."
          );
      }
      for (o = a.attributes; o.length; )
        a.removeAttributeNode(o[0]);
      Pt(a, e, t), a[el] = c, a[Da] = t;
    }
    function Sc(e) {
      for (var t = e.attributes; t.length; )
        e.removeAttributeNode(t[0]);
      M(e);
    }
    function Oh(e) {
      return typeof e.getRootNode == "function" ? e.getRootNode() : e.nodeType === 9 ? e : e.ownerDocument;
    }
    function a0(e, t, a) {
      var c = Em;
      if (c && typeof t == "string" && t) {
        var o = Ut(t);
        o = 'link[rel="' + e + '"][href="' + o + '"]', typeof a == "string" && (o += '[crossorigin="' + a + '"]'), O2.has(o) || (O2.add(o), e = { rel: e, crossOrigin: a, href: t }, c.querySelector(o) === null && (t = c.createElement("link"), Pt(t, "link", e), me(t), c.head.appendChild(t)));
      }
    }
    function n0(e, t, a, c) {
      var o = (o = nn.current) ? Oh(o) : null;
      if (!o)
        throw Error(
          '"resourceRoot" was expected to exist. This is a bug in React.'
        );
      switch (e) {
        case "meta":
        case "title":
          return null;
        case "style":
          return typeof a.precedence == "string" && typeof a.href == "string" ? (a = co(a.href), t = Ce(o).hoistableStyles, c = t.get(a), c || (c = {
            type: "style",
            instance: null,
            count: 0,
            state: null
          }, t.set(a, c)), c) : { type: "void", instance: null, count: 0, state: null };
        case "link":
          if (a.rel === "stylesheet" && typeof a.href == "string" && typeof a.precedence == "string") {
            e = co(a.href);
            var f = Ce(o).hoistableStyles, d = f.get(e);
            if (!d && (o = o.ownerDocument || o, d = {
              type: "stylesheet",
              instance: null,
              count: 0,
              state: { loading: Ir, preload: null }
            }, f.set(e, d), (f = o.querySelector(
              gr(e)
            )) && !f._p && (d.instance = f, d.state.loading = pp | Fu), !Iu.has(e))) {
              var h = {
                rel: "preload",
                as: "style",
                href: a.href,
                crossOrigin: a.crossOrigin,
                integrity: a.integrity,
                media: a.media,
                hrefLang: a.hrefLang,
                referrerPolicy: a.referrerPolicy
              };
              Iu.set(e, h), f || xg(
                o,
                e,
                h,
                d.state
              );
            }
            if (t && c === null)
              throw a = `

  - ` + pr(t) + `
  + ` + pr(a), Error(
                "Expected <link> not to update to be updated to a stylesheet with precedence. Check the `rel`, `href`, and `precedence` props of this component. Alternatively, check whether two different <link> components render in the same slot or share the same key." + a
              );
            return d;
          }
          if (t && c !== null)
            throw a = `

  - ` + pr(t) + `
  + ` + pr(a), Error(
              "Expected stylesheet with precedence to not be updated to a different kind of <link>. Check the `rel`, `href`, and `precedence` props of this component. Alternatively, check whether two different <link> components render in the same slot or share the same key." + a
            );
          return null;
        case "script":
          return t = a.async, a = a.src, typeof a == "string" && t && typeof t != "function" && typeof t != "symbol" ? (a = io(a), t = Ce(o).hoistableScripts, c = t.get(a), c || (c = {
            type: "script",
            instance: null,
            count: 0,
            state: null
          }, t.set(a, c)), c) : { type: "void", instance: null, count: 0, state: null };
        default:
          throw Error(
            'getResource encountered a type it did not expect: "' + e + '". this is a bug in React.'
          );
      }
    }
    function pr(e) {
      var t = 0, a = "<link";
      return typeof e.rel == "string" ? (t++, a += ' rel="' + e.rel + '"') : un.call(e, "rel") && (t++, a += ' rel="' + (e.rel === null ? "null" : "invalid type " + typeof e.rel) + '"'), typeof e.href == "string" ? (t++, a += ' href="' + e.href + '"') : un.call(e, "href") && (t++, a += ' href="' + (e.href === null ? "null" : "invalid type " + typeof e.href) + '"'), typeof e.precedence == "string" ? (t++, a += ' precedence="' + e.precedence + '"') : un.call(e, "precedence") && (t++, a += " precedence={" + (e.precedence === null ? "null" : "invalid type " + typeof e.precedence) + "}"), Object.getOwnPropertyNames(e).length > t && (a += " ..."), a + " />";
    }
    function co(e) {
      return 'href="' + Ut(e) + '"';
    }
    function gr(e) {
      return 'link[rel="stylesheet"][' + e + "]";
    }
    function zh(e) {
      return Ie({}, e, {
        "data-precedence": e.precedence,
        precedence: null
      });
    }
    function xg(e, t, a, c) {
      e.querySelector(
        'link[rel="preload"][as="style"][' + t + "]"
      ) ? c.loading = pp : (t = e.createElement("link"), c.preload = t, t.addEventListener("load", function() {
        return c.loading |= pp;
      }), t.addEventListener("error", function() {
        return c.loading |= T2;
      }), Pt(t, "link", a), me(t), e.head.appendChild(t));
    }
    function io(e) {
      return '[src="' + Ut(e) + '"]';
    }
    function vr(e) {
      return "script[async]" + e;
    }
    function Dh(e, t, a) {
      if (t.count++, t.instance === null)
        switch (t.type) {
          case "style":
            var c = e.querySelector(
              'style[data-href~="' + Ut(a.href) + '"]'
            );
            if (c)
              return t.instance = c, me(c), c;
            var o = Ie({}, a, {
              "data-href": a.href,
              "data-precedence": a.precedence,
              href: null,
              precedence: null
            });
            return c = (e.ownerDocument || e).createElement("style"), me(c), Pt(c, "style", o), Rf(c, a.precedence, e), t.instance = c;
          case "stylesheet":
            o = co(a.href);
            var f = e.querySelector(
              gr(o)
            );
            if (f)
              return t.state.loading |= Fu, t.instance = f, me(f), f;
            c = zh(a), (o = Iu.get(o)) && u0(c, o), f = (e.ownerDocument || e).createElement("link"), me(f);
            var d = f;
            return d._p = new Promise(function(h, y) {
              d.onload = h, d.onerror = y;
            }), Pt(f, "link", c), t.state.loading |= Fu, Rf(f, a.precedence, e), t.instance = f;
          case "script":
            return f = io(a.src), (o = e.querySelector(
              vr(f)
            )) ? (t.instance = o, me(o), o) : (c = a, (o = Iu.get(f)) && (c = Ie({}, a), c0(c, o)), e = e.ownerDocument || e, o = e.createElement("script"), me(o), Pt(o, "link", c), e.head.appendChild(o), t.instance = o);
          case "void":
            return null;
          default:
            throw Error(
              'acquireResource encountered a resource type it did not expect: "' + t.type + '". this is a bug in React.'
            );
        }
      else
        t.type === "stylesheet" && (t.state.loading & Fu) === Ir && (c = t.instance, t.state.loading |= Fu, Rf(c, a.precedence, e));
      return t.instance;
    }
    function Rf(e, t, a) {
      for (var c = a.querySelectorAll(
        'link[rel="stylesheet"][data-precedence],style[data-precedence]'
      ), o = c.length ? c[c.length - 1] : null, f = o, d = 0; d < c.length; d++) {
        var h = c[d];
        if (h.dataset.precedence === t) f = h;
        else if (f !== o) break;
      }
      f ? f.parentNode.insertBefore(e, f.nextSibling) : (t = a.nodeType === 9 ? a.head : a, t.insertBefore(e, t.firstChild));
    }
    function u0(e, t) {
      e.crossOrigin == null && (e.crossOrigin = t.crossOrigin), e.referrerPolicy == null && (e.referrerPolicy = t.referrerPolicy), e.title == null && (e.title = t.title);
    }
    function c0(e, t) {
      e.crossOrigin == null && (e.crossOrigin = t.crossOrigin), e.referrerPolicy == null && (e.referrerPolicy = t.referrerPolicy), e.integrity == null && (e.integrity = t.integrity);
    }
    function _f(e, t, a) {
      if (Gv === null) {
        var c = /* @__PURE__ */ new Map(), o = Gv = /* @__PURE__ */ new Map();
        o.set(a, c);
      } else
        o = Gv, c = o.get(a), c || (c = /* @__PURE__ */ new Map(), o.set(a, c));
      if (c.has(e)) return c;
      for (c.set(e, null), a = a.getElementsByTagName(e), o = 0; o < a.length; o++) {
        var f = a[o];
        if (!(f[Gf] || f[el] || e === "link" && f.getAttribute("rel") === "stylesheet") && f.namespaceURI !== We) {
          var d = f.getAttribute(t) || "";
          d = e + d;
          var h = c.get(d);
          h ? h.push(f) : c.set(d, [f]);
        }
      }
      return c;
    }
    function Ng(e, t, a) {
      e = e.ownerDocument || e, e.head.insertBefore(
        a,
        t === "title" ? e.querySelector("head > title") : null
      );
    }
    function Hg(e, t, a) {
      var c = !a.ancestorInfo.containerTagInScope;
      if (a.context === bm || t.itemProp != null)
        return !c || t.itemProp == null || e !== "meta" && e !== "title" && e !== "style" && e !== "link" && e !== "script" || console.error(
          "Cannot render a <%s> outside the main document if it has an `itemProp` prop. `itemProp` suggests the tag belongs to an `itemScope` which can appear anywhere in the DOM. If you were intending for React to hoist this <%s> remove the `itemProp` prop. Otherwise, try moving this tag into the <head> or <body> of the Document.",
          e,
          e
        ), !1;
      switch (e) {
        case "meta":
        case "title":
          return !0;
        case "style":
          if (typeof t.precedence != "string" || typeof t.href != "string" || t.href === "") {
            c && console.error(
              'Cannot render a <style> outside the main document without knowing its precedence and a unique href key. React can hoist and deduplicate <style> tags if you provide a `precedence` prop along with an `href` prop that does not conflict with the `href` values used in any other hoisted <style> or <link rel="stylesheet" ...> tags.  Note that hoisting <style> tags is considered an advanced feature that most will not use directly. Consider moving the <style> tag to the <head> or consider adding a `precedence="default"` and `href="some unique resource identifier"`.'
            );
            break;
          }
          return !0;
        case "link":
          if (typeof t.rel != "string" || typeof t.href != "string" || t.href === "" || t.onLoad || t.onError) {
            if (t.rel === "stylesheet" && typeof t.precedence == "string") {
              e = t.href;
              var o = t.onError, f = t.disabled;
              a = [], t.onLoad && a.push("`onLoad`"), o && a.push("`onError`"), f != null && a.push("`disabled`"), o = dg(a, "and"), o += a.length === 1 ? " prop" : " props", f = a.length === 1 ? "an " + o : "the " + o, a.length && console.error(
                'React encountered a <link rel="stylesheet" href="%s" ... /> with a `precedence` prop that also included %s. The presence of loading and error handlers indicates an intent to manage the stylesheet loading state from your from your Component code and React will not hoist or deduplicate this stylesheet. If your intent was to have React hoist and deduplciate this stylesheet using the `precedence` prop remove the %s, otherwise remove the `precedence` prop.',
                e,
                f,
                o
              );
            }
            c && (typeof t.rel != "string" || typeof t.href != "string" || t.href === "" ? console.error(
              "Cannot render a <link> outside the main document without a `rel` and `href` prop. Try adding a `rel` and/or `href` prop to this <link> or moving the link into the <head> tag"
            ) : (t.onError || t.onLoad) && console.error(
              "Cannot render a <link> with onLoad or onError listeners outside the main document. Try removing onLoad={...} and onError={...} or moving it into the root <head> tag or somewhere in the <body>."
            ));
            break;
          }
          return t.rel === "stylesheet" ? (e = t.precedence, t = t.disabled, typeof e != "string" && c && console.error(
            'Cannot render a <link rel="stylesheet" /> outside the main document without knowing its precedence. Consider adding precedence="default" or moving it into the root <head> tag.'
          ), typeof e == "string" && t == null) : !0;
        case "script":
          if (e = t.async && typeof t.async != "function" && typeof t.async != "symbol", !e || t.onLoad || t.onError || !t.src || typeof t.src != "string") {
            c && (e ? t.onLoad || t.onError ? console.error(
              "Cannot render a <script> with onLoad or onError listeners outside the main document. Try removing onLoad={...} and onError={...} or moving it into the root <head> tag or somewhere in the <body>."
            ) : console.error(
              "Cannot render a <script> outside the main document without `async={true}` and a non-empty `src` prop. Ensure there is a valid `src` and either make the script async or move it into the root <head> tag or somewhere in the <body>."
            ) : console.error(
              'Cannot render a sync or defer <script> outside the main document without knowing its order. Try adding async="" or moving it into the root <head> tag.'
            ));
            break;
          }
          return !0;
        case "noscript":
        case "template":
          c && console.error(
            "Cannot render <%s> outside the main document. Try moving it into the root <head> tag.",
            e
          );
      }
      return !1;
    }
    function ct(e) {
      return !(e.type === "stylesheet" && (e.state.loading & A2) === Ir);
    }
    function i0(e, t, a, c) {
      if (a.type === "stylesheet" && (typeof c.media != "string" || matchMedia(c.media).matches !== !1) && (a.state.loading & Fu) === Ir) {
        if (a.instance === null) {
          var o = co(c.href), f = t.querySelector(
            gr(o)
          );
          if (f) {
            t = f._p, t !== null && typeof t == "object" && typeof t.then == "function" && (e.count++, e = Mf.bind(e), t.then(e, e)), a.state.loading |= Fu, a.instance = f, me(f);
            return;
          }
          f = t.ownerDocument || t, c = zh(c), (o = Iu.get(o)) && u0(c, o), f = f.createElement("link"), me(f);
          var d = f;
          d._p = new Promise(function(h, y) {
            d.onload = h, d.onerror = y;
          }), Pt(f, "link", c), a.instance = f;
        }
        e.stylesheets === null && (e.stylesheets = /* @__PURE__ */ new Map()), e.stylesheets.set(a, t), (t = a.state.preload) && (a.state.loading & A2) === Ir && (e.count++, a = Mf.bind(e), t.addEventListener("load", a), t.addEventListener("error", a));
      }
    }
    function Rh(e, t) {
      return e.stylesheets && e.count === 0 && Sr(e, e.stylesheets), 0 < e.count || 0 < e.imgCount ? function(a) {
        var c = setTimeout(function() {
          if (e.stylesheets && Sr(e, e.stylesheets), e.unsuspend) {
            var f = e.unsuspend;
            e.unsuspend = null, f();
          }
        }, bT + t);
        0 < e.imgBytes && ES === 0 && (ES = 125 * hg() * TT);
        var o = setTimeout(
          function() {
            if (e.waitingForImages = !1, e.count === 0 && (e.stylesheets && Sr(e, e.stylesheets), e.unsuspend)) {
              var f = e.unsuspend;
              e.unsuspend = null, f();
            }
          },
          (e.imgBytes > ES ? 50 : ET) + t
        );
        return e.unsuspend = a, function() {
          e.unsuspend = null, clearTimeout(c), clearTimeout(o);
        };
      } : null;
    }
    function Mf() {
      if (this.count--, this.count === 0 && (this.imgCount === 0 || !this.waitingForImages)) {
        if (this.stylesheets)
          Sr(this, this.stylesheets);
        else if (this.unsuspend) {
          var e = this.unsuspend;
          this.unsuspend = null, e();
        }
      }
    }
    function Sr(e, t) {
      e.stylesheets = null, e.unsuspend !== null && (e.count++, Xv = /* @__PURE__ */ new Map(), t.forEach(o0, e), Xv = null, Mf.call(e));
    }
    function o0(e, t) {
      if (!(t.state.loading & Fu)) {
        var a = Xv.get(e);
        if (a) var c = a.get(TS);
        else {
          a = /* @__PURE__ */ new Map(), Xv.set(e, a);
          for (var o = e.querySelectorAll(
            "link[data-precedence],style[data-precedence]"
          ), f = 0; f < o.length; f++) {
            var d = o[f];
            (d.nodeName === "LINK" || d.getAttribute("media") !== "not all") && (a.set(d.dataset.precedence, d), c = d);
          }
          c && a.set(TS, c);
        }
        o = t.instance, d = o.getAttribute("data-precedence"), f = a.get(d) || c, f === c && a.set(TS, o), a.set(d, o), this.count++, c = Mf.bind(this), o.addEventListener("load", c), o.addEventListener("error", c), f ? f.parentNode.insertBefore(o, f.nextSibling) : (e = e.nodeType === 9 ? e.head : e, e.insertBefore(o, e.firstChild)), t.state.loading |= Fu;
      }
    }
    function br(e, t, a, c, o, f, d, h, y) {
      for (this.tag = 1, this.containerInfo = e, this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = Fr, this.callbackNode = this.next = this.pendingContext = this.context = this.cancelPendingCommit = null, this.callbackPriority = 0, this.expirationTimes = xo(-1), this.entangledLanes = this.shellSuspendCounter = this.errorRecoveryDisabledLanes = this.expiredLanes = this.warmLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = xo(0), this.hiddenUpdates = xo(null), this.identifierPrefix = c, this.onUncaughtError = o, this.onCaughtError = f, this.onRecoverableError = d, this.pooledCache = null, this.pooledCacheLanes = 0, this.formState = y, this.incompleteTransitions = /* @__PURE__ */ new Map(), this.passiveEffectDuration = this.effectDuration = -0, this.memoizedUpdaters = /* @__PURE__ */ new Set(), e = this.pendingUpdatersLaneMap = [], t = 0; 31 > t; t++) e.push(/* @__PURE__ */ new Set());
      this._debugRootType = a ? "hydrateRoot()" : "createRoot()";
    }
    function Er(e, t, a, c, o, f, d, h, y, p, z, _) {
      return e = new br(
        e,
        t,
        a,
        d,
        y,
        p,
        z,
        _,
        h
      ), t = JE, f === !0 && (t |= Ba | Tc), t |= Pe, f = x(3, null, null, t), e.current = f, f.stateNode = e, t = Dd(), Bi(t), e.pooledCache = t, Bi(t), f.memoizedState = {
        element: c,
        isDehydrated: a,
        cache: t
      }, ot(f), e;
    }
    function jg(e) {
      return e ? (e = Jf, e) : Jf;
    }
    function _h(e, t, a, c, o, f) {
      if (Ml && typeof Ml.onScheduleFiberRoot == "function")
        try {
          Ml.onScheduleFiberRoot(ho, c, a);
        } catch (d) {
          qu || (qu = !0, console.error(
            "React instrumentation encountered an error: %o",
            d
          ));
        }
      o = jg(o), c.context === null ? c.context = o : c.pendingContext = o, Yu && ja !== null && !_2 && (_2 = !0, console.error(
        `Render methods should be a pure function of props and state; triggering nested component updates from render is not allowed. If necessary, trigger nested updates in componentDidUpdate.

Check the render method of %s.`,
        se(ja) || "Unknown"
      )), c = Dl(t), c.payload = { element: a }, f = f === void 0 ? null : f, f !== null && (typeof f != "function" && console.error(
        "Expected the last optional `callback` argument to be a function. Instead received: %s.",
        f
      ), c.callback = f), a = Su(e, c, t), a !== null && (pu(t, "root.render()", null), je(a, e, t), Tn(a, e, t));
    }
    function Bg(e, t) {
      if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
        var a = e.retryLane;
        e.retryLane = a !== 0 && a < t ? a : t;
      }
    }
    function f0(e, t) {
      Bg(e, t), (e = e.alternate) && Bg(e, t);
    }
    function s0(e) {
      if (e.tag === 13 || e.tag === 31) {
        var t = aa(e, 67108864);
        t !== null && je(t, e, 67108864), f0(e, 67108864);
      }
    }
    function r0(e) {
      if (e.tag === 13 || e.tag === 31) {
        var t = ua(e);
        t = hn(t);
        var a = aa(e, t);
        a !== null && je(a, e, t), f0(e, t);
      }
    }
    function Ht() {
      return ja;
    }
    function d0(e, t, a, c) {
      var o = G.T;
      G.T = null;
      var f = At.p;
      try {
        At.p = Cl, h0(e, t, a, c);
      } finally {
        At.p = f, G.T = o;
      }
    }
    function Wl(e, t, a, c) {
      var o = G.T;
      G.T = null;
      var f = At.p;
      try {
        At.p = Il, h0(e, t, a, c);
      } finally {
        At.p = f, G.T = o;
      }
    }
    function h0(e, t, a, c) {
      if (Qv) {
        var o = Mh(c);
        if (o === null)
          kn(
            e,
            t,
            c,
            Vv,
            a
          ), Uh(e, c);
        else if (Yg(
          o,
          e,
          t,
          a,
          c
        ))
          c.stopPropagation();
        else if (Uh(e, c), t & 4 && -1 < OT.indexOf(e)) {
          for (; o !== null; ) {
            var f = ae(o);
            if (f !== null)
              switch (f.tag) {
                case 3:
                  if (f = f.stateNode, f.current.memoizedState.isDehydrated) {
                    var d = ou(f.pendingLanes);
                    if (d !== 0) {
                      var h = f;
                      for (h.pendingLanes |= 2, h.entangledLanes |= 2; d; ) {
                        var y = 1 << 31 - Fl(d);
                        h.entanglements[1] |= y, d &= ~y;
                      }
                      Ua(f), (pt & (ea | uu)) === sa && (Dv = Xl() + l2, xu(0));
                    }
                  }
                  break;
                case 31:
                case 13:
                  h = aa(f, 2), h !== null && je(h, f, 2), ln(), f0(f, 2);
              }
            if (f = Mh(c), f === null && kn(
              e,
              t,
              c,
              Vv,
              a
            ), f === o) break;
            o = f;
          }
          o !== null && c.stopPropagation();
        } else
          kn(
            e,
            t,
            c,
            null,
            a
          );
      }
    }
    function Mh(e) {
      return e = Nn(e), m0(e);
    }
    function m0(e) {
      if (Vv = null, e = P(e), e !== null) {
        var t = Ze(e);
        if (t === null) e = null;
        else {
          var a = t.tag;
          if (a === 13) {
            if (e = qt(t), e !== null) return e;
            e = null;
          } else if (a === 31) {
            if (e = Ot(t), e !== null) return e;
            e = null;
          } else if (a === 3) {
            if (t.stateNode.current.memoizedState.isDehydrated)
              return t.tag === 3 ? t.stateNode.containerInfo : null;
            e = null;
          } else t !== e && (e = null);
        }
      }
      return Vv = e, null;
    }
    function Ch(e) {
      switch (e) {
        case "beforetoggle":
        case "cancel":
        case "click":
        case "close":
        case "contextmenu":
        case "copy":
        case "cut":
        case "auxclick":
        case "dblclick":
        case "dragend":
        case "dragstart":
        case "drop":
        case "focusin":
        case "focusout":
        case "input":
        case "invalid":
        case "keydown":
        case "keypress":
        case "keyup":
        case "mousedown":
        case "mouseup":
        case "paste":
        case "pause":
        case "play":
        case "pointercancel":
        case "pointerdown":
        case "pointerup":
        case "ratechange":
        case "reset":
        case "resize":
        case "seeked":
        case "submit":
        case "toggle":
        case "touchcancel":
        case "touchend":
        case "touchstart":
        case "volumechange":
        case "change":
        case "selectionchange":
        case "textInput":
        case "compositionstart":
        case "compositionend":
        case "compositionupdate":
        case "beforeblur":
        case "afterblur":
        case "beforeinput":
        case "blur":
        case "fullscreenchange":
        case "focus":
        case "hashchange":
        case "popstate":
        case "select":
        case "selectstart":
          return Cl;
        case "drag":
        case "dragenter":
        case "dragexit":
        case "dragleave":
        case "dragover":
        case "mousemove":
        case "mouseout":
        case "mouseover":
        case "pointermove":
        case "pointerout":
        case "pointerover":
        case "scroll":
        case "touchmove":
        case "wheel":
        case "mouseenter":
        case "mouseleave":
        case "pointerenter":
        case "pointerleave":
          return Il;
        case "message":
          switch (Rr()) {
            case O0:
              return Cl;
            case Gh:
              return Il;
            case ro:
            case Qg:
              return ia;
            case Xh:
              return hi;
            default:
              return ia;
          }
        default:
          return ia;
      }
    }
    function Uh(e, t) {
      switch (e) {
        case "focusin":
        case "focusout":
          os = null;
          break;
        case "dragenter":
        case "dragleave":
          fs = null;
          break;
        case "mouseover":
        case "mouseout":
          ss = null;
          break;
        case "pointerover":
        case "pointerout":
          vp.delete(t.pointerId);
          break;
        case "gotpointercapture":
        case "lostpointercapture":
          Sp.delete(t.pointerId);
      }
    }
    function fi(e, t, a, c, o, f) {
      return e === null || e.nativeEvent !== f ? (e = {
        blockedOn: t,
        domEventName: a,
        eventSystemFlags: c,
        nativeEvent: f,
        targetContainers: [o]
      }, t !== null && (t = ae(t), t !== null && s0(t)), e) : (e.eventSystemFlags |= c, t = e.targetContainers, o !== null && t.indexOf(o) === -1 && t.push(o), e);
    }
    function Yg(e, t, a, c, o) {
      switch (t) {
        case "focusin":
          return os = fi(
            os,
            e,
            t,
            a,
            c,
            o
          ), !0;
        case "dragenter":
          return fs = fi(
            fs,
            e,
            t,
            a,
            c,
            o
          ), !0;
        case "mouseover":
          return ss = fi(
            ss,
            e,
            t,
            a,
            c,
            o
          ), !0;
        case "pointerover":
          var f = o.pointerId;
          return vp.set(
            f,
            fi(
              vp.get(f) || null,
              e,
              t,
              a,
              c,
              o
            )
          ), !0;
        case "gotpointercapture":
          return f = o.pointerId, Sp.set(
            f,
            fi(
              Sp.get(f) || null,
              e,
              t,
              a,
              c,
              o
            )
          ), !0;
      }
      return !1;
    }
    function y0(e) {
      var t = P(e.target);
      if (t !== null) {
        var a = Ze(t);
        if (a !== null) {
          if (t = a.tag, t === 13) {
            if (t = qt(a), t !== null) {
              e.blockedOn = t, g(e.priority, function() {
                r0(a);
              });
              return;
            }
          } else if (t === 31) {
            if (t = Ot(a), t !== null) {
              e.blockedOn = t, g(e.priority, function() {
                r0(a);
              });
              return;
            }
          } else if (t === 3 && a.stateNode.current.memoizedState.isDehydrated) {
            e.blockedOn = a.tag === 3 ? a.stateNode.containerInfo : null;
            return;
          }
        }
      }
      e.blockedOn = null;
    }
    function Cf(e) {
      if (e.blockedOn !== null) return !1;
      for (var t = e.targetContainers; 0 < t.length; ) {
        var a = Mh(e.nativeEvent);
        if (a === null) {
          a = e.nativeEvent;
          var c = new a.constructor(
            a.type,
            a
          ), o = c;
          M0 !== null && console.error(
            "Expected currently replaying event to be null. This error is likely caused by a bug in React. Please file an issue."
          ), M0 = o, a.target.dispatchEvent(c), M0 === null && console.error(
            "Expected currently replaying event to not be null. This error is likely caused by a bug in React. Please file an issue."
          ), M0 = null;
        } else
          return t = ae(a), t !== null && s0(t), e.blockedOn = a, !1;
        t.shift();
      }
      return !0;
    }
    function xh(e, t, a) {
      Cf(e) && a.delete(t);
    }
    function f1() {
      AS = !1, os !== null && Cf(os) && (os = null), fs !== null && Cf(fs) && (fs = null), ss !== null && Cf(ss) && (ss = null), vp.forEach(xh), Sp.forEach(xh);
    }
    function Tr(e, t) {
      e.blockedOn === t && (e.blockedOn = null, AS || (AS = !0, vl.unstable_scheduleCallback(
        vl.unstable_NormalPriority,
        f1
      )));
    }
    function qg(e) {
      Zv !== e && (Zv = e, vl.unstable_scheduleCallback(
        vl.unstable_NormalPriority,
        function() {
          Zv === e && (Zv = null);
          for (var t = 0; t < e.length; t += 3) {
            var a = e[t], c = e[t + 1], o = e[t + 2];
            if (typeof c != "function") {
              if (m0(c || a) === null)
                continue;
              break;
            }
            var f = ae(a);
            f !== null && (e.splice(t, 3), t -= 3, a = {
              pending: !0,
              data: o,
              method: a.method,
              action: c
            }, Object.freeze(a), rc(
              f,
              a,
              c,
              o
            ));
          }
        }
      ));
    }
    function oo(e) {
      function t(y) {
        return Tr(y, e);
      }
      os !== null && Tr(os, e), fs !== null && Tr(fs, e), ss !== null && Tr(ss, e), vp.forEach(t), Sp.forEach(t);
      for (var a = 0; a < rs.length; a++) {
        var c = rs[a];
        c.blockedOn === e && (c.blockedOn = null);
      }
      for (; 0 < rs.length && (a = rs[0], a.blockedOn === null); )
        y0(a), a.blockedOn === null && rs.shift();
      if (a = (e.ownerDocument || e).$$reactFormReplay, a != null)
        for (c = 0; c < a.length; c += 3) {
          var o = a[c], f = a[c + 1], d = o[Da] || null;
          if (typeof f == "function")
            d || qg(a);
          else if (d) {
            var h = null;
            if (f && f.hasAttribute("formAction")) {
              if (o = f, d = f[Da] || null)
                h = d.formAction;
              else if (m0(o) !== null) continue;
            } else h = d.action;
            typeof h == "function" ? a[c + 1] = h : (a.splice(c, 3), c -= 3), qg(a);
          }
        }
    }
    function wg() {
      function e(f) {
        f.canIntercept && f.info === "react-transition" && f.intercept({
          handler: function() {
            return new Promise(function(d) {
              return o = d;
            });
          },
          focusReset: "manual",
          scroll: "manual"
        });
      }
      function t() {
        o !== null && (o(), o = null), c || setTimeout(a, 20);
      }
      function a() {
        if (!c && !navigation.transition) {
          var f = navigation.currentEntry;
          f && f.url != null && navigation.navigate(f.url, {
            state: f.getState(),
            info: "react-transition",
            history: "replace"
          });
        }
      }
      if (typeof navigation == "object") {
        var c = !1, o = null;
        return navigation.addEventListener("navigate", e), navigation.addEventListener("navigatesuccess", t), navigation.addEventListener("navigateerror", t), setTimeout(a, 100), function() {
          c = !0, navigation.removeEventListener("navigate", e), navigation.removeEventListener(
            "navigatesuccess",
            t
          ), navigation.removeEventListener(
            "navigateerror",
            t
          ), o !== null && (o(), o = null);
        };
      }
    }
    function p0(e) {
      this._internalRoot = e;
    }
    function In(e) {
      this._internalRoot = e;
    }
    function g0(e) {
      e[Ec] && (e._reactRootContainer ? console.error(
        "You are calling ReactDOMClient.createRoot() on a container that was previously passed to ReactDOM.render(). This is not supported."
      ) : console.error(
        "You are calling ReactDOMClient.createRoot() on a container that has already been passed to createRoot() before. Instead, call root.render() on the existing root instead if you want to update it."
      ));
    }
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error());
    var vl = lE(), Ar = Om(), s1 = aE(), Ie = Object.assign, Gg = /* @__PURE__ */ Symbol.for("react.element"), Dn = /* @__PURE__ */ Symbol.for("react.transitional.element"), si = /* @__PURE__ */ Symbol.for("react.portal"), Uf = /* @__PURE__ */ Symbol.for("react.fragment"), za = /* @__PURE__ */ Symbol.for("react.strict_mode"), Or = /* @__PURE__ */ Symbol.for("react.profiler"), Nh = /* @__PURE__ */ Symbol.for("react.consumer"), Pn = /* @__PURE__ */ Symbol.for("react.context"), xf = /* @__PURE__ */ Symbol.for("react.forward_ref"), fo = /* @__PURE__ */ Symbol.for("react.suspense"), Ha = /* @__PURE__ */ Symbol.for("react.suspense_list"), zr = /* @__PURE__ */ Symbol.for("react.memo"), ca = /* @__PURE__ */ Symbol.for("react.lazy"), eu = /* @__PURE__ */ Symbol.for("react.activity"), r1 = /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel"), Xg = Symbol.iterator, Nf = /* @__PURE__ */ Symbol.for("react.client.reference"), Al = Array.isArray, G = Ar.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, At = s1.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, d1 = Object.freeze({
      pending: !1,
      data: null,
      method: null,
      action: null
    }), v0 = [], S0 = [], bc = -1, ri = Yt(null), Hf = Yt(null), nn = Yt(null), di = Yt(null), jf = 0, Lg, so, Bf, b0, Dr, Hh, jh;
    De.__reactDisabledLog = !0;
    var Yf, E0, Bh = !1, T0 = new (typeof WeakMap == "function" ? WeakMap : Map)(), ja = null, Yu = !1, un = Object.prototype.hasOwnProperty, A0 = vl.unstable_scheduleCallback, Yh = vl.unstable_cancelCallback, qh = vl.unstable_shouldYield, wh = vl.unstable_requestPaint, Xl = vl.unstable_now, Rr = vl.unstable_getCurrentPriorityLevel, O0 = vl.unstable_ImmediatePriority, Gh = vl.unstable_UserBlockingPriority, ro = vl.unstable_NormalPriority, Qg = vl.unstable_LowPriority, Xh = vl.unstable_IdlePriority, z0 = vl.log, Vg = vl.unstable_setDisableYieldValue, ho = null, Ml = null, qu = !1, wu = typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u", Fl = Math.clz32 ? Math.clz32 : Cc, D0 = Math.log, Lh = Math.LN2, qf = 256, _r = 262144, wf = 4194304, Cl = 2, Il = 8, ia = 32, hi = 268435456, Rn = Math.random().toString(36).slice(2), el = "__reactFiber$" + Rn, Da = "__reactProps$" + Rn, Ec = "__reactContainer$" + Rn, mo = "__reactEvents$" + Rn, h1 = "__reactListeners$" + Rn, Zg = "__reactHandles$" + Rn, Mr = "__reactResources$" + Rn, Gf = "__reactMarker$" + Rn, Jg = /* @__PURE__ */ new Set(), Gu = {}, Xf = {}, Kg = {
      button: !0,
      checkbox: !0,
      image: !0,
      hidden: !0,
      radio: !0,
      reset: !0,
      submit: !0
    }, Lf = RegExp(
      "^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
    ), R0 = {}, Qh = {}, Vh = /[\n"\\]/g, _0 = !1, $g = !1, Cr = !1, l = !1, n = !1, u = !1, i = ["value", "defaultValue"], s = !1, r = /["'&<>\n\t]|^\s|\s$/, m = "address applet area article aside base basefont bgsound blockquote body br button caption center col colgroup dd details dir div dl dt embed fieldset figcaption figure footer form frame frameset h1 h2 h3 h4 h5 h6 head header hgroup hr html iframe img input isindex li link listing main marquee menu menuitem meta nav noembed noframes noscript object ol p param plaintext pre script section select source style summary table tbody td template textarea tfoot th thead title tr track ul wbr xmp".split(
      " "
    ), v = "applet caption html table td th marquee object template foreignObject desc title".split(
      " "
    ), A = v.concat(["button"]), j = "dd dt li option optgroup p rp rt".split(" "), V = {
      current: null,
      formTag: null,
      aTagInScope: null,
      buttonTagInScope: null,
      nobrTagInScope: null,
      pTagInButtonScope: null,
      listItemTagAutoclosing: null,
      dlItemTagAutoclosing: null,
      containerTagInScope: null,
      implicitRootScope: !1
    }, $ = {}, B = {
      animation: "animationDelay animationDirection animationDuration animationFillMode animationIterationCount animationName animationPlayState animationTimingFunction".split(
        " "
      ),
      background: "backgroundAttachment backgroundClip backgroundColor backgroundImage backgroundOrigin backgroundPositionX backgroundPositionY backgroundRepeat backgroundSize".split(
        " "
      ),
      backgroundPosition: ["backgroundPositionX", "backgroundPositionY"],
      border: "borderBottomColor borderBottomStyle borderBottomWidth borderImageOutset borderImageRepeat borderImageSlice borderImageSource borderImageWidth borderLeftColor borderLeftStyle borderLeftWidth borderRightColor borderRightStyle borderRightWidth borderTopColor borderTopStyle borderTopWidth".split(
        " "
      ),
      borderBlockEnd: [
        "borderBlockEndColor",
        "borderBlockEndStyle",
        "borderBlockEndWidth"
      ],
      borderBlockStart: [
        "borderBlockStartColor",
        "borderBlockStartStyle",
        "borderBlockStartWidth"
      ],
      borderBottom: [
        "borderBottomColor",
        "borderBottomStyle",
        "borderBottomWidth"
      ],
      borderColor: [
        "borderBottomColor",
        "borderLeftColor",
        "borderRightColor",
        "borderTopColor"
      ],
      borderImage: [
        "borderImageOutset",
        "borderImageRepeat",
        "borderImageSlice",
        "borderImageSource",
        "borderImageWidth"
      ],
      borderInlineEnd: [
        "borderInlineEndColor",
        "borderInlineEndStyle",
        "borderInlineEndWidth"
      ],
      borderInlineStart: [
        "borderInlineStartColor",
        "borderInlineStartStyle",
        "borderInlineStartWidth"
      ],
      borderLeft: ["borderLeftColor", "borderLeftStyle", "borderLeftWidth"],
      borderRadius: [
        "borderBottomLeftRadius",
        "borderBottomRightRadius",
        "borderTopLeftRadius",
        "borderTopRightRadius"
      ],
      borderRight: [
        "borderRightColor",
        "borderRightStyle",
        "borderRightWidth"
      ],
      borderStyle: [
        "borderBottomStyle",
        "borderLeftStyle",
        "borderRightStyle",
        "borderTopStyle"
      ],
      borderTop: ["borderTopColor", "borderTopStyle", "borderTopWidth"],
      borderWidth: [
        "borderBottomWidth",
        "borderLeftWidth",
        "borderRightWidth",
        "borderTopWidth"
      ],
      columnRule: ["columnRuleColor", "columnRuleStyle", "columnRuleWidth"],
      columns: ["columnCount", "columnWidth"],
      flex: ["flexBasis", "flexGrow", "flexShrink"],
      flexFlow: ["flexDirection", "flexWrap"],
      font: "fontFamily fontFeatureSettings fontKerning fontLanguageOverride fontSize fontSizeAdjust fontStretch fontStyle fontVariant fontVariantAlternates fontVariantCaps fontVariantEastAsian fontVariantLigatures fontVariantNumeric fontVariantPosition fontWeight lineHeight".split(
        " "
      ),
      fontVariant: "fontVariantAlternates fontVariantCaps fontVariantEastAsian fontVariantLigatures fontVariantNumeric fontVariantPosition".split(
        " "
      ),
      gap: ["columnGap", "rowGap"],
      grid: "gridAutoColumns gridAutoFlow gridAutoRows gridTemplateAreas gridTemplateColumns gridTemplateRows".split(
        " "
      ),
      gridArea: [
        "gridColumnEnd",
        "gridColumnStart",
        "gridRowEnd",
        "gridRowStart"
      ],
      gridColumn: ["gridColumnEnd", "gridColumnStart"],
      gridColumnGap: ["columnGap"],
      gridGap: ["columnGap", "rowGap"],
      gridRow: ["gridRowEnd", "gridRowStart"],
      gridRowGap: ["rowGap"],
      gridTemplate: [
        "gridTemplateAreas",
        "gridTemplateColumns",
        "gridTemplateRows"
      ],
      listStyle: ["listStyleImage", "listStylePosition", "listStyleType"],
      margin: ["marginBottom", "marginLeft", "marginRight", "marginTop"],
      marker: ["markerEnd", "markerMid", "markerStart"],
      mask: "maskClip maskComposite maskImage maskMode maskOrigin maskPositionX maskPositionY maskRepeat maskSize".split(
        " "
      ),
      maskPosition: ["maskPositionX", "maskPositionY"],
      outline: ["outlineColor", "outlineStyle", "outlineWidth"],
      overflow: ["overflowX", "overflowY"],
      padding: ["paddingBottom", "paddingLeft", "paddingRight", "paddingTop"],
      placeContent: ["alignContent", "justifyContent"],
      placeItems: ["alignItems", "justifyItems"],
      placeSelf: ["alignSelf", "justifySelf"],
      textDecoration: [
        "textDecorationColor",
        "textDecorationLine",
        "textDecorationStyle"
      ],
      textEmphasis: ["textEmphasisColor", "textEmphasisStyle"],
      transition: [
        "transitionDelay",
        "transitionDuration",
        "transitionProperty",
        "transitionTimingFunction"
      ],
      wordWrap: ["overflowWrap"]
    }, X = /([A-Z])/g, re = /^ms-/, _e = /^(?:webkit|moz|o)[A-Z]/, jt = /^-ms-/, C = /-(.)/g, D = /;\s*$/, N = {}, K = {}, Ee = !1, yt = !1, ye = new Set(
      "animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(
        " "
      )
    ), Ve = "http://www.w3.org/1998/Math/MathML", We = "http://www.w3.org/2000/svg", bt = /* @__PURE__ */ new Map([
      ["acceptCharset", "accept-charset"],
      ["htmlFor", "for"],
      ["httpEquiv", "http-equiv"],
      ["crossOrigin", "crossorigin"],
      ["accentHeight", "accent-height"],
      ["alignmentBaseline", "alignment-baseline"],
      ["arabicForm", "arabic-form"],
      ["baselineShift", "baseline-shift"],
      ["capHeight", "cap-height"],
      ["clipPath", "clip-path"],
      ["clipRule", "clip-rule"],
      ["colorInterpolation", "color-interpolation"],
      ["colorInterpolationFilters", "color-interpolation-filters"],
      ["colorProfile", "color-profile"],
      ["colorRendering", "color-rendering"],
      ["dominantBaseline", "dominant-baseline"],
      ["enableBackground", "enable-background"],
      ["fillOpacity", "fill-opacity"],
      ["fillRule", "fill-rule"],
      ["floodColor", "flood-color"],
      ["floodOpacity", "flood-opacity"],
      ["fontFamily", "font-family"],
      ["fontSize", "font-size"],
      ["fontSizeAdjust", "font-size-adjust"],
      ["fontStretch", "font-stretch"],
      ["fontStyle", "font-style"],
      ["fontVariant", "font-variant"],
      ["fontWeight", "font-weight"],
      ["glyphName", "glyph-name"],
      ["glyphOrientationHorizontal", "glyph-orientation-horizontal"],
      ["glyphOrientationVertical", "glyph-orientation-vertical"],
      ["horizAdvX", "horiz-adv-x"],
      ["horizOriginX", "horiz-origin-x"],
      ["imageRendering", "image-rendering"],
      ["letterSpacing", "letter-spacing"],
      ["lightingColor", "lighting-color"],
      ["markerEnd", "marker-end"],
      ["markerMid", "marker-mid"],
      ["markerStart", "marker-start"],
      ["overlinePosition", "overline-position"],
      ["overlineThickness", "overline-thickness"],
      ["paintOrder", "paint-order"],
      ["panose-1", "panose-1"],
      ["pointerEvents", "pointer-events"],
      ["renderingIntent", "rendering-intent"],
      ["shapeRendering", "shape-rendering"],
      ["stopColor", "stop-color"],
      ["stopOpacity", "stop-opacity"],
      ["strikethroughPosition", "strikethrough-position"],
      ["strikethroughThickness", "strikethrough-thickness"],
      ["strokeDasharray", "stroke-dasharray"],
      ["strokeDashoffset", "stroke-dashoffset"],
      ["strokeLinecap", "stroke-linecap"],
      ["strokeLinejoin", "stroke-linejoin"],
      ["strokeMiterlimit", "stroke-miterlimit"],
      ["strokeOpacity", "stroke-opacity"],
      ["strokeWidth", "stroke-width"],
      ["textAnchor", "text-anchor"],
      ["textDecoration", "text-decoration"],
      ["textRendering", "text-rendering"],
      ["transformOrigin", "transform-origin"],
      ["underlinePosition", "underline-position"],
      ["underlineThickness", "underline-thickness"],
      ["unicodeBidi", "unicode-bidi"],
      ["unicodeRange", "unicode-range"],
      ["unitsPerEm", "units-per-em"],
      ["vAlphabetic", "v-alphabetic"],
      ["vHanging", "v-hanging"],
      ["vIdeographic", "v-ideographic"],
      ["vMathematical", "v-mathematical"],
      ["vectorEffect", "vector-effect"],
      ["vertAdvY", "vert-adv-y"],
      ["vertOriginX", "vert-origin-x"],
      ["vertOriginY", "vert-origin-y"],
      ["wordSpacing", "word-spacing"],
      ["writingMode", "writing-mode"],
      ["xmlnsXlink", "xmlns:xlink"],
      ["xHeight", "x-height"]
    ]), tu = {
      accept: "accept",
      acceptcharset: "acceptCharset",
      "accept-charset": "acceptCharset",
      accesskey: "accessKey",
      action: "action",
      allowfullscreen: "allowFullScreen",
      alt: "alt",
      as: "as",
      async: "async",
      autocapitalize: "autoCapitalize",
      autocomplete: "autoComplete",
      autocorrect: "autoCorrect",
      autofocus: "autoFocus",
      autoplay: "autoPlay",
      autosave: "autoSave",
      capture: "capture",
      cellpadding: "cellPadding",
      cellspacing: "cellSpacing",
      challenge: "challenge",
      charset: "charSet",
      checked: "checked",
      children: "children",
      cite: "cite",
      class: "className",
      classid: "classID",
      classname: "className",
      cols: "cols",
      colspan: "colSpan",
      content: "content",
      contenteditable: "contentEditable",
      contextmenu: "contextMenu",
      controls: "controls",
      controlslist: "controlsList",
      coords: "coords",
      crossorigin: "crossOrigin",
      dangerouslysetinnerhtml: "dangerouslySetInnerHTML",
      data: "data",
      datetime: "dateTime",
      default: "default",
      defaultchecked: "defaultChecked",
      defaultvalue: "defaultValue",
      defer: "defer",
      dir: "dir",
      disabled: "disabled",
      disablepictureinpicture: "disablePictureInPicture",
      disableremoteplayback: "disableRemotePlayback",
      download: "download",
      draggable: "draggable",
      enctype: "encType",
      enterkeyhint: "enterKeyHint",
      fetchpriority: "fetchPriority",
      for: "htmlFor",
      form: "form",
      formmethod: "formMethod",
      formaction: "formAction",
      formenctype: "formEncType",
      formnovalidate: "formNoValidate",
      formtarget: "formTarget",
      frameborder: "frameBorder",
      headers: "headers",
      height: "height",
      hidden: "hidden",
      high: "high",
      href: "href",
      hreflang: "hrefLang",
      htmlfor: "htmlFor",
      httpequiv: "httpEquiv",
      "http-equiv": "httpEquiv",
      icon: "icon",
      id: "id",
      imagesizes: "imageSizes",
      imagesrcset: "imageSrcSet",
      inert: "inert",
      innerhtml: "innerHTML",
      inputmode: "inputMode",
      integrity: "integrity",
      is: "is",
      itemid: "itemID",
      itemprop: "itemProp",
      itemref: "itemRef",
      itemscope: "itemScope",
      itemtype: "itemType",
      keyparams: "keyParams",
      keytype: "keyType",
      kind: "kind",
      label: "label",
      lang: "lang",
      list: "list",
      loop: "loop",
      low: "low",
      manifest: "manifest",
      marginwidth: "marginWidth",
      marginheight: "marginHeight",
      max: "max",
      maxlength: "maxLength",
      media: "media",
      mediagroup: "mediaGroup",
      method: "method",
      min: "min",
      minlength: "minLength",
      multiple: "multiple",
      muted: "muted",
      name: "name",
      nomodule: "noModule",
      nonce: "nonce",
      novalidate: "noValidate",
      open: "open",
      optimum: "optimum",
      pattern: "pattern",
      placeholder: "placeholder",
      playsinline: "playsInline",
      poster: "poster",
      preload: "preload",
      profile: "profile",
      radiogroup: "radioGroup",
      readonly: "readOnly",
      referrerpolicy: "referrerPolicy",
      rel: "rel",
      required: "required",
      reversed: "reversed",
      role: "role",
      rows: "rows",
      rowspan: "rowSpan",
      sandbox: "sandbox",
      scope: "scope",
      scoped: "scoped",
      scrolling: "scrolling",
      seamless: "seamless",
      selected: "selected",
      shape: "shape",
      size: "size",
      sizes: "sizes",
      span: "span",
      spellcheck: "spellCheck",
      src: "src",
      srcdoc: "srcDoc",
      srclang: "srcLang",
      srcset: "srcSet",
      start: "start",
      step: "step",
      style: "style",
      summary: "summary",
      tabindex: "tabIndex",
      target: "target",
      title: "title",
      type: "type",
      usemap: "useMap",
      value: "value",
      width: "width",
      wmode: "wmode",
      wrap: "wrap",
      about: "about",
      accentheight: "accentHeight",
      "accent-height": "accentHeight",
      accumulate: "accumulate",
      additive: "additive",
      alignmentbaseline: "alignmentBaseline",
      "alignment-baseline": "alignmentBaseline",
      allowreorder: "allowReorder",
      alphabetic: "alphabetic",
      amplitude: "amplitude",
      arabicform: "arabicForm",
      "arabic-form": "arabicForm",
      ascent: "ascent",
      attributename: "attributeName",
      attributetype: "attributeType",
      autoreverse: "autoReverse",
      azimuth: "azimuth",
      basefrequency: "baseFrequency",
      baselineshift: "baselineShift",
      "baseline-shift": "baselineShift",
      baseprofile: "baseProfile",
      bbox: "bbox",
      begin: "begin",
      bias: "bias",
      by: "by",
      calcmode: "calcMode",
      capheight: "capHeight",
      "cap-height": "capHeight",
      clip: "clip",
      clippath: "clipPath",
      "clip-path": "clipPath",
      clippathunits: "clipPathUnits",
      cliprule: "clipRule",
      "clip-rule": "clipRule",
      color: "color",
      colorinterpolation: "colorInterpolation",
      "color-interpolation": "colorInterpolation",
      colorinterpolationfilters: "colorInterpolationFilters",
      "color-interpolation-filters": "colorInterpolationFilters",
      colorprofile: "colorProfile",
      "color-profile": "colorProfile",
      colorrendering: "colorRendering",
      "color-rendering": "colorRendering",
      contentscripttype: "contentScriptType",
      contentstyletype: "contentStyleType",
      cursor: "cursor",
      cx: "cx",
      cy: "cy",
      d: "d",
      datatype: "datatype",
      decelerate: "decelerate",
      descent: "descent",
      diffuseconstant: "diffuseConstant",
      direction: "direction",
      display: "display",
      divisor: "divisor",
      dominantbaseline: "dominantBaseline",
      "dominant-baseline": "dominantBaseline",
      dur: "dur",
      dx: "dx",
      dy: "dy",
      edgemode: "edgeMode",
      elevation: "elevation",
      enablebackground: "enableBackground",
      "enable-background": "enableBackground",
      end: "end",
      exponent: "exponent",
      externalresourcesrequired: "externalResourcesRequired",
      fill: "fill",
      fillopacity: "fillOpacity",
      "fill-opacity": "fillOpacity",
      fillrule: "fillRule",
      "fill-rule": "fillRule",
      filter: "filter",
      filterres: "filterRes",
      filterunits: "filterUnits",
      floodopacity: "floodOpacity",
      "flood-opacity": "floodOpacity",
      floodcolor: "floodColor",
      "flood-color": "floodColor",
      focusable: "focusable",
      fontfamily: "fontFamily",
      "font-family": "fontFamily",
      fontsize: "fontSize",
      "font-size": "fontSize",
      fontsizeadjust: "fontSizeAdjust",
      "font-size-adjust": "fontSizeAdjust",
      fontstretch: "fontStretch",
      "font-stretch": "fontStretch",
      fontstyle: "fontStyle",
      "font-style": "fontStyle",
      fontvariant: "fontVariant",
      "font-variant": "fontVariant",
      fontweight: "fontWeight",
      "font-weight": "fontWeight",
      format: "format",
      from: "from",
      fx: "fx",
      fy: "fy",
      g1: "g1",
      g2: "g2",
      glyphname: "glyphName",
      "glyph-name": "glyphName",
      glyphorientationhorizontal: "glyphOrientationHorizontal",
      "glyph-orientation-horizontal": "glyphOrientationHorizontal",
      glyphorientationvertical: "glyphOrientationVertical",
      "glyph-orientation-vertical": "glyphOrientationVertical",
      glyphref: "glyphRef",
      gradienttransform: "gradientTransform",
      gradientunits: "gradientUnits",
      hanging: "hanging",
      horizadvx: "horizAdvX",
      "horiz-adv-x": "horizAdvX",
      horizoriginx: "horizOriginX",
      "horiz-origin-x": "horizOriginX",
      ideographic: "ideographic",
      imagerendering: "imageRendering",
      "image-rendering": "imageRendering",
      in2: "in2",
      in: "in",
      inlist: "inlist",
      intercept: "intercept",
      k1: "k1",
      k2: "k2",
      k3: "k3",
      k4: "k4",
      k: "k",
      kernelmatrix: "kernelMatrix",
      kernelunitlength: "kernelUnitLength",
      kerning: "kerning",
      keypoints: "keyPoints",
      keysplines: "keySplines",
      keytimes: "keyTimes",
      lengthadjust: "lengthAdjust",
      letterspacing: "letterSpacing",
      "letter-spacing": "letterSpacing",
      lightingcolor: "lightingColor",
      "lighting-color": "lightingColor",
      limitingconeangle: "limitingConeAngle",
      local: "local",
      markerend: "markerEnd",
      "marker-end": "markerEnd",
      markerheight: "markerHeight",
      markermid: "markerMid",
      "marker-mid": "markerMid",
      markerstart: "markerStart",
      "marker-start": "markerStart",
      markerunits: "markerUnits",
      markerwidth: "markerWidth",
      mask: "mask",
      maskcontentunits: "maskContentUnits",
      maskunits: "maskUnits",
      mathematical: "mathematical",
      mode: "mode",
      numoctaves: "numOctaves",
      offset: "offset",
      opacity: "opacity",
      operator: "operator",
      order: "order",
      orient: "orient",
      orientation: "orientation",
      origin: "origin",
      overflow: "overflow",
      overlineposition: "overlinePosition",
      "overline-position": "overlinePosition",
      overlinethickness: "overlineThickness",
      "overline-thickness": "overlineThickness",
      paintorder: "paintOrder",
      "paint-order": "paintOrder",
      panose1: "panose1",
      "panose-1": "panose1",
      pathlength: "pathLength",
      patterncontentunits: "patternContentUnits",
      patterntransform: "patternTransform",
      patternunits: "patternUnits",
      pointerevents: "pointerEvents",
      "pointer-events": "pointerEvents",
      points: "points",
      pointsatx: "pointsAtX",
      pointsaty: "pointsAtY",
      pointsatz: "pointsAtZ",
      popover: "popover",
      popovertarget: "popoverTarget",
      popovertargetaction: "popoverTargetAction",
      prefix: "prefix",
      preservealpha: "preserveAlpha",
      preserveaspectratio: "preserveAspectRatio",
      primitiveunits: "primitiveUnits",
      property: "property",
      r: "r",
      radius: "radius",
      refx: "refX",
      refy: "refY",
      renderingintent: "renderingIntent",
      "rendering-intent": "renderingIntent",
      repeatcount: "repeatCount",
      repeatdur: "repeatDur",
      requiredextensions: "requiredExtensions",
      requiredfeatures: "requiredFeatures",
      resource: "resource",
      restart: "restart",
      result: "result",
      results: "results",
      rotate: "rotate",
      rx: "rx",
      ry: "ry",
      scale: "scale",
      security: "security",
      seed: "seed",
      shaperendering: "shapeRendering",
      "shape-rendering": "shapeRendering",
      slope: "slope",
      spacing: "spacing",
      specularconstant: "specularConstant",
      specularexponent: "specularExponent",
      speed: "speed",
      spreadmethod: "spreadMethod",
      startoffset: "startOffset",
      stddeviation: "stdDeviation",
      stemh: "stemh",
      stemv: "stemv",
      stitchtiles: "stitchTiles",
      stopcolor: "stopColor",
      "stop-color": "stopColor",
      stopopacity: "stopOpacity",
      "stop-opacity": "stopOpacity",
      strikethroughposition: "strikethroughPosition",
      "strikethrough-position": "strikethroughPosition",
      strikethroughthickness: "strikethroughThickness",
      "strikethrough-thickness": "strikethroughThickness",
      string: "string",
      stroke: "stroke",
      strokedasharray: "strokeDasharray",
      "stroke-dasharray": "strokeDasharray",
      strokedashoffset: "strokeDashoffset",
      "stroke-dashoffset": "strokeDashoffset",
      strokelinecap: "strokeLinecap",
      "stroke-linecap": "strokeLinecap",
      strokelinejoin: "strokeLinejoin",
      "stroke-linejoin": "strokeLinejoin",
      strokemiterlimit: "strokeMiterlimit",
      "stroke-miterlimit": "strokeMiterlimit",
      strokewidth: "strokeWidth",
      "stroke-width": "strokeWidth",
      strokeopacity: "strokeOpacity",
      "stroke-opacity": "strokeOpacity",
      suppresscontenteditablewarning: "suppressContentEditableWarning",
      suppresshydrationwarning: "suppressHydrationWarning",
      surfacescale: "surfaceScale",
      systemlanguage: "systemLanguage",
      tablevalues: "tableValues",
      targetx: "targetX",
      targety: "targetY",
      textanchor: "textAnchor",
      "text-anchor": "textAnchor",
      textdecoration: "textDecoration",
      "text-decoration": "textDecoration",
      textlength: "textLength",
      textrendering: "textRendering",
      "text-rendering": "textRendering",
      to: "to",
      transform: "transform",
      transformorigin: "transformOrigin",
      "transform-origin": "transformOrigin",
      typeof: "typeof",
      u1: "u1",
      u2: "u2",
      underlineposition: "underlinePosition",
      "underline-position": "underlinePosition",
      underlinethickness: "underlineThickness",
      "underline-thickness": "underlineThickness",
      unicode: "unicode",
      unicodebidi: "unicodeBidi",
      "unicode-bidi": "unicodeBidi",
      unicoderange: "unicodeRange",
      "unicode-range": "unicodeRange",
      unitsperem: "unitsPerEm",
      "units-per-em": "unitsPerEm",
      unselectable: "unselectable",
      valphabetic: "vAlphabetic",
      "v-alphabetic": "vAlphabetic",
      values: "values",
      vectoreffect: "vectorEffect",
      "vector-effect": "vectorEffect",
      version: "version",
      vertadvy: "vertAdvY",
      "vert-adv-y": "vertAdvY",
      vertoriginx: "vertOriginX",
      "vert-origin-x": "vertOriginX",
      vertoriginy: "vertOriginY",
      "vert-origin-y": "vertOriginY",
      vhanging: "vHanging",
      "v-hanging": "vHanging",
      videographic: "vIdeographic",
      "v-ideographic": "vIdeographic",
      viewbox: "viewBox",
      viewtarget: "viewTarget",
      visibility: "visibility",
      vmathematical: "vMathematical",
      "v-mathematical": "vMathematical",
      vocab: "vocab",
      widths: "widths",
      wordspacing: "wordSpacing",
      "word-spacing": "wordSpacing",
      writingmode: "writingMode",
      "writing-mode": "writingMode",
      x1: "x1",
      x2: "x2",
      x: "x",
      xchannelselector: "xChannelSelector",
      xheight: "xHeight",
      "x-height": "xHeight",
      xlinkactuate: "xlinkActuate",
      "xlink:actuate": "xlinkActuate",
      xlinkarcrole: "xlinkArcrole",
      "xlink:arcrole": "xlinkArcrole",
      xlinkhref: "xlinkHref",
      "xlink:href": "xlinkHref",
      xlinkrole: "xlinkRole",
      "xlink:role": "xlinkRole",
      xlinkshow: "xlinkShow",
      "xlink:show": "xlinkShow",
      xlinktitle: "xlinkTitle",
      "xlink:title": "xlinkTitle",
      xlinktype: "xlinkType",
      "xlink:type": "xlinkType",
      xmlbase: "xmlBase",
      "xml:base": "xmlBase",
      xmllang: "xmlLang",
      "xml:lang": "xmlLang",
      xmlns: "xmlns",
      "xml:space": "xmlSpace",
      xmlnsxlink: "xmlnsXlink",
      "xmlns:xlink": "xmlnsXlink",
      xmlspace: "xmlSpace",
      y1: "y1",
      y2: "y2",
      y: "y",
      ychannelselector: "yChannelSelector",
      z: "z",
      zoomandpan: "zoomAndPan"
    }, kg = {
      "aria-current": 0,
      "aria-description": 0,
      "aria-details": 0,
      "aria-disabled": 0,
      "aria-hidden": 0,
      "aria-invalid": 0,
      "aria-keyshortcuts": 0,
      "aria-label": 0,
      "aria-roledescription": 0,
      "aria-autocomplete": 0,
      "aria-checked": 0,
      "aria-expanded": 0,
      "aria-haspopup": 0,
      "aria-level": 0,
      "aria-modal": 0,
      "aria-multiline": 0,
      "aria-multiselectable": 0,
      "aria-orientation": 0,
      "aria-placeholder": 0,
      "aria-pressed": 0,
      "aria-readonly": 0,
      "aria-required": 0,
      "aria-selected": 0,
      "aria-sort": 0,
      "aria-valuemax": 0,
      "aria-valuemin": 0,
      "aria-valuenow": 0,
      "aria-valuetext": 0,
      "aria-atomic": 0,
      "aria-busy": 0,
      "aria-live": 0,
      "aria-relevant": 0,
      "aria-dropeffect": 0,
      "aria-grabbed": 0,
      "aria-activedescendant": 0,
      "aria-colcount": 0,
      "aria-colindex": 0,
      "aria-colspan": 0,
      "aria-controls": 0,
      "aria-describedby": 0,
      "aria-errormessage": 0,
      "aria-flowto": 0,
      "aria-labelledby": 0,
      "aria-owns": 0,
      "aria-posinset": 0,
      "aria-rowcount": 0,
      "aria-rowindex": 0,
      "aria-rowspan": 0,
      "aria-setsize": 0,
      "aria-braillelabel": 0,
      "aria-brailleroledescription": 0,
      "aria-colindextext": 0,
      "aria-rowindextext": 0
    }, Zh = {}, nE = RegExp(
      "^(aria)-[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
    ), uE = RegExp(
      "^(aria)[A-Z][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
    ), CS = !1, cn = {}, US = /^on./, cE = /^on[^A-Z]/, iE = RegExp(
      "^(aria)-[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
    ), oE = RegExp(
      "^(aria)[A-Z][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
    ), fE = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i, M0 = null, Jh = null, Kh = null, m1 = !1, mi = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), y1 = !1;
    if (mi)
      try {
        var C0 = {};
        Object.defineProperty(C0, "passive", {
          get: function() {
            y1 = !0;
          }
        }), window.addEventListener("test", C0, C0), window.removeEventListener("test", C0, C0);
      } catch {
        y1 = !1;
      }
    var Qf = null, p1 = null, Wg = null, Ur = {
      eventPhase: 0,
      bubbles: 0,
      cancelable: 0,
      timeStamp: function(e) {
        return e.timeStamp || Date.now();
      },
      defaultPrevented: 0,
      isTrusted: 0
    }, Fg = Hl(Ur), U0 = Ie({}, Ur, { view: 0, detail: 0 }), sE = Hl(U0), g1, v1, x0, Ig = Ie({}, U0, {
      screenX: 0,
      screenY: 0,
      clientX: 0,
      clientY: 0,
      pageX: 0,
      pageY: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      getModifierState: Es,
      button: 0,
      buttons: 0,
      relatedTarget: function(e) {
        return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
      },
      movementX: function(e) {
        return "movementX" in e ? e.movementX : (e !== x0 && (x0 && e.type === "mousemove" ? (g1 = e.screenX - x0.screenX, v1 = e.screenY - x0.screenY) : v1 = g1 = 0, x0 = e), g1);
      },
      movementY: function(e) {
        return "movementY" in e ? e.movementY : v1;
      }
    }), xS = Hl(Ig), rE = Ie({}, Ig, { dataTransfer: 0 }), dE = Hl(rE), hE = Ie({}, U0, { relatedTarget: 0 }), S1 = Hl(hE), mE = Ie({}, Ur, {
      animationName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), yE = Hl(mE), pE = Ie({}, Ur, {
      clipboardData: function(e) {
        return "clipboardData" in e ? e.clipboardData : window.clipboardData;
      }
    }), gE = Hl(pE), vE = Ie({}, Ur, { data: 0 }), NS = Hl(
      vE
    ), SE = NS, bE = {
      Esc: "Escape",
      Spacebar: " ",
      Left: "ArrowLeft",
      Up: "ArrowUp",
      Right: "ArrowRight",
      Down: "ArrowDown",
      Del: "Delete",
      Win: "OS",
      Menu: "ContextMenu",
      Apps: "ContextMenu",
      Scroll: "ScrollLock",
      MozPrintableKey: "Unidentified"
    }, EE = {
      8: "Backspace",
      9: "Tab",
      12: "Clear",
      13: "Enter",
      16: "Shift",
      17: "Control",
      18: "Alt",
      19: "Pause",
      20: "CapsLock",
      27: "Escape",
      32: " ",
      33: "PageUp",
      34: "PageDown",
      35: "End",
      36: "Home",
      37: "ArrowLeft",
      38: "ArrowUp",
      39: "ArrowRight",
      40: "ArrowDown",
      45: "Insert",
      46: "Delete",
      112: "F1",
      113: "F2",
      114: "F3",
      115: "F4",
      116: "F5",
      117: "F6",
      118: "F7",
      119: "F8",
      120: "F9",
      121: "F10",
      122: "F11",
      123: "F12",
      144: "NumLock",
      145: "ScrollLock",
      224: "Meta"
    }, TE = {
      Alt: "altKey",
      Control: "ctrlKey",
      Meta: "metaKey",
      Shift: "shiftKey"
    }, AE = Ie({}, U0, {
      key: function(e) {
        if (e.key) {
          var t = bE[e.key] || e.key;
          if (t !== "Unidentified") return t;
        }
        return e.type === "keypress" ? (e = bs(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? EE[e.keyCode] || "Unidentified" : "";
      },
      code: 0,
      location: 0,
      ctrlKey: 0,
      shiftKey: 0,
      altKey: 0,
      metaKey: 0,
      repeat: 0,
      locale: 0,
      getModifierState: Es,
      charCode: function(e) {
        return e.type === "keypress" ? bs(e) : 0;
      },
      keyCode: function(e) {
        return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      },
      which: function(e) {
        return e.type === "keypress" ? bs(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
      }
    }), OE = Hl(AE), zE = Ie({}, Ig, {
      pointerId: 0,
      width: 0,
      height: 0,
      pressure: 0,
      tangentialPressure: 0,
      tiltX: 0,
      tiltY: 0,
      twist: 0,
      pointerType: 0,
      isPrimary: 0
    }), HS = Hl(zE), DE = Ie({}, U0, {
      touches: 0,
      targetTouches: 0,
      changedTouches: 0,
      altKey: 0,
      metaKey: 0,
      ctrlKey: 0,
      shiftKey: 0,
      getModifierState: Es
    }), RE = Hl(DE), _E = Ie({}, Ur, {
      propertyName: 0,
      elapsedTime: 0,
      pseudoElement: 0
    }), ME = Hl(_E), CE = Ie({}, Ig, {
      deltaX: function(e) {
        return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
      },
      deltaY: function(e) {
        return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
      },
      deltaZ: 0,
      deltaMode: 0
    }), UE = Hl(CE), xE = Ie({}, Ur, {
      newState: 0,
      oldState: 0
    }), NE = Hl(xE), HE = [9, 13, 27, 32], jS = 229, b1 = mi && "CompositionEvent" in window, N0 = null;
    mi && "documentMode" in document && (N0 = document.documentMode);
    var jE = mi && "TextEvent" in window && !N0, BS = mi && (!b1 || N0 && 8 < N0 && 11 >= N0), YS = 32, qS = String.fromCharCode(YS), wS = !1, $h = !1, BE = {
      color: !0,
      date: !0,
      datetime: !0,
      "datetime-local": !0,
      email: !0,
      month: !0,
      number: !0,
      password: !0,
      range: !0,
      search: !0,
      tel: !0,
      text: !0,
      time: !0,
      url: !0,
      week: !0
    }, H0 = null, j0 = null, GS = !1;
    mi && (GS = yd("input") && (!document.documentMode || 9 < document.documentMode));
    var on = typeof Object.is == "function" ? Object.is : pd, YE = mi && "documentMode" in document && 11 >= document.documentMode, kh = null, E1 = null, B0 = null, T1 = !1, Wh = {
      animationend: _i("Animation", "AnimationEnd"),
      animationiteration: _i("Animation", "AnimationIteration"),
      animationstart: _i("Animation", "AnimationStart"),
      transitionrun: _i("Transition", "TransitionRun"),
      transitionstart: _i("Transition", "TransitionStart"),
      transitioncancel: _i("Transition", "TransitionCancel"),
      transitionend: _i("Transition", "TransitionEnd")
    }, A1 = {}, XS = {};
    mi && (XS = document.createElement("div").style, "AnimationEvent" in window || (delete Wh.animationend.animation, delete Wh.animationiteration.animation, delete Wh.animationstart.animation), "TransitionEvent" in window || delete Wh.transitionend.transition);
    var LS = Mi("animationend"), QS = Mi("animationiteration"), VS = Mi("animationstart"), qE = Mi("transitionrun"), wE = Mi("transitionstart"), GE = Mi("transitioncancel"), ZS = Mi("transitionend"), JS = /* @__PURE__ */ new Map(), O1 = "abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(
      " "
    );
    O1.push("scrollEnd");
    var KS = 0;
    if (typeof performance == "object" && typeof performance.now == "function")
      var XE = performance, $S = function() {
        return XE.now();
      };
    else {
      var LE = Date;
      $S = function() {
        return LE.now();
      };
    }
    var z1 = typeof reportError == "function" ? reportError : function(e) {
      if (typeof window == "object" && typeof window.ErrorEvent == "function") {
        var t = new window.ErrorEvent("error", {
          bubbles: !0,
          cancelable: !0,
          message: typeof e == "object" && e !== null && typeof e.message == "string" ? String(e.message) : String(e),
          error: e
        });
        if (!window.dispatchEvent(t)) return;
      } else if (typeof process == "object" && typeof process.emit == "function") {
        process.emit("uncaughtException", e);
        return;
      }
      console.error(e);
    }, QE = "This object has been omitted by React in the console log to avoid sending too much data from the server. Try logging smaller or more specific objects.", Pg = 0, D1 = 1, R1 = 2, _1 = 3, ev = "– ", tv = "+ ", kS = "  ", tl = typeof console < "u" && typeof console.timeStamp == "function" && typeof performance < "u" && typeof performance.measure == "function", Xu = "Components ⚛", rt = "Scheduler ⚛", ht = "Blocking", Vf = !1, yo = {
      color: "primary",
      properties: null,
      tooltipText: "",
      track: Xu
    }, Zf = {
      start: -0,
      end: -0,
      detail: { devtools: yo }
    }, VE = ["Changed Props", ""], WS = "This component received deeply equal props. It might benefit from useMemo or the React Compiler in its owner.", ZE = ["Changed Props", WS], Y0 = 1, po = 2, Lu = [], Fh = 0, M1 = 0, Jf = {};
    Object.freeze(Jf);
    var Qu = null, Ih = null, He = 0, JE = 1, Pe = 2, Ba = 8, Tc = 16, KE = 32, FS = !1;
    try {
      var IS = Object.preventExtensions({});
    } catch {
      FS = !0;
    }
    var C1 = /* @__PURE__ */ new WeakMap(), Ph = [], em = 0, lv = null, q0 = 0, Vu = [], Zu = 0, xr = null, go = 1, vo = "", Ra = null, ll = null, st = !1, yi = !1, lu = null, Kf = null, Ju = !1, U1 = Error(
      "Hydration Mismatch Exception: This is not a real error, and should not leak into userspace. If you're seeing this, it's likely a bug in React."
    ), x1 = Yt(null), N1 = Yt(null), PS = {}, av = null, tm = null, lm = !1, $E = typeof AbortController < "u" ? AbortController : function() {
      var e = [], t = this.signal = {
        aborted: !1,
        addEventListener: function(a, c) {
          e.push(c);
        }
      };
      this.abort = function() {
        t.aborted = !0, e.forEach(function(a) {
          return a();
        });
      };
    }, kE = vl.unstable_scheduleCallback, WE = vl.unstable_NormalPriority, Ll = {
      $$typeof: Pn,
      Consumer: null,
      Provider: null,
      _currentValue: null,
      _currentValue2: null,
      _threadCount: 0,
      _currentRenderer: null,
      _currentRenderer2: null
    }, Ql = vl.unstable_now, nv = console.createTask ? console.createTask : function() {
      return null;
    }, w0 = 1, uv = 2, oa = -0, $f = -0, So = -0, bo = null, fn = -1.1, Nr = -0, rl = -0, ze = -1.1, Ue = -1.1, il = null, Sl = !1, Hr = -0, pi = -1.1, G0 = null, kf = 0, H1 = null, j1 = null, jr = -1.1, X0 = null, am = -1.1, cv = -1.1, Eo = -0, To = -1.1, Ku = -1.1, B1 = 0, L0 = null, eb = null, tb = null, Wf = -1.1, Br = null, Ff = -1.1, iv = -1.1, lb = -0, ab = -0, ov = 0, FE = null, nb = 0, Q0 = -1.1, fv = !1, sv = !1, V0 = null, Y1 = 0, Yr = 0, nm = null, ub = G.S;
    G.S = function(e, t) {
      if (e2 = Xl(), typeof t == "object" && t !== null && typeof t.then == "function") {
        if (0 > To && 0 > Ku) {
          To = Ql();
          var a = Of(), c = ju();
          (a !== Ff || c !== Br) && (Ff = -1.1), Wf = a, Br = c;
        }
        nc(e, t);
      }
      ub !== null && ub(e, t);
    };
    var qr = Yt(null), Ac = {
      recordUnsafeLifecycleWarnings: function() {
      },
      flushPendingUnsafeLifecycleWarnings: function() {
      },
      recordLegacyContextWarning: function() {
      },
      flushLegacyContextWarning: function() {
      },
      discardPendingWarnings: function() {
      }
    }, Z0 = [], J0 = [], K0 = [], $0 = [], k0 = [], W0 = [], wr = /* @__PURE__ */ new Set();
    Ac.recordUnsafeLifecycleWarnings = function(e, t) {
      wr.has(e.type) || (typeof t.componentWillMount == "function" && t.componentWillMount.__suppressDeprecationWarning !== !0 && Z0.push(e), e.mode & Ba && typeof t.UNSAFE_componentWillMount == "function" && J0.push(e), typeof t.componentWillReceiveProps == "function" && t.componentWillReceiveProps.__suppressDeprecationWarning !== !0 && K0.push(e), e.mode & Ba && typeof t.UNSAFE_componentWillReceiveProps == "function" && $0.push(e), typeof t.componentWillUpdate == "function" && t.componentWillUpdate.__suppressDeprecationWarning !== !0 && k0.push(e), e.mode & Ba && typeof t.UNSAFE_componentWillUpdate == "function" && W0.push(e));
    }, Ac.flushPendingUnsafeLifecycleWarnings = function() {
      var e = /* @__PURE__ */ new Set();
      0 < Z0.length && (Z0.forEach(function(h) {
        e.add(
          se(h) || "Component"
        ), wr.add(h.type);
      }), Z0 = []);
      var t = /* @__PURE__ */ new Set();
      0 < J0.length && (J0.forEach(function(h) {
        t.add(
          se(h) || "Component"
        ), wr.add(h.type);
      }), J0 = []);
      var a = /* @__PURE__ */ new Set();
      0 < K0.length && (K0.forEach(function(h) {
        a.add(
          se(h) || "Component"
        ), wr.add(h.type);
      }), K0 = []);
      var c = /* @__PURE__ */ new Set();
      0 < $0.length && ($0.forEach(
        function(h) {
          c.add(
            se(h) || "Component"
          ), wr.add(h.type);
        }
      ), $0 = []);
      var o = /* @__PURE__ */ new Set();
      0 < k0.length && (k0.forEach(function(h) {
        o.add(
          se(h) || "Component"
        ), wr.add(h.type);
      }), k0 = []);
      var f = /* @__PURE__ */ new Set();
      if (0 < W0.length && (W0.forEach(function(h) {
        f.add(
          se(h) || "Component"
        ), wr.add(h.type);
      }), W0 = []), 0 < t.size) {
        var d = w(
          t
        );
        console.error(
          `Using UNSAFE_componentWillMount in strict mode is not recommended and may indicate bugs in your code. See https://react.dev/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.

Please update the following components: %s`,
          d
        );
      }
      0 < c.size && (d = w(
        c
      ), console.error(
        `Using UNSAFE_componentWillReceiveProps in strict mode is not recommended and may indicate bugs in your code. See https://react.dev/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://react.dev/link/derived-state

Please update the following components: %s`,
        d
      )), 0 < f.size && (d = w(
        f
      ), console.error(
        `Using UNSAFE_componentWillUpdate in strict mode is not recommended and may indicate bugs in your code. See https://react.dev/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.

Please update the following components: %s`,
        d
      )), 0 < e.size && (d = w(e), console.warn(
        `componentWillMount has been renamed, and is not recommended for use. See https://react.dev/link/unsafe-component-lifecycles for details.

* Move code with side effects to componentDidMount, and set initial state in the constructor.
* Rename componentWillMount to UNSAFE_componentWillMount to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`,
        d
      )), 0 < a.size && (d = w(
        a
      ), console.warn(
        `componentWillReceiveProps has been renamed, and is not recommended for use. See https://react.dev/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* If you're updating state whenever props change, refactor your code to use memoization techniques or move it to static getDerivedStateFromProps. Learn more at: https://react.dev/link/derived-state
* Rename componentWillReceiveProps to UNSAFE_componentWillReceiveProps to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`,
        d
      )), 0 < o.size && (d = w(o), console.warn(
        `componentWillUpdate has been renamed, and is not recommended for use. See https://react.dev/link/unsafe-component-lifecycles for details.

* Move data fetching code or side effects to componentDidUpdate.
* Rename componentWillUpdate to UNSAFE_componentWillUpdate to suppress this warning in non-strict mode. In React 18.x, only the UNSAFE_ name will work. To rename all deprecated lifecycles to their new names, you can run \`npx react-codemod rename-unsafe-lifecycles\` in your project source folder.

Please update the following components: %s`,
        d
      ));
    };
    var rv = /* @__PURE__ */ new Map(), cb = /* @__PURE__ */ new Set();
    Ac.recordLegacyContextWarning = function(e, t) {
      for (var a = null, c = e; c !== null; )
        c.mode & Ba && (a = c), c = c.return;
      a === null ? console.error(
        "Expected to find a StrictMode component in a strict mode tree. This error is likely caused by a bug in React. Please file an issue."
      ) : !cb.has(e.type) && (c = rv.get(a), e.type.contextTypes != null || e.type.childContextTypes != null || t !== null && typeof t.getChildContext == "function") && (c === void 0 && (c = [], rv.set(a, c)), c.push(e));
    }, Ac.flushLegacyContextWarning = function() {
      rv.forEach(function(e) {
        if (e.length !== 0) {
          var t = e[0], a = /* @__PURE__ */ new Set();
          e.forEach(function(o) {
            a.add(se(o) || "Component"), cb.add(o.type);
          });
          var c = w(a);
          oe(t, function() {
            console.error(
              `Legacy context API has been detected within a strict-mode tree.

The old API will be supported in all 16.x releases, but applications using it should migrate to the new version.

Please update the following components: %s

Learn more about this warning here: https://react.dev/link/legacy-context`,
              c
            );
          });
        }
      });
    }, Ac.discardPendingWarnings = function() {
      Z0 = [], J0 = [], K0 = [], $0 = [], k0 = [], W0 = [], rv = /* @__PURE__ */ new Map();
    };
    var ib = {
      react_stack_bottom_frame: function(e, t, a) {
        var c = Yu;
        Yu = !0;
        try {
          return e(t, a);
        } finally {
          Yu = c;
        }
      }
    }, q1 = ib.react_stack_bottom_frame.bind(ib), ob = {
      react_stack_bottom_frame: function(e) {
        var t = Yu;
        Yu = !0;
        try {
          return e.render();
        } finally {
          Yu = t;
        }
      }
    }, fb = ob.react_stack_bottom_frame.bind(ob), sb = {
      react_stack_bottom_frame: function(e, t) {
        try {
          t.componentDidMount();
        } catch (a) {
          ke(e, e.return, a);
        }
      }
    }, w1 = sb.react_stack_bottom_frame.bind(
      sb
    ), rb = {
      react_stack_bottom_frame: function(e, t, a, c, o) {
        try {
          t.componentDidUpdate(a, c, o);
        } catch (f) {
          ke(e, e.return, f);
        }
      }
    }, db = rb.react_stack_bottom_frame.bind(
      rb
    ), hb = {
      react_stack_bottom_frame: function(e, t) {
        var a = t.stack;
        e.componentDidCatch(t.value, {
          componentStack: a !== null ? a : ""
        });
      }
    }, IE = hb.react_stack_bottom_frame.bind(
      hb
    ), mb = {
      react_stack_bottom_frame: function(e, t, a) {
        try {
          a.componentWillUnmount();
        } catch (c) {
          ke(e, t, c);
        }
      }
    }, yb = mb.react_stack_bottom_frame.bind(
      mb
    ), pb = {
      react_stack_bottom_frame: function(e) {
        var t = e.create;
        return e = e.inst, t = t(), e.destroy = t;
      }
    }, PE = pb.react_stack_bottom_frame.bind(pb), gb = {
      react_stack_bottom_frame: function(e, t, a) {
        try {
          a();
        } catch (c) {
          ke(e, t, c);
        }
      }
    }, eT = gb.react_stack_bottom_frame.bind(gb), vb = {
      react_stack_bottom_frame: function(e) {
        var t = e._init;
        return t(e._payload);
      }
    }, tT = vb.react_stack_bottom_frame.bind(vb), um = Error(
      "Suspense Exception: This is not a real error! It's an implementation detail of `use` to interrupt the current render. You must either rethrow it immediately, or move the `use` call outside of the `try/catch` block. Capturing without rethrowing will lead to unexpected behavior.\n\nTo handle async errors, wrap your component in an error boundary, or call the promise's `.catch` method and pass the result to `use`."
    ), G1 = Error(
      "Suspense Exception: This is not a real error, and should not leak into userspace. If you're seeing this, it's likely a bug in React."
    ), dv = Error(
      "Suspense Exception: This is not a real error! It's an implementation detail of `useActionState` to interrupt the current render. You must either rethrow it immediately, or move the `useActionState` call outside of the `try/catch` block. Capturing without rethrowing will lead to unexpected behavior.\n\nTo handle async errors, wrap your component in an error boundary."
    ), hv = {
      then: function() {
        console.error(
          'Internal React error: A listener was unexpectedly attached to a "noop" thenable. This is a bug in React. Please file an issue.'
        );
      }
    }, Gr = null, F0 = !1, cm = null, I0 = 0, et = null, X1, Sb = X1 = !1, bb = {}, Eb = {}, Tb = {};
    Ne = function(e, t, a) {
      if (a !== null && typeof a == "object" && a._store && (!a._store.validated && a.key == null || a._store.validated === 2)) {
        if (typeof a._store != "object")
          throw Error(
            "React Component in warnForMissingKey should have a _store. This error is likely caused by a bug in React. Please file an issue."
          );
        a._store.validated = 1;
        var c = se(e), o = c || "null";
        if (!bb[o]) {
          bb[o] = !0, a = a._owner, e = e._debugOwner;
          var f = "";
          e && typeof e.tag == "number" && (o = se(e)) && (f = `

Check the render method of \`` + o + "`."), f || c && (f = `

Check the top-level render call using <` + c + ">.");
          var d = "";
          a != null && e !== a && (c = null, typeof a.tag == "number" ? c = se(a) : typeof a.name == "string" && (c = a.name), c && (d = " It was passed a child from " + c + ".")), oe(t, function() {
            console.error(
              'Each child in a list should have a unique "key" prop.%s%s See https://react.dev/link/warning-keys for more information.',
              f,
              d
            );
          });
        }
      }
    };
    var Xr = Bl(!0), Ab = Bl(!1), Ob = 0, zb = 1, Db = 2, L1 = 3, If = !1, Rb = !1, Q1 = null, V1 = !1, im = Yt(null), mv = Yt(0), au = Yt(null), $u = null, om = 1, P0 = 2, Ul = Yt(0), yv = 0, ku = 1, sn = 2, nu = 4, rn = 8, fm, _b = /* @__PURE__ */ new Set(), Mb = /* @__PURE__ */ new Set(), Z1 = /* @__PURE__ */ new Set(), Cb = /* @__PURE__ */ new Set(), Ao = 0, qe = null, Zt = null, Vl = null, pv = !1, sm = !1, Lr = !1, gv = 0, ep = 0, Oo = null, lT = 0, aT = 25, q = null, Wu = null, zo = -1, tp = !1, lp = {
      readContext: Et,
      use: oc,
      useCallback: fl,
      useContext: fl,
      useEffect: fl,
      useImperativeHandle: fl,
      useLayoutEffect: fl,
      useInsertionEffect: fl,
      useMemo: fl,
      useReducer: fl,
      useRef: fl,
      useState: fl,
      useDebugValue: fl,
      useDeferredValue: fl,
      useTransition: fl,
      useSyncExternalStore: fl,
      useId: fl,
      useHostTransitionStatus: fl,
      useFormState: fl,
      useActionState: fl,
      useOptimistic: fl,
      useMemoCache: fl,
      useCacheRefresh: fl
    };
    lp.useEffectEvent = fl;
    var J1 = null, Ub = null, K1 = null, xb = null, gi = null, Oc = null, vv = null;
    J1 = {
      readContext: function(e) {
        return Et(e);
      },
      use: oc,
      useCallback: function(e, t) {
        return q = "useCallback", Ye(), ic(t), Yd(e, t);
      },
      useContext: function(e) {
        return q = "useContext", Ye(), Et(e);
      },
      useEffect: function(e, t) {
        return q = "useEffect", Ye(), ic(t), Ji(e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", Ye(), ic(a), Au(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        q = "useInsertionEffect", Ye(), ic(t), Ic(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", Ye(), ic(t), ga(e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", Ye(), ic(t);
        var a = G.H;
        G.H = gi;
        try {
          return va(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", Ye();
        var c = G.H;
        G.H = gi;
        try {
          return Po(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function(e) {
        return q = "useRef", Ye(), Bd(e);
      },
      useState: function(e) {
        q = "useState", Ye();
        var t = G.H;
        G.H = gi;
        try {
          return $c(e);
        } finally {
          G.H = t;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", Ye();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", Ye(), nf(e, t);
      },
      useTransition: function() {
        return q = "useTransition", Ye(), Pc();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", Ye(), ef(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", Ye(), Zs();
      },
      useFormState: function(e, t) {
        return q = "useFormState", Ye(), Hs(), Fa(e, t);
      },
      useActionState: function(e, t) {
        return q = "useActionState", Ye(), Fa(e, t);
      },
      useOptimistic: function(e) {
        return q = "useOptimistic", Ye(), Zi(e);
      },
      useHostTransitionStatus: dc,
      useMemoCache: ka,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", Ye(), qd();
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", Ye(), Qs(e);
      }
    }, Ub = {
      readContext: function(e) {
        return Et(e);
      },
      use: oc,
      useCallback: function(e, t) {
        return q = "useCallback", k(), Yd(e, t);
      },
      useContext: function(e) {
        return q = "useContext", k(), Et(e);
      },
      useEffect: function(e, t) {
        return q = "useEffect", k(), Ji(e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", k(), Au(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        q = "useInsertionEffect", k(), Ic(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", k(), ga(e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", k();
        var a = G.H;
        G.H = gi;
        try {
          return va(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", k();
        var c = G.H;
        G.H = gi;
        try {
          return Po(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function(e) {
        return q = "useRef", k(), Bd(e);
      },
      useState: function(e) {
        q = "useState", k();
        var t = G.H;
        G.H = gi;
        try {
          return $c(e);
        } finally {
          G.H = t;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", k();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", k(), nf(e, t);
      },
      useTransition: function() {
        return q = "useTransition", k(), Pc();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", k(), ef(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", k(), Zs();
      },
      useActionState: function(e, t) {
        return q = "useActionState", k(), Fa(e, t);
      },
      useFormState: function(e, t) {
        return q = "useFormState", k(), Hs(), Fa(e, t);
      },
      useOptimistic: function(e) {
        return q = "useOptimistic", k(), Zi(e);
      },
      useHostTransitionStatus: dc,
      useMemoCache: ka,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", k(), qd();
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", k(), Qs(e);
      }
    }, K1 = {
      readContext: function(e) {
        return Et(e);
      },
      use: oc,
      useCallback: function(e, t) {
        return q = "useCallback", k(), Vn(e, t);
      },
      useContext: function(e) {
        return q = "useContext", k(), Et(e);
      },
      useEffect: function(e, t) {
        q = "useEffect", k(), Rl(2048, rn, e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", k(), af(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        return q = "useInsertionEffect", k(), Rl(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", k(), Rl(4, nu, e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", k();
        var a = G.H;
        G.H = Oc;
        try {
          return It(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", k();
        var c = G.H;
        G.H = Oc;
        try {
          return Li(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function() {
        return q = "useRef", k(), Dt().memoizedState;
      },
      useState: function() {
        q = "useState", k();
        var e = G.H;
        G.H = Oc;
        try {
          return Li(Wa);
        } finally {
          G.H = e;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", k();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", k(), Ou(e, t);
      },
      useTransition: function() {
        return q = "useTransition", k(), Kp();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", k(), Vi(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", k(), Dt().memoizedState;
      },
      useFormState: function(e) {
        return q = "useFormState", k(), Hs(), Wc(e);
      },
      useActionState: function(e) {
        return q = "useActionState", k(), Wc(e);
      },
      useOptimistic: function(e, t) {
        return q = "useOptimistic", k(), Gs(e, t);
      },
      useHostTransitionStatus: dc,
      useMemoCache: ka,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", k(), Dt().memoizedState;
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", k(), lf(e);
      }
    }, xb = {
      readContext: function(e) {
        return Et(e);
      },
      use: oc,
      useCallback: function(e, t) {
        return q = "useCallback", k(), Vn(e, t);
      },
      useContext: function(e) {
        return q = "useContext", k(), Et(e);
      },
      useEffect: function(e, t) {
        q = "useEffect", k(), Rl(2048, rn, e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", k(), af(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        return q = "useInsertionEffect", k(), Rl(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", k(), Rl(4, nu, e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", k();
        var a = G.H;
        G.H = vv;
        try {
          return It(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", k();
        var c = G.H;
        G.H = vv;
        try {
          return Qi(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function() {
        return q = "useRef", k(), Dt().memoizedState;
      },
      useState: function() {
        q = "useState", k();
        var e = G.H;
        G.H = vv;
        try {
          return Qi(Wa);
        } finally {
          G.H = e;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", k();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", k(), Ke(e, t);
      },
      useTransition: function() {
        return q = "useTransition", k(), nl();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", k(), Vi(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", k(), Dt().memoizedState;
      },
      useFormState: function(e) {
        return q = "useFormState", k(), Hs(), Fc(e);
      },
      useActionState: function(e) {
        return q = "useActionState", k(), Fc(e);
      },
      useOptimistic: function(e, t) {
        return q = "useOptimistic", k(), Xs(e, t);
      },
      useHostTransitionStatus: dc,
      useMemoCache: ka,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", k(), Dt().memoizedState;
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", k(), lf(e);
      }
    }, gi = {
      readContext: function(e) {
        return ne(), Et(e);
      },
      use: function(e) {
        return le(), oc(e);
      },
      useCallback: function(e, t) {
        return q = "useCallback", le(), Ye(), Yd(e, t);
      },
      useContext: function(e) {
        return q = "useContext", le(), Ye(), Et(e);
      },
      useEffect: function(e, t) {
        return q = "useEffect", le(), Ye(), Ji(e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", le(), Ye(), Au(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        q = "useInsertionEffect", le(), Ye(), Ic(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", le(), Ye(), ga(e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", le(), Ye();
        var a = G.H;
        G.H = gi;
        try {
          return va(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", le(), Ye();
        var c = G.H;
        G.H = gi;
        try {
          return Po(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function(e) {
        return q = "useRef", le(), Ye(), Bd(e);
      },
      useState: function(e) {
        q = "useState", le(), Ye();
        var t = G.H;
        G.H = gi;
        try {
          return $c(e);
        } finally {
          G.H = t;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", le(), Ye();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", le(), Ye(), nf(e, t);
      },
      useTransition: function() {
        return q = "useTransition", le(), Ye(), Pc();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", le(), Ye(), ef(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", le(), Ye(), Zs();
      },
      useFormState: function(e, t) {
        return q = "useFormState", le(), Ye(), Fa(e, t);
      },
      useActionState: function(e, t) {
        return q = "useActionState", le(), Ye(), Fa(e, t);
      },
      useOptimistic: function(e) {
        return q = "useOptimistic", le(), Ye(), Zi(e);
      },
      useMemoCache: function(e) {
        return le(), ka(e);
      },
      useHostTransitionStatus: dc,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", Ye(), qd();
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", le(), Ye(), Qs(e);
      }
    }, Oc = {
      readContext: function(e) {
        return ne(), Et(e);
      },
      use: function(e) {
        return le(), oc(e);
      },
      useCallback: function(e, t) {
        return q = "useCallback", le(), k(), Vn(e, t);
      },
      useContext: function(e) {
        return q = "useContext", le(), k(), Et(e);
      },
      useEffect: function(e, t) {
        q = "useEffect", le(), k(), Rl(2048, rn, e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", le(), k(), af(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        return q = "useInsertionEffect", le(), k(), Rl(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", le(), k(), Rl(4, nu, e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", le(), k();
        var a = G.H;
        G.H = Oc;
        try {
          return It(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", le(), k();
        var c = G.H;
        G.H = Oc;
        try {
          return Li(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function() {
        return q = "useRef", le(), k(), Dt().memoizedState;
      },
      useState: function() {
        q = "useState", le(), k();
        var e = G.H;
        G.H = Oc;
        try {
          return Li(Wa);
        } finally {
          G.H = e;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", le(), k();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", le(), k(), Ou(e, t);
      },
      useTransition: function() {
        return q = "useTransition", le(), k(), Kp();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", le(), k(), Vi(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", le(), k(), Dt().memoizedState;
      },
      useFormState: function(e) {
        return q = "useFormState", le(), k(), Wc(e);
      },
      useActionState: function(e) {
        return q = "useActionState", le(), k(), Wc(e);
      },
      useOptimistic: function(e, t) {
        return q = "useOptimistic", le(), k(), Gs(e, t);
      },
      useMemoCache: function(e) {
        return le(), ka(e);
      },
      useHostTransitionStatus: dc,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", k(), Dt().memoizedState;
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", le(), k(), lf(e);
      }
    }, vv = {
      readContext: function(e) {
        return ne(), Et(e);
      },
      use: function(e) {
        return le(), oc(e);
      },
      useCallback: function(e, t) {
        return q = "useCallback", le(), k(), Vn(e, t);
      },
      useContext: function(e) {
        return q = "useContext", le(), k(), Et(e);
      },
      useEffect: function(e, t) {
        q = "useEffect", le(), k(), Rl(2048, rn, e, t);
      },
      useImperativeHandle: function(e, t, a) {
        return q = "useImperativeHandle", le(), k(), af(e, t, a);
      },
      useInsertionEffect: function(e, t) {
        return q = "useInsertionEffect", le(), k(), Rl(4, sn, e, t);
      },
      useLayoutEffect: function(e, t) {
        return q = "useLayoutEffect", le(), k(), Rl(4, nu, e, t);
      },
      useMemo: function(e, t) {
        q = "useMemo", le(), k();
        var a = G.H;
        G.H = Oc;
        try {
          return It(e, t);
        } finally {
          G.H = a;
        }
      },
      useReducer: function(e, t, a) {
        q = "useReducer", le(), k();
        var c = G.H;
        G.H = Oc;
        try {
          return Qi(e, t, a);
        } finally {
          G.H = c;
        }
      },
      useRef: function() {
        return q = "useRef", le(), k(), Dt().memoizedState;
      },
      useState: function() {
        q = "useState", le(), k();
        var e = G.H;
        G.H = Oc;
        try {
          return Qi(Wa);
        } finally {
          G.H = e;
        }
      },
      useDebugValue: function() {
        q = "useDebugValue", le(), k();
      },
      useDeferredValue: function(e, t) {
        return q = "useDeferredValue", le(), k(), Ke(e, t);
      },
      useTransition: function() {
        return q = "useTransition", le(), k(), nl();
      },
      useSyncExternalStore: function(e, t, a) {
        return q = "useSyncExternalStore", le(), k(), Vi(
          e,
          t,
          a
        );
      },
      useId: function() {
        return q = "useId", le(), k(), Dt().memoizedState;
      },
      useFormState: function(e) {
        return q = "useFormState", le(), k(), Fc(e);
      },
      useActionState: function(e) {
        return q = "useActionState", le(), k(), Fc(e);
      },
      useOptimistic: function(e, t) {
        return q = "useOptimistic", le(), k(), Xs(e, t);
      },
      useMemoCache: function(e) {
        return le(), ka(e);
      },
      useHostTransitionStatus: dc,
      useCacheRefresh: function() {
        return q = "useCacheRefresh", k(), Dt().memoizedState;
      },
      useEffectEvent: function(e) {
        return q = "useEffectEvent", le(), k(), lf(e);
      }
    };
    var Nb = {}, Hb = /* @__PURE__ */ new Set(), jb = /* @__PURE__ */ new Set(), Bb = /* @__PURE__ */ new Set(), Yb = /* @__PURE__ */ new Set(), qb = /* @__PURE__ */ new Set(), wb = /* @__PURE__ */ new Set(), Gb = /* @__PURE__ */ new Set(), Xb = /* @__PURE__ */ new Set(), Lb = /* @__PURE__ */ new Set(), Qb = /* @__PURE__ */ new Set();
    Object.freeze(Nb);
    var $1 = {
      enqueueSetState: function(e, t, a) {
        e = e._reactInternals;
        var c = ua(e), o = Dl(c);
        o.payload = t, a != null && (Wi(a), o.callback = a), t = Su(e, o, c), t !== null && (pu(c, "this.setState()", e), je(t, e, c), Tn(t, e, c));
      },
      enqueueReplaceState: function(e, t, a) {
        e = e._reactInternals;
        var c = ua(e), o = Dl(c);
        o.tag = zb, o.payload = t, a != null && (Wi(a), o.callback = a), t = Su(e, o, c), t !== null && (pu(c, "this.replaceState()", e), je(t, e, c), Tn(t, e, c));
      },
      enqueueForceUpdate: function(e, t) {
        e = e._reactInternals;
        var a = ua(e), c = Dl(a);
        c.tag = Db, t != null && (Wi(t), c.callback = t), t = Su(e, c, a), t !== null && (pu(a, "this.forceUpdate()", e), je(t, e, a), Tn(t, e, a));
      }
    }, rm = null, k1 = null, W1 = Error(
      "This is not a real error. It's an implementation detail of React's selective hydration feature. If this leaks into userspace, it's a bug in React. Please file an issue."
    ), Zl = !1, Vb = {}, Zb = {}, Jb = {}, Kb = {}, dm = !1, $b = {}, Sv = {}, F1 = {
      dehydrated: null,
      treeContext: null,
      retryLane: 0,
      hydrationErrors: null
    }, kb = !1, Wb = null;
    Wb = /* @__PURE__ */ new Set();
    var Do = !1, Jl = !1, I1 = !1, Fb = typeof WeakSet == "function" ? WeakSet : Set, fa = null, hm = null, mm = null, Kl = null, _n = !1, zc = null, Pl = !1, ap = 8192, nT = {
      getCacheForType: function(e) {
        var t = Et(Ll), a = t.data.get(e);
        return a === void 0 && (a = e(), t.data.set(e, a)), a;
      },
      cacheSignal: function() {
        return Et(Ll).controller.signal;
      },
      getOwner: function() {
        return ja;
      }
    };
    if (typeof Symbol == "function" && Symbol.for) {
      var np = Symbol.for;
      np("selector.component"), np("selector.has_pseudo_class"), np("selector.role"), np("selector.test_id"), np("selector.text");
    }
    var uT = [], cT = typeof WeakMap == "function" ? WeakMap : Map, sa = 0, ea = 2, uu = 4, Ro = 0, up = 1, Qr = 2, bv = 3, Pf = 4, Ev = 6, Ib = 5, pt = sa, Jt = null, nt = null, tt = 0, Mn = 0, Tv = 1, Vr = 2, cp = 3, Pb = 4, P1 = 5, ip = 6, Av = 7, eS = 8, Zr = 9, Bt = Mn, cu = null, es = !1, ym = !1, tS = !1, vi = 0, dl = Ro, ts = 0, ls = 0, lS = 0, Cn = 0, Jr = 0, op = null, dn = null, Ov = !1, zv = 0, e2 = 0, t2 = 300, Dv = 1 / 0, l2 = 500, fp = null, Ol = null, as = null, Rv = 0, aS = 1, nS = 2, a2 = 3, ns = 0, n2 = 1, u2 = 2, c2 = 3, i2 = 4, _v = 5, $l = 0, us = null, pm = null, Dc = 0, uS = 0, cS = -0, iS = null, o2 = null, f2 = null, Rc = Rv, s2 = null, iT = 50, sp = 0, oS = null, fS = !1, Mv = !1, oT = 50, Kr = 0, rp = null, gm = !1, Cv = null, r2 = !1, d2 = /* @__PURE__ */ new Set(), fT = {}, Uv = null, vm = null, sS = !1, rS = !1, xv = !1, dS = !1, cs = 0, hS = {};
    (function() {
      for (var e = 0; e < O1.length; e++) {
        var t = O1[e], a = t.toLowerCase();
        t = t[0].toUpperCase() + t.slice(1), Hn(a, "on" + t);
      }
      Hn(LS, "onAnimationEnd"), Hn(QS, "onAnimationIteration"), Hn(VS, "onAnimationStart"), Hn("dblclick", "onDoubleClick"), Hn("focusin", "onFocus"), Hn("focusout", "onBlur"), Hn(qE, "onTransitionRun"), Hn(wE, "onTransitionStart"), Hn(GE, "onTransitionCancel"), Hn(ZS, "onTransitionEnd");
    })(), Qe("onMouseEnter", ["mouseout", "mouseover"]), Qe("onMouseLeave", ["mouseout", "mouseover"]), Qe("onPointerEnter", ["pointerout", "pointerover"]), Qe("onPointerLeave", ["pointerout", "pointerover"]), lt(
      "onChange",
      "change click focusin focusout input keydown keyup selectionchange".split(
        " "
      )
    ), lt(
      "onSelect",
      "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(
        " "
      )
    ), lt("onBeforeInput", [
      "compositionend",
      "keypress",
      "textInput",
      "paste"
    ]), lt(
      "onCompositionEnd",
      "compositionend focusout keydown keypress keyup mousedown".split(" ")
    ), lt(
      "onCompositionStart",
      "compositionstart focusout keydown keypress keyup mousedown".split(" ")
    ), lt(
      "onCompositionUpdate",
      "compositionupdate focusout keydown keypress keyup mousedown".split(" ")
    );
    var dp = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(
      " "
    ), mS = new Set(
      "beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(dp)
    ), Nv = "_reactListening" + Math.random().toString(36).slice(2), h2 = !1, m2 = !1, Hv = !1, y2 = !1, jv = !1, Bv = !1, p2 = !1, Yv = {}, sT = /\r\n?/g, rT = /\u0000|\uFFFD/g, $r = "http://www.w3.org/1999/xlink", yS = "http://www.w3.org/XML/1998/namespace", dT = "javascript:throw new Error('React form unexpectedly submitted.')", hT = "suppressHydrationWarning", kr = "&", qv = "/&", hp = "$", mp = "/$", is = "$?", Wr = "$~", Sm = "$!", mT = "html", yT = "body", pT = "head", pS = "F!", g2 = "F", v2 = "loading", gT = "style", _o = 0, bm = 1, wv = 2, gS = null, vS = null, S2 = { dialog: !0, webview: !0 }, SS = null, yp = void 0, b2 = typeof setTimeout == "function" ? setTimeout : void 0, vT = typeof clearTimeout == "function" ? clearTimeout : void 0, Fr = -1, E2 = typeof Promise == "function" ? Promise : void 0, ST = typeof queueMicrotask == "function" ? queueMicrotask : typeof E2 < "u" ? function(e) {
      return E2.resolve(null).then(e).catch(yg);
    } : b2, bS = null, Ir = 0, pp = 1, T2 = 2, A2 = 3, Fu = 4, Iu = /* @__PURE__ */ new Map(), O2 = /* @__PURE__ */ new Set(), Mo = At.d;
    At.d = {
      f: function() {
        var e = Mo.f(), t = ln();
        return e || t;
      },
      r: function(e) {
        var t = ae(e);
        t !== null && t.tag === 5 && t.type === "form" ? uf(t) : Mo.r(e);
      },
      D: function(e) {
        Mo.D(e), a0("dns-prefetch", e, null);
      },
      C: function(e, t) {
        Mo.C(e, t), a0("preconnect", e, t);
      },
      L: function(e, t, a) {
        Mo.L(e, t, a);
        var c = Em;
        if (c && e && t) {
          var o = 'link[rel="preload"][as="' + Ut(t) + '"]';
          t === "image" && a && a.imageSrcSet ? (o += '[imagesrcset="' + Ut(
            a.imageSrcSet
          ) + '"]', typeof a.imageSizes == "string" && (o += '[imagesizes="' + Ut(
            a.imageSizes
          ) + '"]')) : o += '[href="' + Ut(e) + '"]';
          var f = o;
          switch (t) {
            case "style":
              f = co(e);
              break;
            case "script":
              f = io(e);
          }
          Iu.has(f) || (e = Ie(
            {
              rel: "preload",
              href: t === "image" && a && a.imageSrcSet ? void 0 : e,
              as: t
            },
            a
          ), Iu.set(f, e), c.querySelector(o) !== null || t === "style" && c.querySelector(
            gr(f)
          ) || t === "script" && c.querySelector(vr(f)) || (t = c.createElement("link"), Pt(t, "link", e), me(t), c.head.appendChild(t)));
        }
      },
      m: function(e, t) {
        Mo.m(e, t);
        var a = Em;
        if (a && e) {
          var c = t && typeof t.as == "string" ? t.as : "script", o = 'link[rel="modulepreload"][as="' + Ut(c) + '"][href="' + Ut(e) + '"]', f = o;
          switch (c) {
            case "audioworklet":
            case "paintworklet":
            case "serviceworker":
            case "sharedworker":
            case "worker":
            case "script":
              f = io(e);
          }
          if (!Iu.has(f) && (e = Ie({ rel: "modulepreload", href: e }, t), Iu.set(f, e), a.querySelector(o) === null)) {
            switch (c) {
              case "audioworklet":
              case "paintworklet":
              case "serviceworker":
              case "sharedworker":
              case "worker":
              case "script":
                if (a.querySelector(vr(f)))
                  return;
            }
            c = a.createElement("link"), Pt(c, "link", e), me(c), a.head.appendChild(c);
          }
        }
      },
      X: function(e, t) {
        Mo.X(e, t);
        var a = Em;
        if (a && e) {
          var c = Ce(a).hoistableScripts, o = io(e), f = c.get(o);
          f || (f = a.querySelector(
            vr(o)
          ), f || (e = Ie({ src: e, async: !0 }, t), (t = Iu.get(o)) && c0(e, t), f = a.createElement("script"), me(f), Pt(f, "link", e), a.head.appendChild(f)), f = {
            type: "script",
            instance: f,
            count: 1,
            state: null
          }, c.set(o, f));
        }
      },
      S: function(e, t, a) {
        Mo.S(e, t, a);
        var c = Em;
        if (c && e) {
          var o = Ce(c).hoistableStyles, f = co(e);
          t = t || "default";
          var d = o.get(f);
          if (!d) {
            var h = { loading: Ir, preload: null };
            if (d = c.querySelector(
              gr(f)
            ))
              h.loading = pp | Fu;
            else {
              e = Ie(
                {
                  rel: "stylesheet",
                  href: e,
                  "data-precedence": t
                },
                a
              ), (a = Iu.get(f)) && u0(e, a);
              var y = d = c.createElement("link");
              me(y), Pt(y, "link", e), y._p = new Promise(function(p, z) {
                y.onload = p, y.onerror = z;
              }), y.addEventListener("load", function() {
                h.loading |= pp;
              }), y.addEventListener("error", function() {
                h.loading |= T2;
              }), h.loading |= Fu, Rf(d, t, c);
            }
            d = {
              type: "stylesheet",
              instance: d,
              count: 1,
              state: h
            }, o.set(f, d);
          }
        }
      },
      M: function(e, t) {
        Mo.M(e, t);
        var a = Em;
        if (a && e) {
          var c = Ce(a).hoistableScripts, o = io(e), f = c.get(o);
          f || (f = a.querySelector(
            vr(o)
          ), f || (e = Ie({ src: e, async: !0, type: "module" }, t), (t = Iu.get(o)) && c0(e, t), f = a.createElement("script"), me(f), Pt(f, "link", e), a.head.appendChild(f)), f = {
            type: "script",
            instance: f,
            count: 1,
            state: null
          }, c.set(o, f));
        }
      }
    };
    var Em = typeof document > "u" ? null : document, Gv = null, bT = 6e4, ET = 800, TT = 500, ES = 0, TS = null, Xv = null, Pr = d1, gp = {
      $$typeof: Pn,
      Provider: null,
      Consumer: null,
      _currentValue: Pr,
      _currentValue2: Pr,
      _threadCount: 0
    }, z2 = "%c%s%c", D2 = "background: #e6e6e6;background: light-dark(rgba(0,0,0,0.1), rgba(255,255,255,0.25));color: #000000;color: light-dark(#000000, #ffffff);border-radius: 2px", R2 = "", Lv = " ", AT = Function.prototype.bind, _2 = !1, M2 = null, C2 = null, U2 = null, x2 = null, N2 = null, H2 = null, j2 = null, B2 = null, Y2 = null, q2 = null;
    M2 = function(e, t, a, c) {
      t = Q(e, t), t !== null && (a = te(t.memoizedState, a, 0, c), t.memoizedState = a, t.baseState = a, e.memoizedProps = Ie({}, e.memoizedProps), a = aa(e, 2), a !== null && je(a, e, 2));
    }, C2 = function(e, t, a) {
      t = Q(e, t), t !== null && (a = Re(t.memoizedState, a, 0), t.memoizedState = a, t.baseState = a, e.memoizedProps = Ie({}, e.memoizedProps), a = aa(e, 2), a !== null && je(a, e, 2));
    }, U2 = function(e, t, a, c) {
      t = Q(e, t), t !== null && (a = Be(t.memoizedState, a, c), t.memoizedState = a, t.baseState = a, e.memoizedProps = Ie({}, e.memoizedProps), a = aa(e, 2), a !== null && je(a, e, 2));
    }, x2 = function(e, t, a) {
      e.pendingProps = te(e.memoizedProps, t, 0, a), e.alternate && (e.alternate.pendingProps = e.pendingProps), t = aa(e, 2), t !== null && je(t, e, 2);
    }, N2 = function(e, t) {
      e.pendingProps = Re(e.memoizedProps, t, 0), e.alternate && (e.alternate.pendingProps = e.pendingProps), t = aa(e, 2), t !== null && je(t, e, 2);
    }, H2 = function(e, t, a) {
      e.pendingProps = Be(
        e.memoizedProps,
        t,
        a
      ), e.alternate && (e.alternate.pendingProps = e.pendingProps), t = aa(e, 2), t !== null && je(t, e, 2);
    }, j2 = function(e) {
      var t = aa(e, 2);
      t !== null && je(t, e, 2);
    }, B2 = function(e) {
      var t = Uo(), a = aa(e, t);
      a !== null && je(a, e, t);
    }, Y2 = function(e) {
      mt = e;
    }, q2 = function(e) {
      Se = e;
    };
    var Qv = !0, Vv = null, AS = !1, os = null, fs = null, ss = null, vp = /* @__PURE__ */ new Map(), Sp = /* @__PURE__ */ new Map(), rs = [], OT = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(
      " "
    ), Zv = null;
    if (In.prototype.render = p0.prototype.render = function(e) {
      var t = this._internalRoot;
      if (t === null) throw Error("Cannot update an unmounted root.");
      var a = arguments;
      typeof a[1] == "function" ? console.error(
        "does not support the second callback argument. To execute a side effect after rendering, declare it in a component body with useEffect()."
      ) : ut(a[1]) ? console.error(
        "You passed a container to the second argument of root.render(...). You don't need to pass it again since you already passed it to create the root."
      ) : typeof a[1] < "u" && console.error(
        "You passed a second argument to root.render(...) but it only accepts one argument."
      ), a = e;
      var c = t.current, o = ua(c);
      _h(c, o, a, t, null, null);
    }, In.prototype.unmount = p0.prototype.unmount = function() {
      var e = arguments;
      if (typeof e[0] == "function" && console.error(
        "does not support a callback argument. To execute a side effect after rendering, declare it in a component body with useEffect()."
      ), e = this._internalRoot, e !== null) {
        this._internalRoot = null;
        var t = e.containerInfo;
        (pt & (ea | uu)) !== sa && console.error(
          "Attempted to synchronously unmount a root while React was already rendering. React cannot finish unmounting the root until the current render has completed, which may lead to a race condition."
        ), _h(e.current, 2, null, e, null, null), ln(), t[Ec] = null;
      }
    }, In.prototype.unstable_scheduleHydration = function(e) {
      if (e) {
        var t = Uc();
        e = { blockedOn: null, target: e, priority: t };
        for (var a = 0; a < rs.length && t !== 0 && t < rs[a].priority; a++) ;
        rs.splice(a, 0, e), a === 0 && y0(e);
      }
    }, (function() {
      var e = Ar.version;
      if (e !== "19.2.4")
        throw Error(
          `Incompatible React versions: The "react" and "react-dom" packages must have the exact same version. Instead got:
  - react:      ` + (e + `
  - react-dom:  19.2.4
Learn more: https://react.dev/warnings/version-mismatch`)
        );
    })(), typeof Map == "function" && Map.prototype != null && typeof Map.prototype.forEach == "function" && typeof Set == "function" && Set.prototype != null && typeof Set.prototype.clear == "function" && typeof Set.prototype.forEach == "function" || console.error(
      "React depends on Map and Set built-in types. Make sure that you load a polyfill in older browsers. https://react.dev/link/react-polyfills"
    ), At.findDOMNode = function(e) {
      var t = e._reactInternals;
      if (t === void 0)
        throw typeof e.render == "function" ? Error("Unable to find node on an unmounted component.") : (e = Object.keys(e).join(","), Error(
          "Argument appears to not be a ReactComponent. Keys: " + e
        ));
      return e = wt(t), e = e !== null ? Gt(e) : null, e = e === null ? null : e.stateNode, e;
    }, !(function() {
      var e = {
        bundleType: 1,
        version: "19.2.4",
        rendererPackageName: "react-dom",
        currentDispatcherRef: G,
        reconcilerVersion: "19.2.4"
      };
      return e.overrideHookState = M2, e.overrideHookStateDeletePath = C2, e.overrideHookStateRenamePath = U2, e.overrideProps = x2, e.overridePropsDeletePath = N2, e.overridePropsRenamePath = H2, e.scheduleUpdate = j2, e.scheduleRetry = B2, e.setErrorHandler = Y2, e.setSuspenseHandler = q2, e.scheduleRefresh = Ge, e.scheduleRoot = ce, e.setRefreshHandler = it, e.getCurrentFiber = Ht, hs(e);
    })() && mi && window.top === window.self && (-1 < navigator.userAgent.indexOf("Chrome") && navigator.userAgent.indexOf("Edge") === -1 || -1 < navigator.userAgent.indexOf("Firefox"))) {
      var w2 = window.location.protocol;
      /^(https?|file):$/.test(w2) && console.info(
        "%cDownload the React DevTools for a better development experience: https://react.dev/link/react-devtools" + (w2 === "file:" ? `
You might need to use a local HTTP server (instead of file://): https://react.dev/link/react-devtools-faq` : ""),
        "font-weight:bold"
      );
    }
    Ap.createRoot = function(e, t) {
      if (!ut(e))
        throw Error("Target container is not a DOM element.");
      g0(e);
      var a = !1, c = "", o = Xd, f = Ld, d = ry;
      return t != null && (t.hydrate ? console.warn(
        "hydrate through createRoot is deprecated. Use ReactDOMClient.hydrateRoot(container, <App />) instead."
      ) : typeof t == "object" && t !== null && t.$$typeof === Dn && console.error(
        `You passed a JSX element to createRoot. You probably meant to call root.render instead. Example usage:

  let root = createRoot(domContainer);
  root.render(<App />);`
      ), t.unstable_strictMode === !0 && (a = !0), t.identifierPrefix !== void 0 && (c = t.identifierPrefix), t.onUncaughtError !== void 0 && (o = t.onUncaughtError), t.onCaughtError !== void 0 && (f = t.onCaughtError), t.onRecoverableError !== void 0 && (d = t.onRecoverableError)), t = Er(
        e,
        1,
        !1,
        null,
        null,
        a,
        c,
        null,
        o,
        f,
        d,
        wg
      ), e[Ec] = t.current, ci(e), new p0(t);
    }, Ap.hydrateRoot = function(e, t, a) {
      if (!ut(e))
        throw Error("Target container is not a DOM element.");
      g0(e), t === void 0 && console.error(
        "Must provide initial children as second argument to hydrateRoot. Example usage: hydrateRoot(domContainer, <App />)"
      );
      var c = !1, o = "", f = Xd, d = Ld, h = ry, y = null;
      return a != null && (a.unstable_strictMode === !0 && (c = !0), a.identifierPrefix !== void 0 && (o = a.identifierPrefix), a.onUncaughtError !== void 0 && (f = a.onUncaughtError), a.onCaughtError !== void 0 && (d = a.onCaughtError), a.onRecoverableError !== void 0 && (h = a.onRecoverableError), a.formState !== void 0 && (y = a.formState)), t = Er(
        e,
        1,
        !0,
        t,
        a ?? null,
        c,
        o,
        y,
        f,
        d,
        h,
        wg
      ), t.context = jg(null), a = t.current, c = ua(a), c = hn(c), o = Dl(c), o.callback = null, Su(a, o, c), pu(c, "hydrateRoot()", null), a = c, t.current.lanes = a, Un(t, a), Ua(t), e[Ec] = t.current, ci(e), new In(t);
    }, Ap.version = "19.2.4", typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
  })()), Ap;
}
var eE;
function qT() {
  if (eE) return $v.exports;
  eE = 1;
  function Q() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) {
      if (process.env.NODE_ENV !== "production")
        throw new Error("^_^");
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(Q);
      } catch (te) {
        console.error(te);
      }
    }
  }
  return process.env.NODE_ENV === "production" ? (Q(), $v.exports = BT()) : $v.exports = YT(), $v.exports;
}
var wT = qT();
const GT = /* @__PURE__ */ tE(wT), Tm = {
  NC: { lead: 252, transfer: 1400, case: 3010 },
  NY: { lead: 315, transfer: 1715, case: 3640 },
  AZ: { lead: 315, transfer: 1715, case: 3640 },
  UT: { lead: 315, transfer: 1715, case: 3640 },
  TX: { lead: 378, transfer: 2030, case: 4270 },
  PA: { lead: 378, transfer: 2030, case: 4270 },
  NM: { lead: 378, transfer: 2030, case: 4270 },
  CA: { lead: 673, transfer: 3504, case: 7218 }
}, Iv = {
  NC: { lead: 180, transfer: 1e3, case: 2150 },
  NY: { lead: 225, transfer: 1225, case: 2600 },
  AZ: { lead: 225, transfer: 1225, case: 2600 },
  UT: { lead: 225, transfer: 1225, case: 2600 },
  TX: { lead: 270, transfer: 1450, case: 3050 },
  PA: { lead: 270, transfer: 1450, case: 3050 },
  NM: { lead: 270, transfer: 1450, case: 3050 },
  CA: { lead: 481, transfer: 2503, case: 5156 }
}, Am = (Q, te) => {
  const Be = Object.values(Q).map((U) => U[te]);
  return Math.round(Be.reduce((U, Re) => U + Re, 0) / Be.length);
}, Fv = {
  lead: Am(Tm, "lead"),
  transfer: Am(Tm, "transfer"),
  case: Am(Tm, "case")
}, XT = {
  lead: Am(Iv, "lead"),
  transfer: Am(Iv, "transfer"),
  case: Am(Iv, "case")
}, LT = [
  { code: "DEFAULT", name: "Average (All States)" },
  { code: "AL", name: "Alabama" },
  { code: "AK", name: "Alaska" },
  { code: "AZ", name: "Arizona" },
  { code: "AR", name: "Arkansas" },
  { code: "CA", name: "California" },
  { code: "CO", name: "Colorado" },
  { code: "CT", name: "Connecticut" },
  { code: "DE", name: "Delaware" },
  { code: "FL", name: "Florida" },
  { code: "GA", name: "Georgia" },
  { code: "HI", name: "Hawaii" },
  { code: "ID", name: "Idaho" },
  { code: "IL", name: "Illinois" },
  { code: "IN", name: "Indiana" },
  { code: "IA", name: "Iowa" },
  { code: "KS", name: "Kansas" },
  { code: "KY", name: "Kentucky" },
  { code: "LA", name: "Louisiana" },
  { code: "ME", name: "Maine" },
  { code: "MD", name: "Maryland" },
  { code: "MA", name: "Massachusetts" },
  { code: "MI", name: "Michigan" },
  { code: "MN", name: "Minnesota" },
  { code: "MS", name: "Mississippi" },
  { code: "MO", name: "Missouri" },
  { code: "MT", name: "Montana" },
  { code: "NE", name: "Nebraska" },
  { code: "NV", name: "Nevada" },
  { code: "NH", name: "New Hampshire" },
  { code: "NJ", name: "New Jersey" },
  { code: "NM", name: "New Mexico" },
  { code: "NY", name: "New York" },
  { code: "NC", name: "North Carolina" },
  { code: "ND", name: "North Dakota" },
  { code: "OH", name: "Ohio" },
  { code: "OK", name: "Oklahoma" },
  { code: "OR", name: "Oregon" },
  { code: "PA", name: "Pennsylvania" },
  { code: "RI", name: "Rhode Island" },
  { code: "SC", name: "South Carolina" },
  { code: "SD", name: "South Dakota" },
  { code: "TN", name: "Tennessee" },
  { code: "TX", name: "Texas" },
  { code: "UT", name: "Utah" },
  { code: "VT", name: "Vermont" },
  { code: "VA", name: "Virginia" },
  { code: "WA", name: "Washington" },
  { code: "WV", name: "West Virginia" },
  { code: "WI", name: "Wisconsin" },
  { code: "WY", name: "Wyoming" }
], _S = 3e4, MS = 0.33, DS = _S * MS, QT = {
  lead: 0.1,
  // 10% of leads become signed cases
  transfer: 0.5,
  // 50% of transfers become signed cases
  case: 1
  // 100% (already signed)
}, RS = (Q, te) => {
  window.mvaAnalytics && typeof window.mvaAnalytics.track == "function" && window.mvaAnalytics.track(Q, te), console.log("[MVA Analytics]", Q, te);
}, hl = (Q) => new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 0,
  maximumFractionDigits: 0
}).format(Q), ed = (Q, te = 1) => Number.isInteger(Q) ? Q.toString() : Q.toFixed(te);
function VT({ embedded: Q = !1 }) {
  const [te, Be] = ds.useState("lead"), [U, Re] = ds.useState("CA"), [Se, mt] = ds.useState(1e4), [le, ne] = ds.useState(!1), W = ds.useCallback((Me) => Tm[Me] || Fv, []), Ne = ds.useCallback((Me) => Iv[Me] || XT, []), w = W(U), x = Ne(U), ce = w[te], Ge = x[te], it = Se / ce, ut = QT[te], Ze = it * ut, qt = Ze * DS, Ot = it * Ge, Ct = Se - Ot, wt = Se > 0 ? Ct / Se * 100 : 0, Gt = Se > 0 ? (qt - Se) / Se * 100 : 0;
  ds.useEffect(() => {
    RS("calculation_updated", {
      offerType: te,
      state: U,
      budget: Se,
      guaranteedQty: it,
      expectedRevenue: qt
    });
  }, [te, U, Se, it, qt]);
  const Ae = {
    lead: "Guaranteed Leads",
    transfer: "Live Transfers",
    case: "Signed Cases"
  }, Je = Q ? "mva-widget p-4" : "min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4 md:p-8";
  return /* @__PURE__ */ L.jsx("div", { className: Je, children: /* @__PURE__ */ L.jsxs("div", { className: `max-w-4xl mx-auto ${!Q && "pt-8"}`, children: [
    /* @__PURE__ */ L.jsxs("div", { className: "text-center mb-8", children: [
      /* @__PURE__ */ L.jsx("h1", { className: "text-3xl md:text-4xl font-bold text-white mb-2", children: "MVA Calculator" }),
      /* @__PURE__ */ L.jsx("p", { className: "text-blue-200 text-lg", children: "Motor Vehicle Accident Lead Pricing & ROI Calculator" })
    ] }),
    /* @__PURE__ */ L.jsxs("div", { className: "bg-white/10 backdrop-blur-lg rounded-2xl p-6 md:p-8 border border-white/20 shadow-2xl", children: [
      /* @__PURE__ */ L.jsxs("div", { className: "grid md:grid-cols-3 gap-6 mb-8", children: [
        /* @__PURE__ */ L.jsxs("div", { children: [
          /* @__PURE__ */ L.jsx("label", { className: "block text-blue-200 text-sm font-medium mb-2", children: "Offer Type" }),
          /* @__PURE__ */ L.jsxs(
            "select",
            {
              value: te,
              onChange: (Me) => {
                Be(Me.target.value), RS("offer_type_changed", { offerType: Me.target.value });
              },
              className: "w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none cursor-pointer",
              children: [
                /* @__PURE__ */ L.jsx("option", { value: "lead", className: "bg-slate-800", children: "Guaranteed Leads" }),
                /* @__PURE__ */ L.jsx("option", { value: "transfer", className: "bg-slate-800", children: "Live Transfers" }),
                /* @__PURE__ */ L.jsx("option", { value: "case", className: "bg-slate-800", children: "Signed Cases" })
              ]
            }
          )
        ] }),
        /* @__PURE__ */ L.jsxs("div", { children: [
          /* @__PURE__ */ L.jsx("label", { className: "block text-blue-200 text-sm font-medium mb-2", children: "State" }),
          /* @__PURE__ */ L.jsx(
            "select",
            {
              value: U,
              onChange: (Me) => {
                Re(Me.target.value), RS("state_changed", { state: Me.target.value });
              },
              className: "w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none cursor-pointer",
              children: LT.map((Me) => /* @__PURE__ */ L.jsxs("option", { value: Me.code, className: "bg-slate-800", children: [
                Me.name,
                " ",
                Tm[Me.code] ? "" : "(Avg)"
              ] }, Me.code))
            }
          )
        ] }),
        /* @__PURE__ */ L.jsxs("div", { children: [
          /* @__PURE__ */ L.jsx("label", { className: "block text-blue-200 text-sm font-medium mb-2", children: "Budget" }),
          /* @__PURE__ */ L.jsxs("div", { className: "relative", children: [
            /* @__PURE__ */ L.jsx("span", { className: "absolute left-4 top-1/2 -translate-y-1/2 text-white/60", children: "$" }),
            /* @__PURE__ */ L.jsx(
              "input",
              {
                type: "number",
                value: Se,
                onChange: (Me) => mt(Math.max(0, parseFloat(Me.target.value) || 0)),
                className: "w-full bg-white/10 border border-white/20 rounded-lg pl-8 pr-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                min: "0",
                step: "100"
              }
            )
          ] })
        ] })
      ] }),
      /* @__PURE__ */ L.jsxs("div", { className: "grid md:grid-cols-2 gap-6 mb-8", children: [
        /* @__PURE__ */ L.jsxs("div", { className: "bg-gradient-to-br from-blue-600/30 to-blue-800/30 rounded-xl p-6 border border-blue-400/30", children: [
          /* @__PURE__ */ L.jsx("h3", { className: "text-blue-200 text-sm font-medium uppercase tracking-wide mb-4", children: "Client Gets (Guaranteed)" }),
          /* @__PURE__ */ L.jsxs("div", { className: "flex items-end justify-between", children: [
            /* @__PURE__ */ L.jsxs("div", { children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-5xl font-bold text-white", children: ed(it) }),
              /* @__PURE__ */ L.jsx("p", { className: "text-blue-200 mt-1", children: Ae[te] })
            ] }),
            /* @__PURE__ */ L.jsx("div", { className: "text-right", children: /* @__PURE__ */ L.jsxs("p", { className: "text-lg text-blue-200", children: [
              "@ ",
              hl(ce),
              " each"
            ] }) })
          ] })
        ] }),
        /* @__PURE__ */ L.jsxs("div", { className: "bg-gradient-to-br from-emerald-600/30 to-emerald-800/30 rounded-xl p-6 border border-emerald-400/30", children: [
          /* @__PURE__ */ L.jsx("h3", { className: "text-emerald-200 text-sm font-medium uppercase tracking-wide mb-4", children: "Kurios Profitability" }),
          /* @__PURE__ */ L.jsxs("div", { className: "space-y-3", children: [
            /* @__PURE__ */ L.jsxs("div", { className: "flex justify-between items-center", children: [
              /* @__PURE__ */ L.jsx("span", { className: "text-emerald-200", children: "Revenue:" }),
              /* @__PURE__ */ L.jsx("span", { className: "text-white font-semibold", children: hl(Se) })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "flex justify-between items-center", children: [
              /* @__PURE__ */ L.jsx("span", { className: "text-emerald-200", children: "Our Cost:" }),
              /* @__PURE__ */ L.jsxs("span", { className: "text-white font-semibold", children: [
                "-",
                hl(Ot)
              ] })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "border-t border-emerald-400/30 pt-2 flex justify-between items-center", children: [
              /* @__PURE__ */ L.jsx("span", { className: "text-emerald-200", children: "Profit:" }),
              /* @__PURE__ */ L.jsx("span", { className: `text-2xl font-bold ${Ct >= 0 ? "text-emerald-400" : "text-red-400"}`, children: hl(Ct) })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "flex justify-between items-center", children: [
              /* @__PURE__ */ L.jsx("span", { className: "text-emerald-200", children: "Margin:" }),
              /* @__PURE__ */ L.jsxs("span", { className: `font-semibold ${wt >= 30 ? "text-emerald-400" : "text-yellow-400"}`, children: [
                wt.toFixed(1),
                "%"
              ] })
            ] })
          ] })
        ] })
      ] }),
      /* @__PURE__ */ L.jsxs("div", { className: "bg-gradient-to-br from-purple-600/30 to-purple-800/30 rounded-xl p-6 border border-purple-400/30 mb-8", children: [
        /* @__PURE__ */ L.jsx("h3", { className: "text-purple-200 text-sm font-medium uppercase tracking-wide mb-4", children: "Client ROI Projection" }),
        /* @__PURE__ */ L.jsxs("div", { className: "grid md:grid-cols-4 gap-4", children: [
          /* @__PURE__ */ L.jsxs("div", { className: "text-center", children: [
            /* @__PURE__ */ L.jsx("p", { className: "text-3xl font-bold text-white", children: ed(it) }),
            /* @__PURE__ */ L.jsx("p", { className: "text-purple-200 text-sm", children: Ae[te] })
          ] }),
          /* @__PURE__ */ L.jsx("div", { className: "text-center flex items-center justify-center", children: /* @__PURE__ */ L.jsxs("div", { children: [
            /* @__PURE__ */ L.jsx("p", { className: "text-purple-200", children: "×" }),
            /* @__PURE__ */ L.jsxs("p", { className: "text-white font-semibold", children: [
              (ut * 100).toFixed(0),
              "% sign rate"
            ] })
          ] }) }),
          /* @__PURE__ */ L.jsxs("div", { className: "text-center", children: [
            /* @__PURE__ */ L.jsx("p", { className: "text-3xl font-bold text-white", children: ed(Ze) }),
            /* @__PURE__ */ L.jsx("p", { className: "text-purple-200 text-sm", children: "Signed Cases" })
          ] }),
          /* @__PURE__ */ L.jsxs("div", { className: "text-center", children: [
            /* @__PURE__ */ L.jsx("p", { className: "text-3xl font-bold text-emerald-400", children: hl(qt) }),
            /* @__PURE__ */ L.jsx("p", { className: "text-purple-200 text-sm", children: "Firm Revenue" })
          ] })
        ] }),
        /* @__PURE__ */ L.jsxs("div", { className: "mt-4 pt-4 border-t border-purple-400/30 flex flex-wrap justify-between items-center gap-4", children: [
          /* @__PURE__ */ L.jsxs("div", { className: "text-purple-200 text-sm", children: [
            "Based on ",
            hl(_S),
            " avg settlement × ",
            (MS * 100).toFixed(0),
            "% contingency = ",
            hl(DS),
            "/case"
          ] }),
          /* @__PURE__ */ L.jsxs("div", { className: "text-right", children: [
            /* @__PURE__ */ L.jsx("span", { className: "text-purple-200 mr-2", children: "Client ROI:" }),
            /* @__PURE__ */ L.jsxs("span", { className: `text-2xl font-bold ${Gt >= 0 ? "text-emerald-400" : "text-red-400"}`, children: [
              Gt.toFixed(0),
              "%"
            ] })
          ] })
        ] })
      ] }),
      /* @__PURE__ */ L.jsx(
        "button",
        {
          onClick: () => ne(!le),
          className: "w-full text-center text-blue-300 hover:text-blue-100 text-sm py-2 transition-colors",
          children: le ? "▼ Hide Formulas" : "▶ Show Formulas & Pricing Breakdown"
        }
      ),
      le && /* @__PURE__ */ L.jsxs("div", { className: "mt-6 space-y-6", children: [
        /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-800/50 rounded-xl p-6 border border-slate-600/30", children: [
          /* @__PURE__ */ L.jsx("h4", { className: "text-white font-semibold mb-4", children: "State Pricing Reference" }),
          /* @__PURE__ */ L.jsx("div", { className: "overflow-x-auto", children: /* @__PURE__ */ L.jsxs("table", { className: "w-full text-sm", children: [
            /* @__PURE__ */ L.jsx("thead", { children: /* @__PURE__ */ L.jsxs("tr", { className: "text-slate-400 border-b border-slate-600", children: [
              /* @__PURE__ */ L.jsx("th", { className: "text-left py-2 px-3", children: "State" }),
              /* @__PURE__ */ L.jsx("th", { className: "text-right py-2 px-3", children: "Lead" }),
              /* @__PURE__ */ L.jsx("th", { className: "text-right py-2 px-3", children: "Transfer" }),
              /* @__PURE__ */ L.jsx("th", { className: "text-right py-2 px-3", children: "Case" })
            ] }) }),
            /* @__PURE__ */ L.jsxs("tbody", { children: [
              Object.entries(Tm).map(([Me, se]) => /* @__PURE__ */ L.jsxs("tr", { className: `border-b border-slate-700/50 ${U === Me ? "bg-blue-600/20" : ""}`, children: [
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-white font-medium", children: Me }),
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-right text-slate-300", children: hl(se.lead) }),
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-right text-slate-300", children: hl(se.transfer) }),
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-right text-slate-300", children: hl(se.case) })
              ] }, Me)),
              /* @__PURE__ */ L.jsxs("tr", { className: "border-b border-slate-700/50 bg-slate-700/30", children: [
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-white font-medium", children: "Default (Avg)" }),
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-right text-slate-300", children: hl(Fv.lead) }),
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-right text-slate-300", children: hl(Fv.transfer) }),
                /* @__PURE__ */ L.jsx("td", { className: "py-2 px-3 text-right text-slate-300", children: hl(Fv.case) })
              ] })
            ] })
          ] }) })
        ] }),
        /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-800/50 rounded-xl p-6 border border-slate-600/30", children: [
          /* @__PURE__ */ L.jsx("h4", { className: "text-white font-semibold mb-4", children: "Calculation Formulas" }),
          /* @__PURE__ */ L.jsxs("div", { className: "space-y-4 font-mono text-sm", children: [
            /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-900/50 rounded-lg p-4", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 mb-1", children: "Guaranteed Quantity:" }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-blue-300", children: [
                hl(Se),
                " ÷ ",
                hl(ce),
                " = ",
                /* @__PURE__ */ L.jsxs("span", { className: "text-white font-bold", children: [
                  ed(it, 2),
                  " ",
                  Ae[te]
                ] })
              ] })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-900/50 rounded-lg p-4", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 mb-1", children: "Our Cost (Break-even threshold @ 30% margin):" }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-emerald-300", children: [
                hl(ce),
                " ÷ 1.4 = ",
                /* @__PURE__ */ L.jsxs("span", { className: "text-white font-bold", children: [
                  hl(Ge),
                  "/unit"
                ] })
              ] }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-slate-400 mt-2 text-xs", children: [
                "If we pay more than ",
                hl(Ge),
                " per ",
                te,
                ", we lose money."
              ] })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-900/50 rounded-lg p-4", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 mb-1", children: "Expected Signed Cases:" }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-purple-300", children: [
                ed(it, 2),
                " × ",
                ut * 100,
                "% sign rate = ",
                /* @__PURE__ */ L.jsxs("span", { className: "text-white font-bold", children: [
                  ed(Ze, 2),
                  " cases"
                ] })
              ] })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-900/50 rounded-lg p-4", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 mb-1", children: "Client Revenue:" }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-purple-300", children: [
                ed(Ze, 2),
                " cases × ",
                hl(DS),
                " = ",
                /* @__PURE__ */ L.jsx("span", { className: "text-white font-bold", children: hl(qt) })
              ] }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-slate-400 mt-2 text-xs", children: [
                "Based on ",
                hl(_S),
                " avg settlement × ",
                MS * 100,
                "% contingency"
              ] })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-900/50 rounded-lg p-4", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 mb-1", children: "Client ROI:" }),
              /* @__PURE__ */ L.jsxs("p", { className: "text-emerald-300", children: [
                "(",
                hl(qt),
                " - ",
                hl(Se),
                ") ÷ ",
                hl(Se),
                " × 100 = ",
                /* @__PURE__ */ L.jsxs("span", { className: "text-white font-bold", children: [
                  Gt.toFixed(1),
                  "%"
                ] })
              ] })
            ] })
          ] })
        ] }),
        /* @__PURE__ */ L.jsxs("div", { className: "bg-slate-800/50 rounded-xl p-6 border border-slate-600/30", children: [
          /* @__PURE__ */ L.jsx("h4", { className: "text-white font-semibold mb-4", children: "Sign Rate Assumptions" }),
          /* @__PURE__ */ L.jsxs("div", { className: "grid md:grid-cols-3 gap-4", children: [
            /* @__PURE__ */ L.jsxs("div", { className: "text-center p-4 bg-slate-900/50 rounded-lg", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-2xl font-bold text-white", children: "10%" }),
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 text-sm", children: "Leads → Signed Cases" })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "text-center p-4 bg-slate-900/50 rounded-lg", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-2xl font-bold text-white", children: "50%" }),
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 text-sm", children: "Transfers → Signed Cases" })
            ] }),
            /* @__PURE__ */ L.jsxs("div", { className: "text-center p-4 bg-slate-900/50 rounded-lg", children: [
              /* @__PURE__ */ L.jsx("p", { className: "text-2xl font-bold text-white", children: "100%" }),
              /* @__PURE__ */ L.jsx("p", { className: "text-slate-400 text-sm", children: "Cases (already signed)" })
            ] })
          ] })
        ] })
      ] })
    ] }),
    !Q && /* @__PURE__ */ L.jsx("div", { className: "text-center mt-8 text-slate-400 text-sm", children: /* @__PURE__ */ L.jsx("p", { children: "Kurios MVA Calculator • Pricing as of 2024" }) })
  ] }) });
}
const ZT = {
  init(Q, te = {}) {
    const Be = typeof Q == "string" ? document.querySelector(Q) : Q;
    if (!Be)
      return console.error("[MVA Widget] Container not found:", Q), null;
    const U = GT.createRoot(Be);
    return U.render(
      /* @__PURE__ */ L.jsx(UT.StrictMode, { children: /* @__PURE__ */ L.jsx(VT, { embedded: te.embedded ?? !0, ...te }) })
    ), {
      destroy() {
        U.unmount();
      }
    };
  }
};
typeof window < "u" && (window.MVACalculatorWidget = ZT);
export {
  VT as MVACalculator,
  ZT as MVACalculatorWidget,
  ZT as default
};
