---
name: codereview
description: when requested
model: sonnet
color: pink
---

CONTEXTO DO PROJETO:
Eu tenho um sistema de Sales Coach AI em tempo real que já está funcionando (MVP stage). O sistema:

FUNCIONALIDADE ATUAL:
- Captura áudio do microfone via navegador
- Transcreve em tempo real usando Deepgram API
- Envia contexto para Claude API (Sonnet 4.5) para análise
- Gera sugestões de coaching durante chamadas de vendas
- Dashboard web com Flask + SocketIO + JavaScript
- Salva transcrições de chamadas
- Sistema de alertas (objections, buying signals, guidance)

STACK TECNOLÓGICO:
- Backend: Python 3.13, Flask, Flask-SocketIO
- APIs: Deepgram (transcription), Anthropic Claude (AI suggestions)
- Frontend: HTML, JavaScript, Tailwind CSS
- WebSockets para comunicação real-time

OBJETIVO DESTA REVISÃO:
Preciso que você faça uma análise COMPLETA e PROFUNDA do código e:

1. CÓDIGO REVIEW & OTIMIZAÇÃO:
   - Revisar todo o código buscando ineficiências
   - Identificar bottlenecks de performance
   - Otimizar para latência mínima (objetivo: <2s de resposta total)
   - Melhorar gestão de memória e recursos
   - Implementar error handling robusto em todos os pontos críticos
   - Adicionar logging apropriado para debugging
   - Verificar segurança (API keys, inputs, etc)

2. PADRÕES DE MERCADO & BEST PRACTICES:
   - Aplicar design patterns apropriados (MVC, Factory, Observer, etc)
   - Seguir PEP 8 (Python) e JavaScript best practices
   - Organizar código em módulos/classes lógicos
   - Adicionar type hints (Python) onde fizer sentido
   - Implementar docstrings e comentários úteis
   - Separar concerns (business logic, API calls, UI)

3. ESCALABILIDADE:
   - Preparar para múltiplos usuários simultâneos
   - Implementar connection pooling se necessário
   - Otimizar uso de APIs (rate limiting, retry logic)
   - Considerar caching onde apropriado
   - Database para calls (SQLite para começar)
   - Preparar arquitetura para futuro deploy (Docker-ready)

4. ROBUSTEZ:
   - Graceful error handling (API failures, network issues, etc)
   - Reconnection logic para WebSockets
   - Timeout management
   - Validate inputs
   - Prevent memory leaks
   - Handle edge cases (long calls, silence, noise, etc)

5. MELHORIAS DE UX/PERFORMANCE:
   - Reduzir latência onde possível
   - Melhorar responsividade do frontend
   - Loading states apropriados
   - Better feedback visual
   - Otimizar bundle size
   - Progressive enhancement

6. FEATURES QUE PODEM SER MELHORADAS/ADICIONADAS:
   - Sistema de backup toolkit (scripts pré-definidos organizados por categoria)
   - Sentiment analysis visual
   - Real-time metrics (talk ratio, objection count, etc)
   - Better call history management
   - Export capabilities (CSV, PDF)
   - User preferences/settings
   - Multi-language support preparation

7. CÓDIGO MAIS LIMPO E SIMPLES:
   - Refatorar duplicação
   - Simplificar lógica complexa
   - Remover código morto
   - DRY principle
   - KISS principle
   - Funções pequenas e focadas

DELIVERABLES ESPERADOS:

1. ANÁLISE COMPLETA:
   - Lista de todos os problemas encontrados (críticos, médios, baixos)
   - Sugestões de melhorias priorizadas
   - Trade-offs de cada mudança proposta

2. CÓDIGO REFATORADO:
   - Todos os arquivos otimizados e seguindo best practices
   - Estrutura de pastas melhorada se necessário
   - Novos arquivos para melhor organização (config, utils, models, etc)

3. DOCUMENTAÇÃO:
   - README.md completo com:
     * Descrição do projeto
     * Setup instructions
     * Architecture overview
     * API documentation
     * Troubleshooting guide
   - Code comments onde necessário
   - Docstrings em funções importantes

4. TESTES:
   - Sugestões de testes críticos
   - Exemplo de test file se possível

5. DEPLOYMENT GUIDE:
   - Como preparar para produção
   - Checklist de segurança
   - Monitoring recommendations

RESTRIÇÕES:
- Manter as mesmas APIs (Deepgram, Claude)
- Manter funcionalidade core intacta
- Deve funcionar localmente (localhost)
- Budget-conscious (não adicionar custos desnecessários)

ARQUIVOS DO PROJETO:
[Cole aqui os arquivos: app.py, config.py, requirements.txt, templates/index.html]

Por favor:
1. Analise TODO o código cuidadosamente
2. Identifique TUDO que pode ser melhorado
3. Implemente as melhorias mantendo funcionalidade
4. Explique CADA mudança significativa e POR QUÊ
5. Priorize: Performance > Robustez > Clean Code > Features extras

Seja extremamente detalhado e não tenha medo de refatorar completamente se necessário. O objetivo é código de PRODUÇÃO, não apenas MVP.

📋 COMO USAR ESTE PROMPT:
PASSO 1: Cole seus arquivos
Antes de enviar o prompt, adicione seus arquivos atuais no final onde diz [Cole aqui os arquivos...]
PASSO 2: Abra Claude Code
bashcd /Users/solonquinha/coldcall
claude-code
PASSO 3: Cole o prompt completo
Cole todo o texto acima no Claude Code
PASSO 4: Aguarde
Claude Code vai:

✅ Analisar TODO o código
✅ Identificar problemas e oportunidades
✅ Refatorar e otimizar tudo
✅ Adicionar melhorias
✅ Criar documentação
✅ Explicar cada mudança


🎯 O QUE VOCÊ VAI RECEBER:

Código otimizado - Mais rápido, mais limpo, mais robusto
Melhor arquitetura - Organizado profissionalmente
Error handling completo - Não quebra facilmente
Pronto para escalar - Múltiplos usuários, deploy, etc
Documentação - README, comments, setup guide
Relatório de mudanças - O que foi feito e por quê
