import React, { useState } from 'react';
import './ChatUI.css';
import styles from '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator,
} from '@chatscope/chat-ui-kit-react';
import axios from 'axios';
const ChatUI = () => {
  const BACKEND_PORT = 8188;
  const MBIT = `각 MBTI 유형은 고유한 특징과 행동 양식을 가지고 있습니다. 여기서는 각 유형의 차별화되는 특징을 설명합니다.

  1. ISTJ (검사관)
  ISTJ는 신뢰성과 책임감이 뛰어나며, 규칙과 절차를 철저히 따르는 실용적인 성격입니다. 이들은 계획적이고 조직적인 접근 방식을 통해 목표를 달성하며, 세부 사항에 주의를 기울이는 능력이 탁월합니다.
  
  2. ISFJ (수호자)
  ISFJ는 헌신적이고 배려심이 많아 타인을 돕는 것을 즐깁니다. 이들은 신중하고 세심하게 타인의 필요를 챙기며, 전통과 안정성을 중요시합니다. 신뢰할 수 있는 친구나 동료로서 항상 옆에 있어 줍니다.
  
  3. INFJ (옹호자)
  INFJ는 깊은 통찰력과 강한 이상주의를 바탕으로 사람들에게 영감을 주고, 세상을 더 나은 곳으로 만들기 위해 노력합니다. 이들은 직관적이고 공감 능력이 뛰어나며, 종종 창의적인 해결책을 찾아냅니다.
  
  4. INTJ (전략가)
  INTJ는 독립적이고 분석적인 사고로 전략적 계획을 세우는 데 뛰어납니다. 이들은 미래 지향적이며, 복잡한 문제를 해결하는 데 강점을 보입니다. 효율성과 혁신을 중요시하며, 종종 리더 역할을 맡습니다.
  
  5. ISTP (장인)
  ISTP는 문제 해결 능력이 뛰어나며, 실용적이고 논리적인 접근 방식을 선호합니다. 이들은 유연하고 즉흥적이며, 손으로 무언가를 만들거나 수리하는 것을 즐깁니다. 현실적인 상황에서 빠르게 적응합니다.
  
  6. ISFP (모험가)
  ISFP는 예술적이고 감수성이 풍부한 성격으로, 현재 순간을 즐기며 자신의 감정을 표현합니다. 이들은 자유롭고 유연하며, 전통적인 틀에 얽매이지 않습니다. 대개 평화를 사랑하고 갈등을 피하려고 합니다.
  
  7. INFP (중재자)
  INFP는 이상주의적이며, 깊은 내면의 가치를 중요시합니다. 이들은 창의적이고 공감 능력이 뛰어나며, 종종 예술이나 문학에 관심을 가집니다. 자신의 신념을 지키기 위해 노력하며, 세상을 더 나은 곳으로 만들고자 합니다.
  
  8. INTP (논리학자)
  INTP는 지적 호기심이 강하고 논리적 사고를 즐깁니다. 이들은 독창적이고 분석적이며, 복잡한 개념을 탐구하는 것을 좋아합니다. 종종 이론적이고 추상적인 문제에 몰두하며, 새로운 아이디어를 창출합니다.
  
  9. ESTP (사업가)
  ESTP는 활기차고 현실적인 성격으로, 모험을 즐기고 즉흥적으로 행동합니다. 이들은 사교적이고 적응력이 뛰어나며, 현실적인 문제를 해결하는 데 능숙합니다. 주변 환경에 빠르게 반응하며, 사람들과 잘 어울립니다.
  
  10. ESFP (연예인)
  ESFP는 사교적이고 쾌활한 성격으로, 주변 사람들에게 즐거움을 줍니다. 이들은 현재 순간을 즐기며, 자발적이고 열정적입니다. 사람들과의 상호작용을 즐기며, 종종 파티나 사회적 행사에서 중심 역할을 합니다.
  
  11. ENFP (활동가)
  ENFP는 열정적이고 창의적인 성격으로, 다양한 가능성을 탐구합니다. 이들은 사람들과 깊이 연결되기를 원하며, 새로운 아이디어와 프로젝트를 통해 영감을 받습니다. 주의가 산만할 수 있지만, 항상 새로운 것을 추구합니다.
  
  12. ENTP (변론가)
  ENTP는 독창적이고 논쟁을 즐기는 성격으로, 새로운 아이디어를 탐구하고 도전하는 것을 좋아합니다. 이들은 빠른 두뇌 회전과 논리적인 사고로 문제를 해결하며, 종종 토론에서 상대를 설득합니다.
  
  13. ESTJ (관리자)
  ESTJ는 실용적이고 조직적인 성격으로, 효율적으로 목표를 달성하기 위해 계획을 세웁니다. 이들은 책임감이 강하고 리더십을 발휘하며, 체계적이고 논리적인 접근 방식을 선호합니다.
  
  14. ESFJ (집정관)
  ESFJ는 사교적이고 협력적인 성격으로, 다른 사람들을 돌보는 데 헌신적입니다. 이들은 전통과 질서를 중시하며, 주변 사람들과의 관계를 유지하기 위해 노력합니다. 종종 공동체에서 중심적인 역할을 합니다.
  
  15. ENFJ (주인공)
  ENFJ는 지도력과 공감 능력이 뛰어난 성격으로, 사람들에게 영감을 주고 이끌어갑니다. 이들은 이상주의적이며, 다른 사람들의 성장과 발전을 돕는 데 헌신적입니다. 종종 사회적 변화의 촉매제가 됩니다.
  
  16. ENTJ (지휘관)
  ENTJ는 야망이 크고 결단력이 강한 성격으로, 목표를 달성하기 위해 전략적으로 행동합니다. 이들은 리더십과 조직력을 발휘하며, 효율성과 성과를 중요시합니다. 복잡한 상황에서도 명확한 비전을 제시합니다.`;

  const [typing, setTyping] = useState(false);
  const [messages, setMessages] = useState([
    {
      message: '안녕하세요, 소설을 작성해주는 챗봇 스토리위버입니다. 소설의 문장을 입력해주세요.',
      sender: 'Solar',
      direction: 'incoming',
    },
  ]);
  const [flag, setFlag] = useState(0);
  const [stringConn, setStringConn] = useState([
    {
      message: null,
      sender: 'Solar',
      direction: 'incoming',
    },
  ]);

  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: 'user',
      direction: 'outgoing',
    };
    const newMessages = [...messages, newMessage];

    setMessages(newMessages);

    setTyping(true);
    console.log(flag);
    if (flag === 0) {
      await processMessageToSolar(newMessages);
      setFlag(1);
    } else if (flag === 1) {
      let inputValue = newMessages[newMessages.length - 1].message;
      if (inputValue === '끝') {
        await processMessageToSolar3(newMessages);
      } else {
        await processMessageToSolar2(newMessages);
      }
    }
  };

  async function processMessageToSolar(chatMessages) {
    let inputValue = chatMessages[chatMessages.length - 1].message;
    axios
      .post('http://127.0.0.1:8188/solar_conv_memory', {
        question: inputValue,
      })
      .then((res) => {
        const response = {
          message: res.data.text,
          sender: 'Solar',
          direction: 'incoming',
        };
        setMessages([...chatMessages, response]);
        setTyping(false);
      });
  }
  async function processMessageToSolar2(chatMessages) {
    let inputValue = chatMessages[chatMessages.length - 1].message;
    axios
      .post('http://127.0.0.1:8188/solar_conv_memory2', {
        question: inputValue,
      })
      .then((res) => {
        const response = {
          message: res.data.text,
          sender: 'Solar',
          direction: 'incoming',
        };
        setMessages([...chatMessages, response]);
        setTyping(false);
      });
  }
  async function processMessageToSolar3(chatMessages) {
    let inputValue = `
    `;
    axios
      .post('http://127.0.0.1:8188/solar_conv_memory3', {
        question: inputValue,
      })
      .then((res) => {
        const response = {
          message: res.data.text,
          sender: 'Solar',
          direction: 'incoming',
        };
        axios
          .post('http://127.0.0.1:8188/solar_conv_memory4', {
            question: MBIT,
          })
          .then((res) => {
            const mbti = {
              message: res.data.text,
              sender: 'Solar',
              direction: 'incoming',
            };
            setStringConn(mbti);
          });
        setMessages([...chatMessages, response]);
        setTyping(false);
      });
  }

  return (
    <div className="chatui_top_div">
      <div className="chatui_text">Story Weaver</div>
      <MainContainer>
        <ChatContainer>
          <MessageList typingIndicator={typing ? <TypingIndicator content="Solar is typing" /> : null}>
            {messages.map((message, i) => {
              return <Message key={i} model={message} />;
            })}
            {stringConn.message && (
              <Message model={{ message: stringConn.message, sender: 'Solar', direction: 'incoming' }} />
            )}
          </MessageList>
          <MessageInput placeholder="Type message here" onSend={handleSend} />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default ChatUI;
