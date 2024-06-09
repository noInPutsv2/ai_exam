import streamlit as st # type: ignore
from streamlit_option_menu import option_menu # type: ignore
import MongoDB as mdb
import pandas as pd


with st.sidebar:
    if st.button("Back"):
        st.switch_page("main.py")
    selected = option_menu("See:", ["% of score", "% of I Don't know", "average number of sectences", "average number of sectences pr score", "average score", "score vs sentences", "accuracy", "llm vs sectences simularity", "questions"], default_index=0)


if selected == "% of score":
    st.title("% of score")
    st.write("vector data base")
    vector_data = pd.DataFrame(mdb.Score_precentence("vector"))
    row = st.dataframe(vector_data, width=1000, hide_index = True)

    st.write("graph database")
    graph_data = pd.DataFrame(mdb.Score_precentence("graph"))
    row = st.dataframe(graph_data, width=1000, hide_index = True)

    st.write("combined database")
    vector_data = pd.DataFrame(mdb.Score_precentence("Vector_with_graph_as_context"))
    row = st.dataframe(vector_data, width=1000, hide_index = True)

    st.write("From vector database with sentencesimulatery")
    vector_data = pd.DataFrame(mdb.Score_precentence("Vector_with_sentence_simularity"))
    row = st.dataframe(vector_data, width=1000, hide_index = True)

    st.write("From graph database with sentencesimulatery")
    vector_data = pd.DataFrame(mdb.Score_precentence("graph_with_sentence_simularity"))
    row = st.dataframe(vector_data, width=1000, hide_index = True)

if selected == "% of I Don't know":
    st.title("% of I Don't know")
    data = pd.DataFrame(mdb.percentes_of_I_dont_know())
    row = st.dataframe(data, width=1000, hide_index = True)

if selected == "score vs sentences":
    with st.sidebar:
        vector = st.checkbox("vector database")
        vector_with_sentence_simularity = st.checkbox("vector database with sentence simularity")
        graph = st.checkbox("graph database")
        graph_with_sentence_simularity = st.checkbox("graph database with sentence simularity")
        diagram = st.checkbox("show diagrams")


    st.title("score vs sentences")
    choice = st.radio("show:", ["correct", "wrong", "all"])
    if choice == "correct":
        Contains_correct_awnser = True
    elif choice == "wrong":
        Contains_correct_awnser = False
    else:
        Contains_correct_awnser = {"$ne": "null"}
    if vector:
        st.write("vector database")
        data_vector = pd.DataFrame(mdb.number_of_score_and_sentences("vector", Contains_correct_awnser))
        data_vector.columns = ["id", "number of Chats"]
        df2 = data_vector.id.apply(pd.Series)
        data_vector = pd.concat([data_vector, df2], axis=1)
        row = st.dataframe(data_vector, width=1000, hide_index = True)
        if diagram:
            st.scatter_chart(data_vector, x='sentences', y='Score', size='number of Chats')
    if vector_with_sentence_simularity:
        st.write("vector database with sentence simularity")
        data_vector_ss = pd.DataFrame(mdb.number_of_score_and_sentences("Vector_with_sentence_simularity", Contains_correct_awnser))
        data_vector_ss.columns = ["id", "number of Chats"]
        df2 = data_vector_ss.id.apply(pd.Series)
        data_vector_ss = pd.concat([data_vector_ss, df2], axis=1)
        row = st.dataframe(data_vector_ss, width=1000, hide_index = True)
        if diagram:
            st.scatter_chart(data_vector_ss, x='sentences', y='Score', size='number of Chats')
    if graph:
        st.write("graph database")
        graph_data = pd.DataFrame(mdb.number_of_score_and_sentences("graph", Contains_correct_awnser))
        graph_data.columns = ["id", "number of Chats"]
        df2 = graph_data.id.apply(pd.Series)
        graph_data = pd.concat([graph_data, df2], axis=1)
        row = st.dataframe(graph_data, width=1000, hide_index = True)
        if diagram:
            st.scatter_chart(graph_data, x='sentences', y='Score', size='number of Chats')
    if graph_with_sentence_simularity:
        st.write("graph database with sentence simularity")
        graph_data_ss = pd.DataFrame(mdb.number_of_score_and_sentences("graph_with_sentence_simularity", Contains_correct_awnser))
        graph_data_ss.columns = ["id", "number of Chats"]
        df2 = graph_data_ss.id.apply(pd.Series)
        graph_data_ss = pd.concat([graph_data_ss, df2], axis=1)
        row = st.dataframe(graph_data_ss, width=1000, hide_index = True)
        if diagram:
            st.scatter_chart(graph_data_ss, x='sentences', y='Score', size='number of Chats')

