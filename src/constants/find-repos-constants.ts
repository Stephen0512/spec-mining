export type SpecID = {
    specName: string,
    regexQuery: string,
    githubQuery: string,
    dependencyName: string
}

export const specIDList: Array<SpecID> = [
    {
        specName: 'ArgParse_Parent',
        regexQuery: '/argparse/ AND /ArgumentParser\((?:[^()]*|\([^()]*\))*\)/ AND /add_argument\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'argparse AND ArgumentParser( AND add_argument(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Arrays_Comparable',
        regexQuery: '/sorted\((?:[^()]*|\([^()]*\))*\)/ OR /\.sort\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'sorted( OR .sort(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Console_CloseErrorWriter',
        regexQuery: '/stderr.close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'stderr AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Console_CloseReader',
        regexQuery: '/stdin.close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'stdin AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Console_CloseWriter',
        regexQuery: '/stdout.close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'stdout AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'CreateWidgetOnSameFrameCanvas',
        regexQuery: 'nltk AND /add_widget\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND add_widget(',
        dependencyName: 'nltk'
    },
    {
        specName: 'DataMustOpenInBinary',
        regexQuery: 'requests AND /post\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND post(',
        dependencyName: 'requests'
    },
    {
        specName: 'faulthandler_disableBeforeClose',
        regexQuery: '/faulthandler.enable\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'faulthandler.enable( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'faulthandler_tracetrackDumpBeforeClose',
        regexQuery: '/dump_traceback_later\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'dump_traceback_later( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'faulthandler_unregisterBeforeClose',
        regexQuery: '/faulthandler.register\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'faulthandler.register( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'File_MustClose',
        regexQuery: '/open\((?:[^()]*|\([^()]*\))*\)/ NOT /with open\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'open( AND NOT with open(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'HostnamesTerminatesWithSlash',
        regexQuery: 'requests AND Session AND /mount\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session AND mount(',
        dependencyName: 'requests'
    },
    {
        specName: 'NLTK_MissingMegamArgs',
        regexQuery: 'nltk AND /write_megam_file\((?:[^()]*|\([^()]*\))*\)/ AND /call_megam\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND write_megam_file( AND call_megam(',
        dependencyName: 'nltk'
    },
    {
        specName: 'NLTK_MustImplementEntries',
        regexQuery: 'nltk AND /IBMModel1\((?:[^()]*|\([^()]*\))*\)/ OR /IBMModel2\((?:[^()]*|\([^()]*\))*\)/ OR /IBMModel3\((?:[^()]*|\([^()]*\))*\)/ OR /IBMModel4\((?:[^()]*|\([^()]*\))*\)/ OR /IBMModel5\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND IBMModel1 OR IBMModel2 OR IBMModel3 OR IBMModel4 OR IBMModel5',
        dependencyName: 'nltk'
    },
    {
        specName: 'NLTK_MutableProbDistSumToOne',
        regexQuery: 'nltk AND /MutableProbDist\((?:[^()]*|\([^()]*\))*\)/ AND /\.update\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND MutableProbDist( AND .update(',
        dependencyName: 'nltk'
    },
    {
        specName: 'NLTK_NonterminalSymbolMutability',
        regexQuery: 'nltk AND /Nonterminal\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND Nonterminal(',
        dependencyName: 'nltk'
    },
    {
        specName: 'NLTK_regexp_span_tokenize',
        regexQuery: 'nltk AND /regexp_span_tokenize\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND regexp_span_tokenize(',
        dependencyName: 'nltk'
    },
    {
        specName: 'NLTK_RegexpTokenizerCapturingParentheses',
        regexQuery: 'nltk AND /RegexpTokenizer\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'nltk AND RegexpTokenizer(',
        dependencyName: 'nltk'
    },
    {
        specName: 'PriorityQueue_NonComparable',
        regexQuery: 'heapq AND /\.heappush\((?:[^()]*|\([^()]*\))*\)/)',
        githubQuery: 'heapq AND .heappush(',
        dependencyName: 'heapq'
    },
    {
        specName: 'PriorityQueue_NonComparable',
        regexQuery: '/\._put\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: '._put(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomMustUseSeed',
        regexQuery: '/random.*\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random AND random(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomMustUseSeed',
        regexQuery: '/random.*\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random AND choice(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomMustUseSeed',
        regexQuery: '/random.*\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random AND randint(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomMustUseSeed',
        regexQuery: '/random.*\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random AND shuffle(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomMustUseSeed',
        regexQuery: '/random.*\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random AND choices(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomMustUseSeed',
        regexQuery: '/random.*\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random AND sample(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomParams_NoPositives',
        regexQuery: '/random.lognormvariate\((?:[^()]*|\([^()]*\))*\)/ OR /random.vonmisesvariate\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random.lognormvariate( OR random.vonmisesvariate(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'RandomRandrange_MustNotUseKwargs',
        regexQuery: '/random.randrange\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'random.randrange(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Requests_PreparedRequestInit',
        regexQuery: '/requests.PreparedRequest\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests.PreparedRequest(',
        dependencyName: 'requests'
    },
    {
        specName: 'StringTemplate_ChangeAfterCreate',
        regexQuery: '/\.delimiter = .+/',
        githubQuery: '.delimiter = ',
        dependencyName: 'pydocs'
    },
    {
        specName: 'TfFunction_NoSideEffect',
        regexQuery: '/@tf\.function\s*\n\s*def\s+\w+\s*\(.*?\):\s*(?:[^\{]*\{[^\}]*\})?.*?open\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: '@tf.function AND def AND open(',
        dependencyName: 'tensorflow'
    },
    {
        specName: 'TfFunction_NoSideEffect',
        regexQuery: '/@tf\.function\s*\n\s*def\s+\w+\s*\(.*?\):\s*(?:[^\{]*\{[^\}]*\})?.*?append\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: '@tf.function AND def AND append(',
        dependencyName: 'tensorflow'
    },    
    {
        specName: 'TfFunction_NoSideEffect',
        regexQuery: '/@tf\.function\s*\n\s*def\s+\w+\s*\(.*?\):\s*(?:[^\{]*\{[^\}]*\})?.*?print\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: '@tf.function AND def AND print(',
        dependencyName: 'tensorflow'
    },
    {
        specName: 'Turtle_LastStatementDone',
        regexQuery: '/turtle.done\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'turtle.done()',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Scipy_IntegrateRange',
        regexQuery: 'scipy AND /quad\((?:[^()]*|\([^()]*\))*\)/ OR /integrate.quad\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'scipy AND integrate AND quad(',
        dependencyName: 'scipy'
    },
    {
        specName: 'Thread_StartOnce',
        regexQuery: '/threading.Thread\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'threading.Thread(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UseProtp_in_FTP_TLS',
        regexQuery: 'ftplib AND /FTP_TLS\((?:[^()]*|\([^()]*\))*\)/ OR /ftplib.FTP_TLS\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'ftplib AND FTP_TLS( OR ftplib.FTP_TLS(',
        dependencyName: 'ftplib'
    },
    {
        specName: 'VerifyPathProcessed',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/ OR /requests.Session\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session( OR requests.Session(',
        dependencyName: 'requests'
    },
    {
        specName: 'XMLParser_ParseMustFinalize',
        regexQuery: 'xml AND parsers AND expat AND /ParserCreate\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'xml AND parsers AND expat AND ParserCreate(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Flask_NoModifyAfterServe',
        regexQuery: 'flask AND /.config\[(?:[^\[\]]*|\[[^\[\]]*\])*\]/',
        githubQuery: 'flask AND .config[',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_NoOptionsChangeAfterEnvCreate',
        regexQuery: 'flask AND /.jinja_options\[(?:[^\[\]]*|\[[^\[\]]*\])*\] =/',
        githubQuery: 'flask AND .config[ =',
        dependencyName: 'flask'
    },
    // Lowercase letters 'a' to 'z'
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(a',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(b',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(c',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(d',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(e',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(f',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(g',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(h',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(i',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(j',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(k',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(l',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(m',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(n',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(o',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(p',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(q',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(r',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(s',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(t',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(u',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(v',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(w',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(x',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(y',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(z',
        dependencyName: 'flask'
    },
    // Uppercase letters 'A' to 'Z'
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(A',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(B',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(C',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(D',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(E',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(F',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(G',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(H',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(I',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(J',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(K',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(L',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(M',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(N',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(O',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(P',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(Q',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(R',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(S',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(T',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(U',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(V',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(W',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(X',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(Y',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(Z',
        dependencyName: 'flask'
    },
    // Underscore '_'
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(_',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(f\'',
        dependencyName: 'flask'
    },
    {
        specName: 'Flask_UnsafeFilePath',
        regexQuery: 'flask AND /send_file\\(\\s*([a-zA-Z_][a-zA-Z0-9_]*)/',
        githubQuery: 'flask AND send_file(f"',
        dependencyName: 'flask'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND RequestHandler',
        githubQuery: 'tornado AND RequestHandler',
        dependencyName: 'tornado'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND web AND RequestHandler AND /self.render\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tornado AND web AND RequestHandler AND self.render(',
        dependencyName: 'tornado'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND web AND RequestHandler AND /self.write\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tornado AND web AND RequestHandler AND self.write',
        dependencyName: 'tornado'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND web AND RequestHandler AND /self.set_header\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tornado AND web AND RequestHandler AND self.set_header',
        dependencyName: 'tornado'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND web AND RequestHandler AND /self.add_header\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tornado AND web AND RequestHandler AND self.add_header',
        dependencyName: 'tornado'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND web AND RequestHandler AND /self.clear_header\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tornado AND web AND RequestHandler AND self.clear_header',
        dependencyName: 'tornado'
    },
    {
        specName: 'Tornado_NoAdditionalOutputCallsAfterFinish',
        regexQuery: 'tornado AND web AND RequestHandler AND /self.set_status\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tornado AND web AND RequestHandler AND self.set_status',
        dependencyName: 'tornado'
    },
    {
        specName: 'FTP_MustLoginOnceOnly',
        regexQuery: 'ftplib AND FTP AND /login\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'ftplib AND FTP AND login(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Logging_MustNotLogAfterShutdown',
        regexQuery: 'logging AND /logging.shutdown\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'logging AND logging.shutdown(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustShutdownExecutor',
        regexQuery: 'concurrent AND futures AND /ThreadPoolExecutor\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'concurrent AND futures AND ThreadPoolExecutor(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustShutdownExecutor',
        regexQuery: 'concurrent AND futures AND /ProcessPoolExecutor\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'concurrent AND futures AND ProcessPoolExecutor(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_NoReadAfterAccess',
        regexQuery: '/os.access\((?:[^()]*|\([^()]*\))*\)/ AND R_OK AND /open\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'os.access( AND R_OK AND open(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_ShouldUseStreamWriterCorrectly',
        regexQuery: 'asyncio AND /open_connection\((?:[^()]*|\([^()]*\))*\)/ AND /.write\((?:[^()]*|\([^()]*\))*\)/ AND /.drain\((?:[^()]*|\([^()]*\))*\)/ OR /.wait_closed\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'asyncio AND open_connection( AND .write( AND .drain( OR .wait_closed(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_ShouldUseStreamWriterCorrectly',
        regexQuery: 'asyncio AND /start_server\((?:[^()]*|\([^()]*\))*\)/ AND /.write\((?:[^()]*|\([^()]*\))*\)/ AND /.drain\((?:[^()]*|\([^()]*\))*\)/ OR /.wait_closed\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'asyncio AND start_server( AND .write( AND .drain( OR .wait_closed(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_ShouldNotInstantiateStreamWriter',
        regexQuery: 'asyncio AND /StreamWriter\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'asyncio AND StreamWriter(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustFlushMmap',
        regexQuery: 'mmap AND /mmap\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'mmap AND mmap(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustCloseSocket',
        regexQuery: 'socket AND /socket\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'socket AND socket(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustCloseSocket',
        regexQuery: 'socket AND /socket\((?:[^()]*|\([^()]*\))*\)/ AND /shutdown\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'socket AND socket( AND shutdown(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustShutdownBeforeCloseSocket',
        regexQuery: 'socket AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'socket AND close(',
        dependencyName: 'pydocs'
    },    
    {
        specName: 'Pydocs_MustShutdownBeforeCloseSocket',
        regexQuery: 'socket AND /socket\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'socket AND socket( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustUnlinkSharedMemory',
        regexQuery: 'multiprocessing OR shared_memory AND /SharedMemory\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing OR shared_memory AND SharedMemory(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustUnlinkSharedMemory',
        regexQuery: 'multiprocessing OR shared_memory AND /SharedMemory\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing OR shared_memory AND SharedMemory( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Requests_MustCloseSession',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseSession',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/ AND /get\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session( AND get(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseSession',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/ AND /post\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session( AND post(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseSession',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/ AND /delete\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session( AND delete(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseSession',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/ AND /put\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session( AND put(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseSession',
        regexQuery: 'requests AND /Session\((?:[^()]*|\([^()]*\))*\)/ AND /patch\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Session( AND patch(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseResponse',
        regexQuery: 'requests AND /Response\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Response(',
        dependencyName: 'requests'
    },
    {
        specName: 'Requests_MustCloseResponse',
        regexQuery: 'requests AND /Response\((?:[^()]*|\([^()]*\))*\)/ AND /prepare\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'requests AND Response( AND prepare(',
        dependencyName: 'requests'
    },
    {
        specName: 'Pydocs_MustReleaseLock',
        regexQuery: 'threading AND /Lock\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'threading AND Lock(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustReleaseLock',
        regexQuery: 'threading AND /Lock\((?:[^()]*|\([^()]*\))*\)/ AND /acquire\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'threading AND Lock( AND acquire(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustReleaseRLock',
        regexQuery: 'threading AND /RLock\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'threading AND RLock(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_MustReleaseRLock',
        regexQuery: 'threading AND /RLock\((?:[^()]*|\([^()]*\))*\)/ AND /acquire\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'threading AND RLock( AND acquire(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustLockOnce',
        regexQuery: 'threading AND /Lock\((?:[^()]*|\([^()]*\))*\)/ AND /acquire\((?:[^()]*|\([^()]*\))*\)/ AND /release\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'threading AND Lock( AND acquire( AND release(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_SharedMemoryUseAfterUnlink',
        regexQuery: 'multiprocessing OR shared_memory AND /SharedMemory\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing OR shared_memory AND SharedMemory(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_SharedMemoryUseAfterUnlink',
        regexQuery: 'multiprocessing OR shared_memory AND /SharedMemory\((?:[^()]*|\([^()]*\))*\)/ AND /unlink\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing OR shared_memory AND SharedMemory( AND unlink(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_SharedMemoryUseAfterUnlink',
        regexQuery: 'multiprocessing OR shared_memory AND /SharedMemory\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing OR shared_memory AND SharedMemory( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_SharedMemoryUseAfterUnlink',
        regexQuery: 'multiprocessing OR shared_memory AND /SharedMemory\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/ AND /unlink\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing OR shared_memory AND SharedMemory( AND close( AND unlink(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http.client AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/ AND /putheader\((?:[^()]*|\([^()]*\))*\)/ AND /endheaders\((?:[^()]*|\([^()]*\))*\)/ AND /send\((?:[^()]*|\([^()]*\))*\)/ AND /getresponse\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http.client AND HTTPConnection( AND putrequest( AND putheader( AND endheaders( AND send( AND getresponse( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/ AND /putheader\((?:[^()]*|\([^()]*\))*\)/ AND /endheaders\((?:[^()]*|\([^()]*\))*\)/ AND /send\((?:[^()]*|\([^()]*\))*\)/ AND /getresponse\((?:[^()]*|\([^()]*\))*\)/ AND /close\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http AND HTTPConnection( AND putrequest( AND putheader( AND endheaders( AND send( AND getresponse( AND close(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/ AND /putheader\((?:[^()]*|\([^()]*\))*\)/ AND /endheaders\((?:[^()]*|\([^()]*\))*\)/ AND /send\((?:[^()]*|\([^()]*\))*\)/ AND /getresponse\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http AND HTTPConnection( AND putrequest( AND putheader( AND endheaders( AND send( AND getresponse(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/ AND /putheader\((?:[^()]*|\([^()]*\))*\)/ AND /endheaders\((?:[^()]*|\([^()]*\))*\)/ AND /send\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http AND HTTPConnection( AND putrequest( AND putheader( AND endheaders( AND send(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/ AND /putheader\((?:[^()]*|\([^()]*\))*\)/ AND /endheaders\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http AND HTTPConnection( AND putrequest( AND putheader( AND endheaders(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/ AND /putheader\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http AND HTTPConnection( AND putrequest( AND putheader(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'Pydocs_HTTPConnectionSendSequence',
        regexQuery: 'http AND /HTTPConnection\((?:[^()]*|\([^()]*\))*\)/ AND /putrequest\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'http AND HTTPConnection( AND putrequest(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_UnsafeIterUseAfterTee',
        regexQuery: 'itertools AND /iter\((?:[^()]*|\([^()]*\))*\)/ AND /tee\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'itertools AND iter( AND tee(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_UselessIterTee',
        regexQuery: 'itertools AND /tee\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'itertools AND tee(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustOnlyUseDictReader',
        regexQuery: 'csv AND /open\((?:[^()]*|\([^()]*\))*\)/ AND /DictReader\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'csv AND open( AND DictReader(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustOnlyUseDictReader',
        regexQuery: 'csv AND /DictReader\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'csv AND DictReader(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustSortBeforeGroupBy',
        regexQuery: 'itertools AND list AND /groupby\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'itertools AND list AND groupby(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustSortBeforeGroupBy',
        regexQuery: 'itertools AND /groupby\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'itertools AND groupby(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustWaitForPopenToFinish',
        regexQuery: 'subprocess AND /Popen\((?:[^()]*|\([^()]*\))*\)/ AND /wait\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'subprocess AND Popen( AND wait(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustWaitForPopenToFinish',
        regexQuery: 'subprocess AND /Popen\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'subprocess AND Popen(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustWaitForPopenToFinish',
        regexQuery: 'subprocess AND /Popen\((?:[^()]*|\([^()]*\))*\)/ AND /wait\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'subprocess AND Popen( AND wait(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustOnlyAddSynchronizableDataToSharedList',
        regexQuery: 'multiprocessing AND Manager AND /list\((?:[^()]*|\([^()]*\))*\)/ AND /append\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing AND Manager AND list( AND append(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustOnlyAddSynchronizableDataToSharedList',
        regexQuery: 'multiprocessing AND Manager AND /list\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing AND Manager AND list(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustOnlyAddSynchronizableDataToSharedList',
        regexQuery: 'multiprocessing AND /list\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'multiprocessing AND list(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'PyDocs_MustOnlyAddSynchronizableDataToSharedList',
        regexQuery: 'Manager AND /list\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'Manager AND list(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeArrayIterator',
        regexQuery: 'array AND /array\((?:[^()]*|\([^()]*\))*\)/ AND /iter\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'array AND array( AND iter(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeArrayIterator',
        regexQuery: 'array AND /array\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'array AND array(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeListIterator',
        regexQuery: '/list\((?:[^()]*|\([^()]*\))*\)/ AND /iter\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'list( AND iter(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeListIterator',
        regexQuery: '/list\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'list(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeDictIterator',
        regexQuery: '/dict\((?:[^()]*|\([^()]*\))*\)/ AND /iter\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'dict( AND iter(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeDictIterator',
        regexQuery: '/dict\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'dict(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeSetIterator',
        regexQuery: '/set\((?:[^()]*|\([^()]*\))*\)/ AND /iter\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'set( AND iter(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeSetIterator',
        regexQuery: '/set\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'set(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeTupleIterator',
        regexQuery: '/tuple\((?:[^()]*|\([^()]*\))*\)/ AND /iter\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tuple( AND iter(',
        dependencyName: 'pydocs'
    },
    {
        specName: 'UnsafeTupleIterator',
        regexQuery: '/tuple\((?:[^()]*|\([^()]*\))*\)/',
        githubQuery: 'tuple(',
        dependencyName: 'pydocs'
    },
]

export const dependencyNames = [
    // Direct dependencies from your API specs (external libraries):
    "nltk",
    "requests",
    "tensorflow",
    "flask",
    "tornado",
    "scipy",
    
    // Other commonly associated dependencies:
    "numpy",
    "pandas",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "sphinx",
    "pytest",
    "coverage",
    "tox",
    "gunicorn",
    "uvicorn",
    "fastapi",
    "jinja2",
    "sqlalchemy",
    "alembic",
    "pillow",
    "pyyaml",
    "pyparsing",
    "networkx",
    "pyopenssl",
    "cryptography",
    "paramiko",
    "twisted",
    "pyzmq",
    "gevent",
    "boto3",
    "botocore",
    "redis",
    "kombu",
    "celery",
    "python-dateutil",  // often listed as "python-dateutil"
    "pytz",
    "six",
    "setuptools",
    "wheel",
    "attrs",
    "flask-restful",
    "marshmallow",
    "requests-oauthlib",
    "pylint",
    "mypy",
    "black",
    "isort"
]