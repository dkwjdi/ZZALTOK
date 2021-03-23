import http from '@/util/http-common.js';

const mainStore = {
  namespaced: true,
  state: {
      shareItems:{},
      shareDetail:{},

      //댓글
      commentItems:{},
  },
  getters: {
    getShareItems(state){
        return state.shareItems;
    },
    getShareDetail(state){
        return state.shareDetail;
    },
    getCommentItems(state){
        return state.commentItems;
    }
  },
  mutations: {
      SET_SHARE_ITEMS(state, payload){
        state.shareItems = payload;
      },
      SET_SHARE_DETAIL(state, payload){
          state.shareDetail = payload;
          state.shareDetail.url = 'http://localhost:8000'+JSON.parse(state.shareDetail.content).url;
      },
      SET_COMMENT_ITEMS(state, payload){
        state.commentItems = payload;
      }
  },
  actions: {
    //공유짤 조회
    fetchShareList({ commit }) {
        http
        .get('/v1/board')
        .then((res) => {
          console.log('공유 리스트 불러오기 성공');
          commit("SET_SHARE_ITEMS", res.data.items);
        })
        .catch((error) => {
          console.log('에러',error);
          console.log('에러내용',error.response);
        });
    },

    //공유 디테일
    findShareDetail({commit, dispatch}, no){
        http
        .get(`/v1/board/detail/${no}`)
        .then((res) => {
          console.log('공유 디테일 불러오기 성공');
          commit("SET_SHARE_DETAIL", res.data);

          dispatch("fetchCommentList", res.data.board_no);
        })
        .catch((error) => {
          console.log('에러',error);
          console.log('에러내용',error.response);
        });
    },

    //댓글 불러오기
    fetchCommentList({commit}, no){
        http
        .get(`/v1/comment/${no}`)
        .then((res) => {
          console.log('댓글 조회 불러오기 성공');
          commit("SET_COMMENT_ITEMS", res.data);
        })
        .catch((error) => {
          console.log('에러',error);
          console.log('에러내용',error.response);
        });
    },

    //댓글 등록
    createComment({dispatch}, data){
        http
        .post(`/v1/comment/write/${data.no}`, data.item)
        .then((res) => {
          console.log('댓글 등록 성공');
          dispatch("fetchCommentList", data.no);
        })
        .catch((error) => {
          console.log('에러',error);
          console.log('에러내용',error.response);
        });
    },

    deleteComment({dispatch, state}, data) {
        http
          .delete(`/v1/board/detail/${data.no}`, data.item)
          .then((res) => {
            console.log("댓글 삭제 성공");
            dispatch("fetchCommentList", state.shareDetail.board_no);
          })
          .catch((error) => {
            console.log("에러", error);
            console.log("에러내용", error.response);
          });
      },
  },
};

export default mainStore;