if selected == "average number of sectences":
    st.title("average number of sectences")
    data = pd.DataFrame(mdb.avg_sentences())
    row = st.dataframe(data, width=1000, hide_index = True)

if selected == "average number of sectences pr score":
    st.title("average number of sectences pr score")
    def show(database):
        data = pd.DataFrame(mdb.avg_sentences_pr_score(database))
        data.columns = ["Score", "avg number of sentences"]
        row = st.dataframe(data, width=1000, hide_index = True)
    st.write("vector database")
    show("vector")
    st.write("graph database")
    show("graph")
    st.write("combined database")
    show("Vector_with_graph_as_context")
    st.write("vector database with sentence simularity")
    show("Vector_with_sentence_simularity")
    st.write("graph database with sentence simularity")
    show("graph_with_sentence_simularity")

if selected == "average score":
    st.title("average score across all databases")
    data = pd.DataFrame(mdb.avg_score())
    row = st.dataframe(data, width=1000, hide_index = True)

if selected == "accuracy":
    st.title("accuracy of the llm model")
    st.write("vector database")
    data_vector = pd.DataFrame(mdb.percent_accurcy("vector"))
    row = st.dataframe(data_vector, width=1000, hide_index = True)
    st.write("graph database")
    data_graph = pd.DataFrame(mdb.percent_accurcy("graph"))
    row = st.dataframe(data_graph, width=1000, hide_index = True)
    st.write("Combined database")
    data_graph_ss = pd.DataFrame(mdb.percent_accurcy("Vector_with_graph_as_context"))
    row = st.dataframe(data_graph_ss, width=1000, hide_index = True)

if selected == "llm vs sectences simularity":
    st.title("llm vs sectences simularity")
    st.write("vector database with llm")
    data_vector = pd.DataFrame(mdb.percent_accurcy("vector"))
    row = st.dataframe(data_vector, width=1000, hide_index = True)
    st.write("vector database with sentence simularity")
    data_vector_ss = pd.DataFrame(mdb.percent_accurcy("Vector_with_sentence_simularity"))
    row = st.dataframe(data_vector_ss, width=1000, hide_index = True)
    st.write("graph database with llm")
    data_graph = pd.DataFrame(mdb.percent_accurcy("graph"))
    row = st.dataframe(data_graph, width=1000, hide_index = True)
    st.write("graph database with sentence simularity")
    data_graph_ss = pd.DataFrame(mdb.percent_accurcy("graph_with_sentence_simularity"))
    row = st.dataframe(data_graph_ss, width=1000, hide_index = True)

if selected == "questions":
    st.title("questions")
    st.write("Questions and number of correct and wrong awnsers")
    choice = st.radio(
    "pick what to see",
    ["All llm", "vector", "graph", "combined"])
    if choice == "All llm":
        data = pd.DataFrame(mdb.Rigth_and_wrong_awnser_all())
    else:
        if choice == "vector":
            type_of_DB = "vector"
        elif choice == "graph":
            type_of_DB = "graph"
        else:
            type_of_DB = "Vector_with_graph_as_context"
        data = pd.DataFrame(mdb.Rigth_and_wrong_awnser(type_of_DB))
    row = st.dataframe(data, width=1000, height= 1000, hide_index = True)