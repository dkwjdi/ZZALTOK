import http from '@/util/http-common.js';

const mainStore = {
  namespaced: true,
  state: {
      shareItems:{},
      shareDetail:{},

      //댓글
      commentItems:{},
      commentSize:{},
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
    },
    getCommentSize(state){
      return state.commentSize;
    }
  },
  mutations: {
      SET_SHARE_ITEMS(state, payload){
        state.shareItems = payload;
      },
      SET_SHARE_DETAIL(state, payload){
          state.shareDetail = payload;
          state.shareDetail.regdate = state.shareDetail.regdate.replace("T", " ").substr(0,16);
          state.shareDetail.url = 'http://localhost:8000'+JSON.parse(state.shareDetail.content).url;
      },
      SET_COMMENT_ITEMS(state, payload){
        state.commentItems = payload;
        state.commentSize = Object.keys(payload).length;
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

    updateComment({dispatch, state}, data){
      http
        .put(`/v1/comment/${data.no}?content=${data.content}&nickname=${data.nickname}&password=${data.password}`)
        .then((res) => {
          console.log(res);
          dispatch("fetchCommentList", state.shareDetail.board_no);
        })
        .catch((error) => {
          console.log('에러',error);
          console.log('에러내용',error.response);
        });
    },

    deleteComment({dispatch, state}, data) {
        console.log(data.password);
        http
          .delete(`/v1/comment/${data.no}`, {params:{ password: data.password }})
          .then(() => {
            console.log("댓글 삭제 성공");
            dispatch("fetchCommentList", state.shareDetail.board_no);
          })
          .catch((error) => {
            console.log("에러", error);
            console.log("에러내용", error.response);
          });
      },

    //좋아요 기능
    updateDetailLike({dispatch, state}, no){
      http
      .post(`/v1/board/like/${no}`)
      .then((res) => {
        console.log(res.data);
        dispatch("findShareDetail", state.shareDetail.board_no);
      })
      .catch((error) => {
        console.log("에러", error);
        console.log("에러내용", error.response);
      });
    }
  },
};

export default mainStore;
